import sys
import argparse
import os
import pysam
import math


def bam_coverage(infile, size, split_size=100):
    chunk_size = int(math.ceil(float(size)/split_size))  # math.ceil only returns ints in python 3+
    if not infile.endswith('.bam'):
        sys.stderr.write('{} does not end with .bam - skipping\n'.format(infile))

    basedepth = [0] * size
    try:
        bamfile = pysam.AlignmentFile(infile, 'rb')
    except Exception as e:
        sys.stderr.write(infile + ' Could not be read\n')
        sys.stderr.write(e)
        sys.exit(1)

    # Make the basedepth list
    for p in bamfile.pileup():
        for pilups in p.pileups:
            if pilups.query_position:
                basedepth[p.reference_pos] += 1

    # Condense the list into <splitSize> many chunks
    newlist = []
    chunk_size = int(chunk_size)
    for n in range(0, size, chunk_size):
        newlist.append(sum(basedepth[n:n + chunk_size]) / chunk_size)
    return newlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a CSV file of coverage depth per BAM file.'
                    'Each new line in the CSV is a different BAM file and the X axis is coverage depth.')
    parser.add_argument('-i', help='Name of the input .sam or .bam file to be read', required=True)
    parser.add_argument('-l', help='Length of the genome', type=int, required=True)
    parser.add_argument('-n', help='Condense the coverage depth into N sections, default is 100', type=int)
    parser.add_argument('-o', help='CSV file to be appended or written', type=str, required=True)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.n:
        args.n = 100
    if args.o.endswith('.csv'):
        args.o = args.o.replace('.csv', '')

    # If input is a directory, do all the .bam files, otherwise just do the one file
    if args.i.endswith('/'):
        outstrings = []
        row_labels = []
        for f in os.listdir(args.i):
            if not f.endswith('.bam'):
                continue
            row_labels.append(f)
            outstrings.append(map(str, bam_coverage(args.i + f, args.l, args.n)))
        with open(args.o + '.csv', 'w') as outfile:
            for s in outstrings:
                outfile.write(','.join(s))
                outfile.write('\n')
        with open(args.o + '.row_labels.txt', 'w') as outfile:
            for s in row_labels:
                outfile.write(s + '\n')
    else:  # Single BAM file, not a directory
        x = map(str, bam_coverage(args.i, args.l, args.n))
        with open(args.o + '.csv', 'a') as outfile:
            outfile.write(','.join(x) + '\n')
        with open(args.o + '.row_labels.txt', 'a') as outfile:
            outfile.write(args.o + '\n')
    sys.exit(0)