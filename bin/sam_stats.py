import argparse
import pysam
import os
import sys
import subprocess

def sam_to_bam(infile, outdir = None):
    """
    Converts a SAM file to a BAM file, sorts it, and Indexes it.
    :param infile:
    :param outdir:
    :return:
    """

    if infile.endswith('.sam'):
        # Changing the output file name and location
        bamfile = infile.replace('.sam', '.bam')
        if outdir:
            infile = infile.split('/')[-1].replace('.sam', '')
            bamfile = outdir + infile + '.bam'

        # These are the commands to be run, edit them here!
        commands = [["samtools", "view", "-bS", infile],
                    ["samtools", "sort", bamfile, bamfile.replace('.bam', '')],
                    ["samtools", "index", bamfile, bamfile.replace('.bam', '')]]

        for command in commands:
            ret_code = subprocess.call(["samtools", "view", "-bS", infile], stdout=open(bamfile, 'w'))
            if ret_code != 0:
                print("Error running command \"{}\"\n".format(' '.join(command)))
                return
        return bamfile

    else:
        print('File: "{}" does not end with .sam, cannot convert to .bam'.format(infile))
        return




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

    if args.input.endswith('/'):
        for f in os.listdir(args.input):
            if not f.endswith('.sam'):
                continue
            sam_stats(args.input + f)


