import sys
import os
import argparse
from m8_reader import M8_Reader


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Output File')


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    header = ['File Name', 'Protein', '# Hits (evalue < .0001)', '\n']
    data = M8_Reader(args.input)
    if args.output:
        sys.stdout = open(args.output, 'w')
    sys.stdout.write('\t'.join(header))
    file_hits = data.hits()
    for f, hit_dict in file_hits.items():
        for prot in sorted(hit_dict, key=hit_dict.get, reverse=True):
            hits = hit_dict[prot]
            line = [f, prot, hits, '\n']
            line = [str(x) for x in line]
            sys.stdout.write('\t'.join(line))


