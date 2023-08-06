from statsfiles import statsfiles
import argparse


parser = argparse.ArgumentParser(description='Do the stats of files.')
parser.add_argument('iter_start',  type=int,
                    help='iteration start for the stats')

parser.add_argument('--afm', action='store_const', const=True,
                    help='afm is present')

args = parser.parse_args()

statsfiles.run_statsfiles(args.iter_start, args.afm)
