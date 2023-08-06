# python built-in library
import os
import argparse
import time
from multiprocessing import Manager
# 3rd party library
import numpy as np
import torch
import torch.nn as nn
from torch.nn.utils import clip_grad_norm
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
# own code
from .config import config
from .model import build_model
from .dataset import CTCDataset
from . import transform as tx
from .helper import AverageMeter, iou_mean, prob_to_segment, save_ckpt, load_ckpt
from .loss import focal_criterion

def run(resume=True, n_epoch=None, learn_rate=None):
    model_name = config['ctc_detector']['model']
    if learn_rate is None:
        learn_rate = config['ctc_detector'].getfloat('learn_rate')
    width = config.getint(model_name, 'width')
    # weight_map = config['ctc_detector'].getboolean('weight_map')
    c = config['train']
    log_name = c.get('log_name')
    n_batch = c.getint('n_batch')
    n_worker = c.getint('n_worker')
    n_cv_epoch = c.getint('n_cv_epoch')
    if n_epoch is None:
        n_epoch = c.getint('n_epoch')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = build_model(model_name)
    model = model.to(device)

    # define optimizer
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=learn_rate,
        weight_decay=1e-6
        )

    # dataloader workers are forked process thus we need a IPC manager to keep cache in same memory space
    manager = Manager()
    cache = manager.dict()
    transform = tx.Compose([
        tx.RandomScale(scale=(0.5, 1.5)),
        tx.RandomUniformCrop(size=width),
        tx.RandomVerticalFlip(),
        tx.RandomHorizontalFlip(),
        tx.RandomRotate(),
        tx.RandomNoise(p=0.5),
        tx.RandomGaussianBlur(p=0.5),
        tx.ElasticDistortion(alpha=300, sigma=30),
        tx.ToTensor(),
        tx.Normalize(),
    ])
    # prepare dataset, split train dataset as CV, aka. train-valid
    train_dataset = CTCDataset('data/train', transform, cache=cache)
    train_dataset, train_valid_dataset = train_dataset.split()
    test_valid_dataset = CTCDataset('data/valid', transform, cache=cache, policy='Once')
    # data loader
    def loader(ds):
        return DataLoader(
            ds,
            sampler=ds.sampler(),
            batch_size=n_batch,
            num_workers=n_worker,
            pin_memory=torch.cuda.is_available())
    train_loader = loader(train_dataset)
    train_valid_loader = loader(train_valid_dataset)
    test_valid_loader = loader(test_valid_dataset)

    # resume checkpoint
    start_epoch = iou_tr = iou_cv = 0
    if resume:
        start_epoch = load_ckpt(model, optimizer)
    if start_epoch == 0:
        print('Grand new training ...')

    # put model to GPU
    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = nn.DataParallel(model)

    # decide log directory name
    log_dir = os.path.join(
        'logs', log_name, '{}-{}'.format(model_name, width),
        'ep_{},{}-lr_{}'.format(
            start_epoch,
            n_epoch + start_epoch,
            learn_rate,
        )
    )

    with SummaryWriter(log_dir) as writer:
        if start_epoch == 0 and False:
            # dump graph only for very first training, disable by default
            dump_graph(model, writer, n_batch, width)
        print('Training started ...')
        for epoch in range(start_epoch + 1, n_epoch + start_epoch + 1): # 1 base
            iou_tr = iterate(train_loader, model, optimizer, epoch, writer)
            if epoch % n_cv_epoch == 0:
                with torch.no_grad():
                    iou_cv = iterate(train_valid_loader, model, optimizer, epoch, writer, 'CV_train')
                    _      = iterate(test_valid_loader , model, optimizer, epoch, writer, 'CV_test')
            save_ckpt(model, optimizer, epoch, iou_tr, iou_cv)
        print('Training finished ...')

def dump_graph(model, writer, n_batch, width):
    # Prerequisite
    # $ sudo apt-get install libprotobuf-dev protobuf-compiler
    # $ pip3 install onnx
    print('Dump model graph ...')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dummy_input = torch.rand(n_batch, 3, width, width, device=device)
    torch.onnx.export(model, dummy_input, "checkpoint/model.pb", verbose=False)
    writer.add_graph_onnx("checkpoint/model.pb")

def iterate(loader, model, optimizer, epoch, writer, mode='training'):
    losses = AverageMeter()
    iou = AverageMeter()   # semantic IoU
    print_freq = config['train'].getfloat('print_freq')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Sets the model in training/evaluation mode.
    if mode == 'training':
        model.train()
    else:
        model.eval()
    total = len(loader)
    for i, data in enumerate(loader):
        # split sample data
        inputs = data['image'].to(device)
        labels = data['label'].to(device)
        # splits label tensor into chunks, per channel, in shape [m, 1, h, w]
        assert labels.shape[1] == 2
        y, w = torch.chunk(labels, labels.shape[1], 1)
        if mode == 'training':
            # zero the parameter gradients
            optimizer.zero_grad()
        # zero the parameter gradients
        optimizer.zero_grad()
        # forward step
        y_hat = model(inputs)
        # compute loss
        # weight_criterion equals to segment_criterion if weights is none
        loss = focal_criterion(y_hat, y, weights=w)
        if mode == 'training':
            # compute gradient and do backward step
            loss.backward()
            # clip_grad_norm(model.parameters(), 2.0) # handle gradient explosion when needed
            optimizer.step()
        # measure accuracy and record loss
        losses.update(loss.item(), inputs.size(0))
        y_hat = prob_to_segment(y_hat)
        batch_iou = iou_mean(y_hat, y)
        iou.update(batch_iou, inputs.size(0))
        # console log current status
        if mode == 'training' and (i + 1) % print_freq == 0:
            print(
                'Epoch: [{0}][{1}/{2}]\t'
                'Loss: {loss.avg:.4f}\t'
                'IoU: {iou.avg:.3f}\t'
                .format(
                    epoch, i+1, total, loss=losses, iou=iou
                )
            )
    # end of loop
    # dump epoch summary
    print(
        'Epoch: [{0}]\t\t{1}\t\t'
        'Loss: {loss.avg:.4f}\t'
        'IoU: {iou.avg:.3f}\t'
        .format(epoch, mode, loss=losses, iou=iou)
    )
    writer.add_scalar(f'{mode}/epoch_loss', losses.avg, epoch)
    writer.add_scalar(f'{mode}/epoch_iou', iou.avg, epoch)
    return iou.avg # return epoch average iou

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='train'
    )
    parser.add_argument('--resume', dest='resume', action='store_true')
    parser.add_argument('--no-resume', dest='resume', action='store_false')
    parser.add_argument('--epoch', type=int, help='run number of epoch')
    parser.add_argument('--lr', type=float, dest='learn_rate', help='learning rate')
    parser.set_defaults(resume=True)
    args = parser.parse_args(args)
    run(args.resume, args.epoch, args.learn_rate)