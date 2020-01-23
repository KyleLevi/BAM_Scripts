#!/usr/bin/env python3

import sys
import pysam
import argparse
import os
import time

def genome_coverage_dict(infile):
    """
    Creates a dictionary where keys are organism names, and values are the percent coverage of the genome from 0 to 1
    :param infile: Sorted and indexed BAM file
    :return: dictionary
    """
    if not infile.endswith('.bam'):
        sys.stderr.write('{} does not end with .bam - skipping\n'.format(infile))
        return
    try:
        bamfile = pysam.AlignmentFile(infile, 'rb')
    except Exception as e:
        sys.stderr.write(infile + ' Could not be read\n')
        sys.stderr.write(str(e))
        return

    # Get a dict of genome lengths from the header
    genome_lengths = {}
    for l, r in zip(bamfile.lengths, bamfile.references):
        genome_lengths[r] = l

    # Loop over every read, and calculate coverage an organism if it's the first read found
    organism_coverage = {}
    for read in bamfile.fetch():
        genome_name = read.reference_name
        if genome_name in organism_coverage:
            continue

        #Process one genome
        base_depth = []
        for p in bamfile.pileup(contig=genome_name):
            for pilups in p.pileups:
                if pilups.query_position:
                    #Expand array while insert pos is out of list bounds
                    if p.reference_pos >= len(base_depth):
                        while p.reference_pos >= len(base_depth):
                            base_depth.append(0)
                    base_depth[p.reference_pos] += 1

        bins_covered = len([x for x in base_depth if x > 0])
        organism_coverage[genome_name] = bins_covered/genome_lengths[genome_name]
    return organism_coverage


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Writes to standard out "Genome_Name\tPercent_Coverage" for each genome in a BAM file')
    parser.add_argument('-i', '--input', help='Name of the input .bam file to be read', required=True)
    parser.add_argument('-r', '--dir', help='Add this flag if input is a directory of BAM files', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    if not args.dir:
        x = genome_coverage_dict(args.input)
        if x:
            for k,v in x.items():
                sys.stdout.write('\t'.join([k,str(v),'\n']))
        else:
            sys.stdout.write('Everything worked with this script but the BAM file is empty :(')
    else:
        all_files = {}
        for fname in os.listdir(args.input):
            if fname.endswith('.bai'):
                continue
            all_files[fname] = genome_coverage_dict(args.input + fname)
        for fname, dict in all_files.items():
            sys.stdout.write(fname + '\n')
            if dict:
                for k,v in dict.items():
                    sys.stdout.write('\t'.join(['', k, str(v), '\n']))
            else:
                sys.stdout.write('\tEmpty\n')




















