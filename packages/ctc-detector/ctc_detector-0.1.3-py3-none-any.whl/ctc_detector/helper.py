import os
import json
import csv
import re
import numpy as np
import pandas as pd
import torch
from PIL import Image
from skimage.morphology import label, remove_small_objects
from skimage.segmentation import random_walker
from scipy.ndimage import binary_dilation
from .config import config


def image_picker(root, path, channel='UV', fallback=None, notexist_ok=False):
    ext = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    path = os.path.join(root, path, 'images')
    if not os.path.exists(path):
        return
    files = [f for f in os.listdir(path) if f.endswith(ext)]
    files.sort()
    def _isin(sub, default=None):
        assert isinstance(sub, list)
        for fn in files:
            if any(s in fn for s in sub):
                return fn
        return default
    def _r(fn):
        if not fn:
            return
        if isinstance(fn, list):
            return [os.path.join(path, f) for f in fn]
        return os.path.join(path, fn)
    rule = json.loads(config.get('channels', channel))
    assert isinstance(rule, list)
    if isinstance(rule[0], list):
        # nested rule
        fn = []
        for x in rule:
            fn.append(_isin(x))
        if notexist_ok or not fn.count(None):
            return _r(fn)
    else:
        fn = _isin(rule)
        if notexist_ok or fn is not None:
            return _r(fn)
    # no matched filename, check fallback
    if isinstance(fallback, str):
        return image_picker(root, path, fallback)
    elif isinstance(fallback, int):
        return _r(files[fallback])
    return

# Run-length encoding stolen from https://www.kaggle.com/rakhlin/fast-run-length-encoding-python
def rle_encode(y):
    dots = np.where(y.T.flatten() == 1)[0]
    run_lengths = []
    prev = -2
    for b in dots:
        if (b>prev+1): run_lengths.extend((b + 1, 0))
        run_lengths[-1] += 1
        prev = b
    return run_lengths

# modified from https://www.kaggle.com/paulorzp/run-length-encode-and-decode
# note: the rle encoding is in vertical direction per Kaggle competition rule
def rle_decode(mask_rle, shape):
    h, w = shape
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.full(h * w, False)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = True
    return img.reshape((w, h)).T

# cut-off probabibility to semantic segmentation
def prob_to_segment(raw_bodies):
    threshold=config['ctc_detector'].getfloat('threshold')
    bodies = raw_bodies > threshold
    return bodies

def segment_to_instances(y, y_c, y_m):
    remove_objects = config['post'].getboolean('remove_objects')
    min_object_size = config['post'].getint('min_object_size')
    y, markers = partition_instances(y, y_c, y_m)
    if remove_objects:
        y = remove_small_objects(y, min_size=min_object_size)
    return y, markers

def segment_to_rles(y, y_c, y_m):
    instances, _ = segment_to_instances(y, y_c, y_m)
    idxs = np.unique(instances) # sorted, 1st is background (e.g. 0)
    if len(idxs) == 1:
        yield []
    else:
        for idx in idxs[1:]:
            yield rle_encode(instances == idx)

# It's weird that the order of label & remove_small_objects will have different result.
# It works best in these steps: (1) label, (2) remove small object, (3) restore to boolean type if needed
def drop_small_blobs(mask, min_size, to_label=False):
    mask = label(mask, connectivity=1)
    mask = remove_small_objects(mask, min_size=min_size)
    return mask if to_label else (mask > 0)

def add_missed_blobs(full_mask, labeled_mask, edges):
    missed_mask = full_mask & ~(labeled_mask > 0)
    # bodies must be larger than 1-pixel. weird that the order of label & remove_small_objects
    # will have different result.
    # It works in these steps: (1) label, (2) remove small object, (3) restore to boolean type
    missed_mask = drop_small_blobs(missed_mask, 2, to_label=False)
    missed_markers = label(missed_mask & ~edges)

    if  missed_markers.max() > 0:
        missed_markers[missed_mask == 0] = -1
        if np.any(missed_markers > 0):
            missed_labels = random_walker(missed_mask, missed_markers)
        else:
            missed_labels = np.zeros_like(missed_markers, dtype=np.int32)
        missed_labels[missed_labels <= 0] = 0
        missed_labels = np.where(missed_labels > 0, missed_labels + labeled_mask.max(), 0)
        final_labels = np.add(labeled_mask, missed_labels)
    else:
        final_labels = labeled_mask
    return final_labels

