import sys
import os
import argparse
from sam_stats import Sam_Reader


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Output File', required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    samfiles = Sam_Reader(args.input)
    samfiles.hits(write_file=args.output)