import sys
import argparse
import pysam


def split_sam(infile, minimum_match_length, out_directory):
    """
    Splits a SAM or BAM file containing matches to multiple organisms into separate files for each organism using pysam.
    :param infile:  The path and filename  Ex: ~/Desktop/SRR3403834.sam
    :param minimum_match_length:  Ignore any matches less than this length  EX: 50
    :param out_directory:  New files will be written to this directory  EX: ~/Desktop/split_samfiles/
    :return:  None
    """

    # Read and open in the right type, sam or bam
    if infile.endswith('.sam'):
        readtype = 'r'
    elif infile.endswith('.bam'):
        readtype = 'rb'
    else:
        sys.stderr.write('infile %s does not end with .sam or .bam, trying as samfile...' % infile)
        readtype = 'r'
    try:
        samfile = pysam.AlignmentFile(infile, readtype)
    except Exception as e:
        sys.stderr.write('Input file {} could not be opened by pysam, exiting.\n{}\n'.format(infile, e))
        return

    refnames = {}
    i = 0  # counts total reads
    for read in samfile.fetch():
        i += 1
        refname = read.reference_name
        if refname not in refnames:
            refnames[refname] = []
        refnames[refname].append(read)
    if i == 0:
        sys.stderr.write('Input file {} is empty, no new files will be written.\n'.format(infile))
        return

    #  Write oufiles
    if out_directory:
        if not out_directory.endswith('/'):
            directory = out_directory + '/'
        else:
            directory = out_directory
    else:
        directory = ''.join(infile.split('/')[:-1])

    filename = infile.split('/')[-1]
    run_acc = filename.split('.')[0]
    ftype = filename.split('.')[1]
    for k, v in refnames.items():  # Switched from .iteritems() to .items() for Python 3
        if minimum_match_length > 0:
            outstring = '{0}{1}.{2}.L{3}.{4}'.format(directory, run_acc, k, minimum_match_length, ftype)
        else:
            outstring = '{0}{1}.{2}.{3}'.format(directory, run_acc, k, ftype)

        if readtype == 'rb':
            outfile = pysam.AlignmentFile(outstring, 'wb', template=samfile)
        else:
            outfile = pysam.AlignmentFile(outstring, 'w', template=samfile)
        for read in v:
            x, y = read.get_cigar_stats()
            if x[0] >= minimum_match_length:
                outfile.write(read)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Split a sam or bamfile containing matches from multiple genomes into separate sam or bam files')
    parser.add_argument('-i', help='Name of the input .sam or .bam file to be read', required=True)
    parser.add_argument('-l', help='Optional to remove any matched reads less than __ bp, default is 0', type=int)
    parser.add_argument('-o', help='Optional directory for outfiles, default is same directory', type=str)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.l:
        args.l = 0

    split_sam(args.i, args.l, args.o)