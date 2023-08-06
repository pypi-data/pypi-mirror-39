# python built-in library
import os
import argparse
import time
import csv
# 3rd party library
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from skimage.morphology import label
from PIL import Image
from torch.multiprocessing import Pool, get_context
from functools import partial
from itertools import islice
from tqdm import tqdm
# own code
from .config import config
from .dataset import CTCDataset
from . import transform as tx
from .helper import load_ckpt, write_nuclei_prob


def run(ckpt, action=['pred'], target='test'):
    infr_batchsize = config['valid'].getint('inference_batchsize')
    save_png_prob = False
    if (len(action) == 2) and ('pred' in action) and ('png_prob' in action):
        action = 'pred'
        save_png_prob = True
    elif (len(action) == 1):
        action = action[0]
    else:
        raise ValueError(f'Multiple actions: {action} not supported!')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # load one or more checkpoint
    models = []
    for fn in ckpt or [None]:
        # load model
        model, _ = load_ckpt(filepath=fn)
        if not model:
            print("Aborted: checkpoint {} not found!".format(fn))
            return
        # Sets the model in evaluation mode.
        model.eval()
        # put model to GPU
        # Note: Comment out DataParallel due to
        #       (1) we won't need it in our inference scenario
        #       (2) it will change model's class name to 'dataparallel'
        # if torch.cuda.device_count() > 1:
        #     print("Let's use", torch.cuda.device_count(), "GPUs!")
        #     model = nn.DataParallel(model)
        model = model.to(device)
        # append to model list
        models.append(model)

    resize = not config['valid'].getboolean('pred_orig_size')
    transform = tx.Compose([
        tx.Resize(width) if resize else tx.Lambda(lambda *args: args),
        # map label pixel value to 0 or 1
        tx.Lambda(lambda x, y: (x, np.where(y > 0.5, 1., 0.))),
        tx.ToTensor(),
        tx.Normalize(),
    ])
    # decide which dataset to pick sample
    data_dir = os.path.join('data', target)
    dataset = CTCDataset(data_dir, transform, policy='Once')
    if target == 'train':
        _, dataset = dataset.split()

    # iterate dataset and inference each sample
    for batch_data in split_every(infr_batchsize, dataset):
        preds = []
        for data in tqdm(batch_data, desc='Inference'):
            with torch.no_grad():
                uid, y = inference(data, models, resize)
                preds.append([uid, y])
        desc = 'Post-processing'
        if action == 'pred': # 1 output file per inference
            for _ in parallel_processing_with_progress(partial(save_pred_job, src_dir=data_dir, save_png=save_png_prob), preds, desc): pass
        elif action == 'png_prob': # 1 output file per inference
            for _ in parallel_processing_with_progress(save_png_prob_job, preds, desc): pass
# end of run()

def split_every(size, iterable):
    with tqdm(total=len(iterable), desc='Dataset') as pbar:
        src_iter = iter(iterable)
        items = list(islice(src_iter, size))
        while items:
            yield items
            pbar.update(len(items))
            items = list(islice(src_iter, size))

def parallel_processing_with_progress(func, data, desc):
    n_process = config['post'].getint('n_worker')
    with get_context("spawn").Pool(n_process) as p:
        with tqdm(total=len(data), desc=desc) as pbar:
            for result in p.imap(func, data):
                yield result
                pbar.update()

# png for pixel-level CTC probability (nuclei aligned)
def save_pred_job(pred, src_dir, save_png):
    uid, y = pred
    src_dir = os.path.join(src_dir, uid)
    tgt_dir = os.path.join(predict_save_folder(), uid)
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
    write_nuclei_prob(src_dir, tgt_dir, y)
    if save_png:
        save_png_prob_job(pred)

# png for pixel-level CTC probability (non nuclei aligned)
def save_png_prob_job(pred):
    uid, y = pred
    dir = os.path.join(predict_save_folder(), uid, 'images')
    if not os.path.exists(dir):
        os.makedirs(dir)
    img = Image.fromarray((255*y).astype(np.uint8), mode='L')
    img.save(os.path.join(dir, f'CTC_Prob.png'), 'PNG')

