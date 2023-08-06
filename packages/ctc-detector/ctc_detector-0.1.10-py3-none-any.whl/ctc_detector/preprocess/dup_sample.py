import os
import shutil
import csv
import argparse


def entry_wrapper(duplist, src_dir, dest_dir):
    if not os.path.isfile(duplist):
        raise IOError(f'{duplist} not exist!')
    if not os.path.exists(src_dir):
        raise IOError(f'{src_dir} not exist!')
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(duplist, 'r') as f:
        reader = csv.reader(f)
        samples = [s[0] for s in reader]

    for sample in samples:
        shutil.copytree(os.path.join(src_dir, sample), os.path.join(dest_dir, sample))
    print('\nCompleted!')

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='dup_sample'
    )
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    required.add_argument('--list', type=str, help='file contains samples to be duplicated, one sample per line', required=True)
    required.add_argument('--src_dir', type=str, help='source directory of samples to be duplicated', required=True)
    required.add_argument('--dest_dir', type=str, help='destination directory of duplicated samples', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['list'], args['src_dir'], args['dest_dir'])

if __name__ == '__main__':
    main()