# bodies, markers, and edges are semantic segmentations
def partition_instances(bodies, edges, markers):
    min_object_size = config['post'].getint('min_object_size')
    bodies = drop_small_blobs(bodies, 2, to_label=False) # bodies > 1-pixel to workaround random walker issue
    markers = (markers & ~edges) & bodies
    # remove artifacts caused by non-perfect (mask - contour)
    markers = drop_small_blobs(markers, min_object_size, to_label=True)

    markers[bodies == 0] = -1
    if np.any(markers > 0):
        seg_labels = random_walker(bodies, markers)
    else:
        seg_labels = np.zeros_like(markers, dtype=np.int32)
    seg_labels[seg_labels <= 0] = 0
    markers[markers <= 0] = 0

    final_labels = add_missed_blobs(bodies, seg_labels, edges)
    return final_labels, markers

# merge ctc nuclei into semantic numpy array
def get_ctc_nuclei_array(csv_path, shape):
    nuclei = np.full(shape, False)
    try:
        df = pd.read_csv(csv_path, index_col='ImageId', dtype={'Label': str})
    except FileNotFoundError:
        return nuclei
    if 'Label' not in df.columns:
        return nuclei
    df = df.loc[df['Label'] == 'ctc']
    for row in df.itertuples():
        rle = row.EncodedPixels
        if not isinstance(rle, str):
            continue
        obj = rle_decode(rle, shape)
        nuclei = np.logical_or(nuclei, obj)
    return nuclei

def generate_target_nuclei(path, prob_array):
    focus = prob_to_segment(prob_array)
    fp = image_picker(path, '',  channel='Nuclei')
    if not fp:
        raise FileNotFoundError(f"Nuclei's channel images not found! ({path})")
    s, c, m = Image.open(fp[0]), Image.open(fp[1]), Image.open(fp[2])
    s, c, m = np.asarray(s), np.asarray(c), np.asarray(m)
    focus_ex = binary_dilation(focus, structure=np.full((3,3), True),
                               mask=s, iterations=-1)
    s = s & focus_ex
    rle_csv = os.path.join(path, 'mask.csv')
    with open(rle_csv, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['ImageId', 'EncodedPixels'])
        for idx, rle in enumerate(segment_to_rles(s, c, m)):
            writer.writerow([f'mask_{idx+1}', ' '.join([str(i) for i in rle])])


def write_nuclei_prob(src_dir, tgt_dir, prob_array):
    gen_nuclei_rle = config['post'].getboolean('generate_nuclei_rle')
    src_csv = os.path.join(src_dir, 'mask.csv')
    tgt_csv = os.path.join(tgt_dir, 'mask.csv')
    target = prob_to_segment(prob_array)
    if not os.path.isfile(src_csv):
        if gen_nuclei_rle:
            generate_target_nuclei(src_dir, prob_array)
        else:
            raise FileNotFoundError(f'{src_csv} not found!')

    df = pd.read_csv(src_csv, index_col='ImageId')
    df['TumorProb'] = 0.
    for row in df.itertuples():
        rle = row.EncodedPixels
        if not isinstance(rle, str):
            continue
        obj = rle_decode(rle, target.shape)
        overlap = target & obj
        if overlap.sum() and ((overlap.sum() / obj.sum()) > 0.5):
            rows, cols = np.nonzero(overlap)
            prob = np.mean(prob_array[rows, cols])
            df.at[row.Index, 'TumorProb'] = prob
    df.to_csv(tgt_csv)

# copy from https://github.com/pytorch/examples/blob/master/imagenet/main.py#L139
class AverageMeter():
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

