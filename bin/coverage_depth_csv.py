#!/usr/bin/env python3

import sys
import argparse
import os
import pysam
import math


def bam_coverage(infile):
    """
    Takes in a BAM/SAM file or directory containing multiple, and returns a list of how many times each
    position had any base found.
    :param infile: String, Can be a directory containing multiple BAM/SAM files or a single BAM/SAM file
    :return: List, each position is one less than the position in the genome
    """
    if not infile.endswith('.bam'):
        sys.stderr.write('{} does not end with .bam - skipping\n'.format(infile))

    base_depth = []
    try:
        bamfile = pysam.AlignmentFile(infile, 'rb')
    except Exception as e:
        sys.stderr.write(infile + ' Could not be read\n')
        sys.stderr.write(e)
        sys.exit(1)

    # Make the base_depth list
    for p in bamfile.pileup():
        for pilups in p.pileups:
            if pilups.query_position:
                if p.reference_pos >= len(base_depth):
                    while p.reference_pos >= len(base_depth):
                        base_depth.append(0)
                base_depth[p.reference_pos] += 1
    return base_depth

def condense_list(big_list, condense_size=100):
    """
    Condense a list into n elements by averaging. 
    :param big_list: List
    :param condense_size: Int, the size of the new list to be returned
    :return: 
    """
    size = len(big_list)
    chunk_size = int(math.ceil(float(size)/condense_size))  # math.ceil only returns ints in python 3+
    newlist = []
    chunk_size = int(chunk_size)
    for n in range(0, size, chunk_size):
        newlist.append(sum(big_list[n:n + chunk_size]) / chunk_size)
    return newlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a CSV file of coverage depth per BAM file.'
                    'Each new line in the CSV is a different BAM file and the X axis is coverage depth.')
    parser.add_argument('-i', '--input', help='Name of the input .sam or .bam file to be read', required=True)
    parser.add_argument('-n', '--number_splits', help='Condense the coverage depth into N sections, default is 100', type=int)
    parser.add_argument('-o', '--output', help='CSV file to be appended or written', type=str, required=True)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.number_splits:
        args.number_splits = 100
    if args.output.endswith('.csv'):
        args.output = args.output.replace('.csv', '')

    # If input is a directory, do all the .bam files, otherwise just do the one file
    if args.input.endswith('/'):
        outstrings = []
        row_labels = []
        for f in os.listdir(args.input):
            if not f.endswith('.bam'):
                continue
            row_labels.append(f)
            x = bam_coverage(args.input + f)
            if len(x) < 1:
                continue
            outstrings.append(map(str, condense_list(x, args.number_splits)))
        with open(args.output + '.csv', 'w') as outfile:
            for s in outstrings:
                outfile.write(','.join(s))
                outfile.write('\n')
        with open(args.output + '.row_labels.txt', 'w') as outfile:
            for s in row_labels:
                outfile.write(s + '\n')
    else:  # Single BAM file, not a directory
        x = bam_coverage(args.input)
        x = map(str, condense_list(x, args.number_splits))
        with open(args.output + '.csv', 'a') as outfile:
            outfile.write(','.join(x) + '\n')
        with open(args.output + '.row_labels.txt', 'a') as outfile:
            outfile.write(args.output + '\n')
    sys.exit(0)
