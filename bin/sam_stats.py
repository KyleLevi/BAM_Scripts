import sys
import os
import argparse
import subprocess
import pysam

class Sam_Stats:

    def __init__(self, file_or_folder):
        """
        Initialize with the path to a file or a folder. If a file is
        :param file_or_folder:
        """
        if not os.isdir(file_or_folder):
            if file_or_folder.endswith('.sam'):
                file_or_folder = self.sam_to_bam(file_or_folder)
            input_files = [file_or_folder]
        else:
            # Get the names of every SAM and BAM file in the input dir
            input_files = [file_or_folder + file_name for file_name in os.listdir(file_or_folder) if
                           file_name.endswith(".sam") or file_name.endswith('.bam')]
            # Trim sam files from the list that have a bam file of the same name in the list
            input_files = [file_name for file_name in input_files if not
            (file_name.endswith('.sam') and file_name.replace('.sam','.bam') in input_files)]
            # Convert any sam files to bam files, sort, index and add the new file names to the input_files
            input_files = [file_name if file_name.endswith('.bam') else self.sam_to_bam(file_name) for file_name in input_files]

        self.input_files = input_files

    @staticmethod
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
            convert_to_bam = ["samtools", "view", "-bS", infile]
            sort_bamfile   = ["samtools", "sort", bamfile, bamfile.replace('.bam', '')]
            index_bamfile  = ["samtools", "index", bamfile, bamfile.replace('.bam', '')]

            ret_code = subprocess.call(convert_to_bam, stdout=open(bamfile, 'w'))
            if ret_code != 0:
                sys.stderr.write("Error running command \"{}\"\n".format(' '.join(convert_to_bam)))
                return None
            ret_code = subprocess.call(sort_bamfile)
            if ret_code != 0:
                sys.stderr.write("Error running command \"{}\"\n".format(' '.join(sort_bamfile)))
                return None
            ret_code = subprocess.call(index_bamfile)
            if ret_code != 0:
                sys.stderr.write("Error running command \"{}\"\n".format(' '.join(index_bamfile)))
                return None

            return bamfile

        else:
            sys.stderr.write('File: "{}" does not end with .sam, cannot convert to .bam'.format(infile))
            return None

    @staticmethod
    def quick_percent_coverages(bam_file_name, MIN_POSITIONAL_COVERAGE=1):
        try:
            bamfile = pysam.AlignmentFile(bam_file_name, 'rb')
        except Exception as e:
            sys.stderr.write(
                'Infile {} could not be opened by pysam, check that it is a BAM/SAM file\n{}\n'.format(bam_file_name, e))
            sys.exit(1)

        genome_lengths = {}
        for l, r in zip(bamfile.lengths, bamfile.references):
            genome_lengths[r] = l

        # Loop over every read, and calculate coverage an organism if it's the first read found
        organism_coverage = {}
        for read in bamfile.fetch():
            genome_name = read.reference_name
            if genome_name in organism_coverage:
                continue

            # Process one genome
            base_depth = []
            for p in bamfile.pileup(contig=genome_name):
                for pilups in p.pileups:
                    if pilups.query_position:
                        # Expand array while insert pos is out of list bounds
                        if p.reference_pos >= len(base_depth):
                            base_depth += [0] * (p.reference_pos - len(base_depth) + 1)
                            # while p.reference_pos >= len(base_depth):
                            #     base_depth.append(0)
                        base_depth[p.reference_pos] += 1
                        if base_depth[p.reference_pos] > MIN_POSITIONAL_COVERAGE:
                            continue

            bins_covered = len([x for x in base_depth if x > 0])
            organism_coverage[genome_name] = (bins_covered / genome_lengths[genome_name]) * 100
        return organism_coverage

    def percent_coverage(self):
        sys.stdout.write('\t'.join(['file', 'genome', 'percent_coverage', 'total reads mapped', 'reads mapped > 50 bp']) + '\n')
        for f in self.input_files:
            f_coverages = percent_coverages(f)
            for genome, stats in read_stats(f).items():
                stats = [str(x) for x in stats]
                sys.stdout.write('\t'.join([f, genome, str(f_coverages[genome]), stats[0], stats[1]]) + '\n')


"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-n', help='Some Number', type=int)
    parser.add_argument('-v', help='Verbose', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
"""