#!/usr/bin/env python3

import sys
import os
import argparse
from m8_reader import M8_Reader





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Output DIRECTORY')

    parser.add_argument('-n', help='Some Number', type=int)
    parser.add_argument('-v', help='Verbose', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    if not args.output.endswith('/') and len(args.output) != 0:
        args.output = args.output + '/'
    data = M8_Reader(args.input)
    for pp in data.protein_pilups():
        outfile = open(args.output + pp.protein + '.csv', 'w')
        for idx, dict in enumerate(pp.positions):
            try:
                consensus = max(dict, key=dict.get)
            except:
                consensus = '-'
            total = sum(dict.values())
            spread = {k:(round(v/total, 3)) for k,v in dict.items()}
            line = [idx, sum(dict.values()),consensus, '\t'.join([str(((l,spread[l]))).replace(',', '') for l in sorted(spread, key=spread.get, reverse=True)])]
            line = [str(x) for x in line]
            outfile.write('\t'.join(line))
            outfile.write('\n')
        outfile.close()
