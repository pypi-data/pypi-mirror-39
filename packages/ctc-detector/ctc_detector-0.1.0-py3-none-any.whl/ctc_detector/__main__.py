from . import __version__
import argparse

class Subcmd:
    def __init__(self, func, help=''):
        self.func = func
        self.help = help

subcmd = {}

from .preprocess import etl_zip
from .preprocess import nikon_processor
from .preprocess import nuclei_matcher
from .preprocess import crop_cell
from . import train, valid, stat, dataset
subcmd['etl_zip'] = Subcmd(etl_zip.main, 'extract and convert zip content into data folder')
subcmd['etl_nis'] = Subcmd(nikon_processor.main, 'process nikon nis content for viewer and model inference')
subcmd['train'] = Subcmd(train.main, 'train ctc nuclei detector')
subcmd['inference'] = Subcmd(valid.main, 'predict ctc nuclei')
subcmd['stat'] = Subcmd(stat.main, 'measure prediction statistics')
subcmd['match_label'] = Subcmd(nuclei_matcher.main, 'auto-match initial labels based on existing labels (centroids)')
subcmd['insp_data'] = Subcmd(dataset.main, 'inspect data and label in original and augmented forms')
subcmd['crop_cell'] = Subcmd(crop_cell.main, 'crop cell based on heuristic rule')

# init main parser
parser = argparse.ArgumentParser(
    prog='ctc_detector',
    formatter_class = argparse.RawTextHelpFormatter
)

# generate subcommand help message
subcmd_help_text = '\n'
max_cmd_length = max([len(x) for x in subcmd.keys()])
for cmd in sorted(subcmd):
    subcmd_help_text += cmd.ljust(max_cmd_length+2)
    subcmd_help_text += subcmd[cmd].help
    subcmd_help_text += '\n'

# insert subcommand as argument
parser.add_argument('-v', '--version',action='store_true',help='Print current package version')
parser.add_argument('cmd',choices=subcmd.keys(),help=subcmd_help_text,metavar='',nargs='?')
parser.add_argument('cargs',nargs=argparse.REMAINDER,help=argparse.SUPPRESS)

# parse argument and invoke subcommand
args = parser.parse_args()
#print args
if args.version:
    print('Version:', __version__)
elif args.cmd is None:
    parser.print_help()
else:
    subcmd[args.cmd].func(args.cargs)