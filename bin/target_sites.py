#!/usr/bin/env python3

import argparse
import sys
import operator
from functools import reduce
from conserved_regions_csv import bam_base_distribution


def score(conservation):
    """
    This is the scoring function for sequences, right now it is just the multiplied
    conservation of every base in the sequence.  Change this function for custom scoring.
    """
    return reduce(lambda x, y: x*y, conservation)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Directory containing bamfiles.')
    parser.add_argument('-l', '--length', help='The length of the sequence to be found.', required=True, type=int)
    parser.add_argument('-n', '--num-seqs', help='The top N sequences you want returned.  Default is 50 sequences', type = int)
    parser.add_argument('-d', '--depth', help='Exclude sites with less than -d coverage depth.  Default is 10', type = int)
    parser.add_argument('-s', '--start', help='Exclude sites that start before the -s value.  Default is 0', type = int)
    parser.add_argument('-e', '--end', help='Exclude sites that start after the -e value.  Default is 0', type = int)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.start:
        args.start = 0

    if not args.num_seqs:
        args.num_seqs = 50
    if not args.depth:
        args.depth = 10

    base_lists = bam_base_distribution(args.input)
    conservation_list = [float(max(base_list.values()))/sum(base_list.values()) if sum(base_list.values()) > 0 else 0 for base_list in base_lists]
    depth_list = [sum(base_list.values()) for base_list in base_lists]
    consensus_genome = [max(base_list.iteritems(), key=operator.itemgetter(1))[0] if len(base_list) > 0 else "-" for base_list in base_lists]
    score_list = []
    if not args.end:
        args.end = len(depth_list)
    for i in range(args.start, args.end - args.length):
        if min(depth_list[i:i+args.length]) < args.depth:
            score_list.append(-1)
        else:
            score_list.append(score(conservation_list[i:i+args.length]))

    # sorted_scores is a sorted list of tuples [(.999, 100), (.998, 504)...]
    # The first value is the score, the second is the original position in the list (1 less than the genome position)
    sorted_scores = sorted(((e, i) for i, e in enumerate(score_list)), reverse=True)

    for i in range(0, args.num_seqs):
        loc = sorted_scores[i][1]
        print(">Position_{0} [multiplied_conservation={1}] [avg_coverage_depth={2}]\n{3}\n".format(loc, sorted_scores[i][0], sum(depth_list[loc:loc+args.length])/args.length, ''.join(consensus_genome[loc:loc+args.length])))


