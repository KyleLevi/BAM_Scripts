import argparse
import pysam
import os
import sys
import subprocess

def sam_stats(infile, csvoutfile = None):
    subprocess.call(["samtools", "view", "-bS", infile, "|" "samtools", "sort", "-", infile],
                    stdout=open(infile.replace('.sam', '') + '.bam', 'w'))
    print('.done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Takes in a BAM file or directory containing BAM files and outputs 1 - the conservation'
                    'of each base in the genome.  The default format is a CSV file for a heatmap, and '
                    '-f can be used to create a full CSV with detailed informaion about each position')
    parser.add_argument('--input', '-i', help='Input file', required=True)
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--number-splits', '-n', help='Number of sections to group the genome into.'
                                   'Anything over 500 may not show up well in a heatmap.', type=int)
    parser.add_argument('--full', '-f', help='Output the full base distribution (to view in a spreadsheet)'
                                   'and not just the CSV for a heatmap', action="store_true")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    sam_stats(args.input)


