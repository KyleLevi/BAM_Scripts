#!/usr/bin/env python3

import os
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File',)
    parser.add_argument('-o', '--output', help='Output File')


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.input:
        args.input = 'Output/protein_hits.csv'
    if not args.output:
        args.output = 'Output/hits_by_organism.csv'


    organisms = {}
    with open(args.input) as infile:
        if '\t' in infile.readline():
            delim = '\t'
        else:
            delim = ','
        for line in infile:
            line=line.replace('\n', '').split(delim)
            organisms[line[1]] = organisms.get(line[1], 0) + int(line[2])
    with open(args.output, 'w') as outfile:
        for k in sorted(organisms, key=organisms.get, reverse=True):
            outfile.write(delim.join([str(k),str(organisms[k])]) + '\n')
