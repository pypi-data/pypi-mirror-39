import numpy as np
import pandas as pd
import os
import argparse
from skimage.io import imread
from torch.multiprocessing import Pool, get_context
from tqdm import tqdm
from ctc_detector.helper import image_picker

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

def parallel_processing_with_progress(func, data):
    with get_context("spawn").Pool() as p:
        with tqdm(total=len(data)) as pbar:
            for result in tqdm(p.imap_unordered(func, data)):
                yield result
                pbar.update()

# sample level
def migrate_label(src_sample, tgt_sample):
    grids = next(os.walk(tgt_sample))[1]  # immediate child directories
    grid_dirs = [(os.path.join(src_sample, idx), os.path.join(tgt_sample, idx)) for idx in grids]
    stats = []
    for result in parallel_processing_with_progress(migrate_grid_label, grid_dirs):
        stats.extend(result)
    for stat in stats:
        print(stat)

# grid level
def migrate_grid_label(grid_dir):
    src_grid_dir, tgt_grid_dir = grid_dir
    fp = image_picker(src_grid_dir, '')
    if not fp:
        raise FileNotFoundError(f"DAPI image not found! ({src_grid_dir})")
    img = imread(fp)
    shape = img.shape
    src_csv = os.path.join(src_grid_dir, 'mask.csv')
    tgt_csv = os.path.join(tgt_grid_dir, 'mask.csv')
    src_df = pd.read_csv(src_csv, index_col='ImageId', dtype={'Label': str})
    tgt_df = pd.read_csv(tgt_csv, index_col='ImageId', dtype={'Label': str})
    if 'Label' not in src_df.columns:
        #print(f'No label in {src_csv}!')
        return []
    if 'Label' not in tgt_df.columns:
        tgt_df['Label'] = ''

    src_df = src_df.loc[src_df['Label'] == 'ctc']
    src_df['MigrateLevel'] = 'low_confidence'
    for r in src_df.itertuples():
        rle = r.EncodedPixels
        if not isinstance(rle, str):
            continue
        obj = rle_decode(rle, shape)
        for r2 in tgt_df.itertuples():
            rle = r2.EncodedPixels
            if not isinstance(rle, str):
                continue
            obj2 = rle_decode(rle, shape)
            overlap = (obj & obj2).sum()
            if overlap:
                tgt_df.at[r2.Index, 'Label'] = 'ctc'
                if ((overlap / obj.sum()) > 0.5) and ((overlap / obj2.sum()) > 0.5):
                    src_df.at[r.Index, 'MigrateLevel'] = 'high_confidence'
                else:
                    # print(f"MED: {src_df.loc[r.Index, 'MigrateLevel']}")
                    if src_df.loc[r.Index, 'MigrateLevel'] == 'low_confidence':
                        src_df.at[r.Index, 'MigrateLevel'] = 'medium_confidence'

    # append non-matched/overlapped existing labels to target maskcsv?
    df = src_df.loc[src_df['MigrateLevel'] == 'low_confidence']
    missed = [[f'{r.Index}_migrate', r.EncodedPixels, 'ctc'] for r in df.itertuples()]
    if missed:
        df = pd.DataFrame(missed, columns=['ImageId', 'EncodedPixels', 'Label'])
        df = df.set_index('ImageId')
        tgt_df = pd.concat([tgt_df, df], axis=0)
    tgt_df.to_csv(tgt_csv)

    df = src_df.groupby('MigrateLevel').size().to_frame('count')
    stat = [(tgt_grid_dir, r.Index, r.count) for r in df.itertuples()]
    return stat

def entry_wrapper(src_root, tgt_root):
    if not os.path.exists(src_root):
        raise IOError(f'{src_root} not exist!')
    if not os.path.exists(tgt_root):
        raise IOError(f'{tgt_root} not exist!')

    samples = [os.path.join(tgt_root, s) for s in os.listdir(tgt_root)
              if os.path.isdir(os.path.join(tgt_root, s))]
    for tgt_sample in samples:
        print(f'Processing sample directory: {tgt_sample}')
        sample_id = os.path.relpath(tgt_sample, tgt_root)
        src_sample = os.path.join(src_root, sample_id)
        migrate_label(src_sample, tgt_sample)
    print('\nCompleted!')

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='migrate_label'
    )
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    required.add_argument('--src_root', type=str, help='root directory of examples, which contain labeled mask.csv', required=True)
    required.add_argument('--tgt_root', type=str, help='root directory of examples, which contain newer inferenced mask.csv', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['src_root'], args['tgt_root'])

if __name__ == '__main__':
    main()