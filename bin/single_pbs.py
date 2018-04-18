import sys
import os
import argparse
from BAM_Scripts.bin.sam_stats import Sam_Reader



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Output File', required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    data = Sam_Reader(args.input)
    data.per_base_stats(write_file=args.output)