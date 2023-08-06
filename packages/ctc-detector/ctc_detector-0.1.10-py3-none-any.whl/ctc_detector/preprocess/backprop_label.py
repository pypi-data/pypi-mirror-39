import numpy as np
import pandas as pd
import os
import argparse
import re
from tqdm import tqdm


def backprop_csv(src_csv, dest_csv):
    src_df = pd.read_csv(src_csv, index_col='ImageId', dtype={'Label': str})
    dest_df = pd.read_csv(dest_csv, index_col='ImageId', dtype={'Label': str})
    if 'Label' not in src_df.columns:
        #print(f'No label in {src_csv}!')
        return
    if 'Label' not in dest_df.columns:
        dest_df['Label'] = ''

    src_df = src_df.loc[src_df['Label'] == 'ctc']
    print(f'backprop {len(src_df)} labels from {src_csv} to {dest_csv}')
    for r in src_df.itertuples():
        print(f'\tlabel {r.Index}')
        dest_df.at[r.Index, 'Label'] = 'ctc'
    dest_df.to_csv(dest_csv)


def entry_wrapper(crop_root, sample_root):
    if not os.path.exists(crop_root):
        raise IOError(f'{crop_root} not exist!')
    if not os.path.exists(sample_root):
        raise IOError(f'{sample_root} not exist!')

    crops = [os.path.join(crop_root, s) for s in os.listdir(crop_root)
              if os.path.isdir(os.path.join(crop_root, s))]
    for crop in sorted(crops):
        match = re.search(r'([A-Za-z0-9-_]*)_([0-9]_[0-9])_mask_[0-9]*_*', crop)
        if not match:
            raise ValueError(f'{crop} naming scheme is not compatible!')
        sample_id, tile_id = match[1], match[2]
        src_csv = os.path.join(crop, 'mask.csv')
        dest_csv = os.path.join(sample_root, sample_id, tile_id, 'mask.csv')
        backprop_csv(src_csv, dest_csv)
    print('\nCompleted!')

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='backprop_label'
    )
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    required.add_argument('--crop_root', type=str, help='root directory of cropped samples, which contain mask.csv with revised labels', required=True)
    required.add_argument('--sample_root', type=str, help='root directory of samples, which contain mask.csv to be merged', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['crop_root'], args['sample_root'])

if __name__ == '__main__':
    main()