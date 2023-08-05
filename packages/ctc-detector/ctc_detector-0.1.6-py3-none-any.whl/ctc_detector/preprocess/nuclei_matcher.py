import numpy as np
import pandas as pd
import os
import json
import argparse
from skimage.io import imread
from torch.multiprocessing import Pool, get_context
from tqdm import tqdm


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

def read_metadata(path):
    fp = os.path.join(path, 'meta.json')
    if not os.path.exists(fp):
        return {}
    with open(fp) as f:
        data = json.load(f)
        return data

def parallel_processing_with_progress(func, data):
    with get_context("spawn").Pool() as p:
        with tqdm(total=len(data)) as pbar:
            for result in tqdm(p.imap_unordered(func, data)):
                yield result
                pbar.update()

def match_nuclei(sample_dir):
    grids = next(os.walk(sample_dir))[1]  # immediate child directories
    grid_dirs = [os.path.join(sample_dir, idx) for idx in grids]
    for _ in parallel_processing_with_progress(match_grid_nuclei, grid_dirs): pass

def match_grid_nuclei(grid_dir):
    metadata = read_metadata(grid_dir)
    if metadata:
        grid_id = os.path.basename(os.path.normpath(grid_dir)) # retrieve the last part of grid_dir
        img = imread(os.path.join(grid_dir, 'images', f'{grid_id}_DAPI.png'))
        centroids = metadata['centroid'] if metadata else None
        target_mask = np.full(img.shape, False)
        for y, x in centroids:
            target_mask[y][x] = True

        fp = os.path.join(grid_dir, 'mask.csv')
        df = pd.read_csv(fp, index_col='ImageId')
        if 'Label' not in df.columns:
            df['Label'] = ''
        for row in df.itertuples():
            rle = row.EncodedPixels
            if not isinstance(rle, str):
                continue
            obj = rle_decode(rle, img.shape)
            if np.any(target_mask & obj):
                df.at[row.Index, 'Label'] = 'ctc'
        df.to_csv(fp)  # overwrite mask.csv

def entry_wrapper(input_dir):
    if not os.path.exists(input_dir):
        raise IOError(f'{input_dir} not exist!')

    samples = [os.path.join(input_dir, s) for s in os.listdir(input_dir)
              if os.path.isdir(os.path.join(input_dir, s))]
    print(f'Starting process input directory: {input_dir}')
    for sample in samples:
        print(f'Processing sample directory: {sample}')
        match_nuclei(sample)
    print('Completed!')

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='match_label'
    )
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    required.add_argument('--input_dir', type=str, help='root directory of examples, which contain cropped images & metadata', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['input_dir'])