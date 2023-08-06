from statsfiles import statsfiles
import argparse
import yaml
import pkg_resources


parser = argparse.ArgumentParser(
    description='Do the statistics of tabular like files.')

# positional arguments
parser.add_argument('iter_start',  type=int,
                    help='iteration start for performing the statistics.')


# optional arguments
parser.add_argument('--afm', action='store_const', const=True,
                    help='Antiferromagnetism is present')

# exclusive groupe, gives the file to use for the statistics
exclusive_group = parser.add_mutually_exclusive_group(required=True)
exclusive_group.add_argument('--cdh', action='store_const', const=True,
                             help='Files are from CTQMC of Charles-David Hébert.')
exclusive_group.add_argument('--patrick', action='store_const', const=True,
                             help='Files are from CTQMC of Patrick Sémon.')
exclusive_group.add_argument('-f', '--file',  type=str,
                             help='Specify the file to use.')

args = parser.parse_args()

# select the file to load
if args.cdh:
    cdh_file_path: str = "data/cdh_params.yml"
    yy_params = yaml.load(
        pkg_resources.resource_string(__name__, cdh_file_path))
elif args.patrick:
    patrick_file_path: str = "data/patrick_params.yml"
    yy_params = yaml.load(
        pkg_resources.resource_string(__name__, patrick_file_path))
else:
    with open(args.file, "r") as fin:
        yy_params = yaml.load(fin)

statsfiles.run_statsfiles(args.iter_start, yy_params)
