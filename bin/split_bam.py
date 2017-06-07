import sys
import argparse
import os
import pysam

def splitSam(infile, MIN_LEN, OUTDIR):
    #Read and open in the right type, sam or bam
    if infile.endswith('.sam'):
        readtype = 'r'
    elif infile.endswith('.bam'):
        readtype = 'rb'
    else:
        sys.stderr.write('infile %s does not end with .sam or .bam, trying as samfile...' % infile)
        readtype = 'r'
    try:
        samfile = pysam.AlignmentFile(infile, readtype)
    except:
        sys.stderr.write('infile %s could not be opened by pysam, check that it is a samfile or bamfile' % infile)
        return

    #Group reads by who they matched to
    refnames = {}
    #[1-3]
    i = 0 #counts total reads
    reads = samfile.fetch()
    for read in reads:
        i+=1
        refname = read.reference_name
        if refname not in refnames:
            refnames[refname] = []
        refnames[refname].append(read)
    if i == 0:
        return

    #Write oufiles
    if OUTDIR:
        if not OUTDIR.endswith('/'):
            directory = OUTDIR + '/'
        else:
            directory = OUTDIR
    else:
        directory = ''.join(infile.split('/')[:-1])

    filename = infile.split('/')[-1]
    run_acc = filename.split('.')[0]
    type = filename.split('.')[1]
    for k,v in refnames.iteritems():
        if MIN_LEN > 0:
            outstring = '{0}{1}.{2}.L{3}.{4}'.format(directory,run_acc,k,MIN_LEN,type)
        else:
            outstring = '{0}{1}.{2}.{3}'.format(directory,run_acc,k,type)

        if readtype == 'rb':
            outfile = pysam.AlignmentFile(outstring, 'wb', template=samfile)
        else:
            outfile = pysam.AlignmentFile(outstring, 'w', template=samfile)
        for read in v:
            x, y = read.get_cigar_stats()
            if x[0] >= MIN_LEN:
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
        sys.exit(0)
    if not args.l:
       args.l = 0


    splitSam(args.i, args.l, args.o)