# copy from https://www.kaggle.com/aglotero/another-iou-metric
# y_pred & labels are all 'labelled' numpy arrays
def iou_metric(y_pred, labels, print_table=False):
    true_objects = len(np.unique(labels))
    pred_objects = len(np.unique(y_pred))

    intersection = np.histogram2d(labels.flatten(), y_pred.flatten(), bins=(true_objects, pred_objects))[0]

    # Compute areas (needed for finding the union between all objects)
    area_true = np.histogram(labels, bins = true_objects)[0]
    area_pred = np.histogram(y_pred, bins = pred_objects)[0]
    area_true = np.expand_dims(area_true, -1)
    area_pred = np.expand_dims(area_pred, 0)

    # Compute union
    union = area_true + area_pred - intersection

    # Exclude background from the analysis
    intersection = intersection[1:,1:]
    union = union[1:,1:]
    union[union == 0] = 1e-9

    # Compute the intersection over union
    iou = intersection / union

    # Precision helper function
    def precision_at(threshold, iou):
        matches = iou > threshold
        true_positives = np.sum(matches, axis=1) == 1   # Correct objects
        false_positives = np.sum(matches, axis=0) == 0  # Missed objects
        false_negatives = np.sum(matches, axis=1) == 0  # Extra objects
        tp, fp, fn = np.sum(true_positives), np.sum(false_positives), np.sum(false_negatives)
        return tp, fp, fn

    # Loop over IoU thresholds
    prec = []
    if print_table:
        print("\nThresh\tTP\tFP\tFN\tPrec.")
    for t in np.arange(0.5, 1.0, 0.05):
        tp, fp, fn = precision_at(t, iou)
        if (tp + fp + fn) > 0:
            p = tp / (tp + fp + fn)
        else:
            p = 0
        if print_table:
            print("{:1.3f}\t{}\t{}\t{}\t{:1.3f}".format(t, tp, fp, fn, p))
        prec.append(p)

    if print_table:
        print("AP\t-\t-\t-\t{:1.3f}".format(np.mean(prec)))
    return np.mean(prec)

def iou_mean(y_pred_in, y_true_in):
    y_pred_in = y_pred_in.to('cpu').detach().numpy()
    y_true_in = y_true_in.to('cpu').detach().numpy()
    batch_size = y_true_in.shape[0]
    metric = []
    for idx in range(batch_size):
        y_pred = label(y_pred_in[idx])
        y_true = label(y_true_in[idx] > 0)
        value = iou_metric(y_pred, y_true)
        metric.append(value)
    return np.mean(metric)

# checkpoint handling
def check_ckpt_dir():
    checkpoint_dir = os.path.join('.', 'checkpoint')
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

def ckpt_path(epoch=None):
    check_ckpt_dir()
    current_path = os.path.join('.', 'checkpoint', 'current.json')
    if epoch is None:
        if os.path.exists(current_path):
            with open(current_path) as infile:
                data = json.load(infile)
                epoch = data['epoch']
        else:
            return ''
    else:
        with open(current_path, 'w') as outfile:
            json.dump({
                'epoch': epoch
            }, outfile)
    return os.path.join('.', 'checkpoint', '{}.dat'.format(epoch))

def is_best_ckpt(epoch, iou_tr, iou_cv):
    check_ckpt_dir()
    best_json = os.path.join('.', 'checkpoint', 'best.json')
    best_iou_cv = best_iou_tr = 0
    if os.path.exists(best_json):
        with open(best_json) as infile:
            data = json.load(infile)
            best_iou_cv = data['iou_cv']
            best_iou_tr = data['iou_tr']
    best_iou_tr = max(0.35, best_iou_tr) # only save best checkpoint above certain IoU
    cv_threshold = 0.01 # tolerance of degraded CV IoU
    if iou_tr > best_iou_tr and iou_cv > best_iou_cv - cv_threshold:
        with open(best_json, 'w') as outfile:
            json.dump({
                'epoch': epoch,
                'iou_tr': iou_tr,
                'iou_cv': iou_cv,
            }, outfile)
        return True
    return False