def inference(data, models, resize):
    threshold = config['ctc_detector'].getfloat('threshold')
    tta = config['valid'].getboolean('test_time_augment')
    ensemble_policy = config['valid']['ensemble']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # sub-rountine to convert output tensor to numpy
    def convert(t):
        assert isinstance(t, (torch.FloatTensor, torch.cuda.FloatTensor))
        if len(t) == 0:
            return None
        # pixel wise ensemble output of models
        t = torch.mean(t, 0, True)
        # to numpy array
        t = t.to('cpu').numpy()[0]
        if ensemble_policy == 'vote':
            t = np.where(t >= 0.5, 1., 0.) # majority vote
        # channel first [C, H, W] -> channel last [H, W, C]
        t = np.transpose(t, (1, 2, 0))
        # Remove single-dimensional channel from the shape of an array
        t = np.squeeze(t)
        t = align_size(t, size, resize)
        return t

    # get input data
    uid = data['uid']
    size = data['size']
    inputs = data['image']
    # prepare input variables
    inputs = inputs.unsqueeze(0)
    inputs = inputs.to(device)

    if tta:
        txf_funcs = [lambda x: x,
                     lambda x: flip(x, 2), # up down flip
                     lambda x: flip(x, 3), # left right flip
                     lambda x: flip(flip(x, 3), 2),
                    ]
    else:
        txf_funcs = [lambda x: x]

    y_s = torch.FloatTensor().to(device)
    for model in models:
        model_name = type(model).__name__.lower()
        # predict model output
        for txf in txf_funcs:
            # apply test time transform
            x = inputs
            x = txf(x)
            # padding
            if not resize:
                x = pad_tensor(x, size)
            # inference model
            s = model(x)
            # crop padding
            if not resize:
                h, w = size
                s = s[:, :, :h, :w]
            # reverse flip
            s = txf(s)
            # concat outputs
            if ensemble_policy == 'avg':
                y_s = torch.cat([y_s, s], 0)
            elif ensemble_policy == 'vote':
                y_s = torch.cat([y_s, (s > threshold).float()], 0)
            else:
                raise NotImplementedError("Ensemble policy not implemented")
    return uid, convert(y_s)
# end of predict()

def flip(t, dim):
    dim = t.dim() + dim if dim < 0 else dim
    inds = tuple(slice(None, None) if i != dim
            else t.new(torch.arange(t.size(i)-1, -1, -1).tolist()).long()
            for i in range(t.dim()))
    return t[inds]

def pad_tensor(img_tensor, size, mode='reflect'):
    # get proper mini-width required for model input
    # for example, 32 for 5 layers of max_pool
    gcd = config['ctc_detector'].getint('gcd_depth')
    # estimate border padding margin
    # (paddingLeft, paddingRight, paddingTop, paddingBottom)
    pad_w = pad_h = 0
    h, w = size
    if 0 != (w % gcd):
        pad_w = gcd - (w % gcd)
    if 0 != (h % gcd):
        pad_h = gcd - (h % gcd)
    pad = (0, pad_w, 0, pad_h)
    # decide padding mode
    if mode == 'replica':
        f = nn.ReplicationPad2d(pad)
    elif mode == 'constant':
        # padding color should honor each image background, default is black (0)
        bgcolor = 0 if np.median(img_tensor) < 100 else 255
        f = nn.ConstantPad2d(pad, bgcolor)
    elif mode == 'reflect':
        f = nn.ReflectionPad2d(pad)
    else:
        raise NotImplementedError()
    return f(img_tensor)

def align_size(img_array, size, regrowth=True):
    from skimage.transform import resize
    if img_array is None:
        return img_array
    elif regrowth:
        return resize(img_array, size, mode='constant', preserve_range=True)
    else:
        h, w = size
        # crop padding
        return img_array[:h, :w]

def predict_save_folder():
    dir = os.path.join('data', 'predict')
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='inference'
    )
    parser.add_argument('--dataset', action='store', choices=['train', 'valid', 'test'], help='Specify dataset to evaluate')
    parser.add_argument('--action', action='append', choices=['pred', 'png_prob'], help='Specify action to do, multiple actions only for rle_mask & png_preds')
    parser.add_argument('ckpt', nargs='*', help='filepath of checkpoint(s), otherwise lookup checkpoint/current.json')
    parser.set_defaults(dataset='test')
    args = parser.parse_args(args)
    if not args.action:
        args.action = ['pred']
    run(args.ckpt, args.action, args.dataset)