# DataParallel will change model's class name to 'dataparallel' & prefix 'module.' to existing parameters.
# Here the saved checkpoint might or might not be 'DataParallel' model (e.g. might be trained with multi-GPUs or single GPU),
# handle this variation while loading checkpoint.
# Refer to:
#   https://github.com/pytorch/pytorch/issues/4361
#   https://github.com/pytorch/pytorch/issues/3805
#   https://stackoverflow.com/questions/44230907/keyerror-unexpected-key-module-encoder-embedding-weight-in-state-dict
def _extract_state_from_dataparallel(checkpoint_dict):
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in checkpoint_dict.items():
        if k.startswith('module.'):
            name = k[7:] # remove 'module.'
        else:
            name = k
        new_state_dict[name] = v
    return new_state_dict

def save_ckpt(model, optimizer, epoch, iou_tr, iou_cv):
    def do_save(filepath):
        torch.save({
            'epoch': epoch,
            'name': config['ctc_detector']['model'],
            'model': model.state_dict(),
            'optimizer': optimizer.state_dict(),
        }, filepath)
    # check if best checkpoint
    if is_best_ckpt(epoch, iou_tr, iou_cv):
        filepath = os.path.join('.', 'checkpoint', 'best.dat')
        do_save(filepath)
    # save checkpoint per n epoch
    n_ckpt_epoch = config['train'].getint('n_ckpt_epoch')
    if epoch % n_ckpt_epoch == 0:
        filepath = ckpt_path(epoch)
        do_save(filepath)

def load_ckpt(model=None, optimizer=None, filepath=None):
    if filepath is None:
        filepath = ckpt_path()
    if not os.path.isfile(filepath):
        return 0 if model else (None, '')
    print("Loading checkpoint '{}'".format(filepath))
    if torch.cuda.is_available():
        # Load all tensors onto previous state
        checkpoint = torch.load(filepath)
    else:
        # Load all tensors onto the CPU
        checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
    if optimizer:
        try:
            optimizer.load_state_dict(checkpoint['optimizer'])
        except ValueError as err:
            print('[WARNING]', err)
            print('[WARNING] optimizer not restored from last checkpoint, continue without previous state')
    if model:
        model.load_state_dict(_extract_state_from_dataparallel(checkpoint['model']))
        return checkpoint['epoch']
    else:
        # build model based on checkpoint
        from .model import build_model
        assert 'name' in checkpoint, "Abort! No model name in checkpoint, use ckpt.py to convert first"
        model_name = checkpoint['name']
        model = build_model(model_name)
        model.load_state_dict(_extract_state_from_dataparallel(checkpoint['model']))
        return model, model_name

def freeze_ckpt(src, dest):
    model, model_name = load_ckpt(filepath=src)
    model.eval()
    for param in model.parameters():
        param.requires_grad = False
    torch.save({
        'copyright': '© 2018 AIxMed, Inc. All Rights Reserved',
        'name': model_name,
        'model': model.state_dict()
    }, dest)

def imshow(img, engine='plt'):
    """Show image on screen.Ddebug purpose only, do not use in non-GUI environment
    """
    if isinstance(img, Image.Image):
        # is PIL image, use pil mode directly
        return img.show()

    if torch.is_tensor(img):
        from . import transform as tx
        transform = tx.Compose([
            tx.DeNormalize(),
            tx.ToNumpy()
        ])
        if img.ndimension() == 4:
            # only dislay first sample
            img = img[0]
        img, _ = transform(img)

    assert isinstance(img, np.ndarray) and (img.ndim in {2, 3})

    if engine == 'plt':
        try:
            import matplotlib
            import matplotlib.pyplot as plt
        except ImportError as err:
            print("[WARN] No GUI library for rendering, switch to pil mode")
            engine = 'pil'

    if engine == 'pil':
        if img.dtype in [np.float32, np.float64]:
            img = (a * 255).astype(np.uint8)
        return Image.fromarray(img).show()
    elif engine == 'plt':
        # draw figure immediately and keep alive until you close the figures
        matplotlib.interactive(True)
        fig = plt.figure()
        cmap = None
        if img.ndim == 2 or img.dtype == np.bool:
            cmap = 'gray'
        return plt.imshow(img, cmap)
    else:
        raise ValueError(f'engine type {engine} invalid')
