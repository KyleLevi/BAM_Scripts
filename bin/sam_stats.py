import sys
import os
import argparse
import subprocess
import pysam

class Sam_Reader:

    def __init__(self, file_or_folder, **kwargs):
        """
        Initialize with the path to a file or a folder. If a file is
        :param file_or_folder:
        """

        # Generate a list of files in dir, and convert sam to bam
        if not os.path.isdir(file_or_folder):
            if file_or_folder.endswith('.sam'):
                file_or_folder = self.sam_to_bam(file_or_folder)
            input_files = [file_or_folder]
        else:
            if not file_or_folder.endswith('/'):
                file_or_folder = file_or_folder + '/'
            # Get the names of every SAM and BAM file in the input dir
            input_files = [file_or_folder + file_name for file_name in os.listdir(file_or_folder) if
                           file_name.endswith(".sam") or file_name.endswith('.bam')]
            # Trim sam files from the list that have a bam file of the same name in the list
            input_files = [file_name for file_name in input_files if not
            (file_name.endswith('.sam') and file_name.replace('.sam','.bam') in input_files)]
            # Convert any sam files to bam files, sort, index and add the new file names to the input_files
            input_files = [file_name if file_name.endswith('.bam') else self.sam_to_bam(file_name) for file_name in input_files]
        self.input_files = input_files

        # Check if every BAM files has an index
        #TODO

        # Check if every file can be opened and record genomes & lengths
        genome_lengths = {}
        removed_files = []

        for f in self.input_files:
            try:
                bamfile = pysam.AlignmentFile(f, 'rb')
            except Exception as e:
                sys.stderr.write('File {} could not be opened by pysam because...:\n{}\n'.format(f, e))
                sys.stderr.write('Removing {} from input list and continuing.\n')
                removed_files.append(f)

            for l, r in zip(bamfile.lengths, bamfile.references):
                genome_lengths[r] = l
        self.input_files = list(set(self.input_files)-set(removed_files))
        self.broken_files = removed_files
        self.genome_lengths = genome_lengths

    def __str__(self):
        return "{} BAM file(s): (use .input_files)\n{} Organism(s)/Genome_Length {}\n".format(len(self.input_files), len(self.genome_lengths.keys()), str(self.genome_lengths))

    @staticmethod
    def sam_to_bam(infile, outdir = None):
        """
        Converts a SAM file to a BAM file, sorts it, and Indexes it.
        :param infile: path to SAM file
        :param outdir: (optional) path to write BAM file to
        :return: path to new BAM file
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

            sys.stdout.write('Converting {} to BAM file, sorting, and indexing...'.format(infile))
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
    def read_counts(bam_file_name, n=50):

        bamfile = pysam.AlignmentFile(bam_file_name, 'rb')
        stats_dict = {}  # {genome_name: [total_reads_mapped, reads > n base pairs long]}
        for read in bamfile.fetch():
            if not read.reference_name in stats_dict:
                stats_dict[read.reference_name] = [0, 0]# index 0 is count of all reads, index 1 is all reads > n length
            total_len = int(sum(read.get_cigar_stats()[0]))
            if total_len > n:
                stats_dict[read.reference_name][1] += 1
            stats_dict[read.reference_name][0] += 1
        if stats_dict == {}:
            return {'None': [0, 0]}
        return stats_dict

    def quick_percent_coverages(self, bam_file_name, organism=None, MIN_POSITIONAL_COVERAGE=1):
        bamfile = pysam.AlignmentFile(bam_file_name, 'rb')

        # Loop over every read, and calculate coverage an organism if it's the first read found
        organism_coverage = {}
        for read in bamfile.fetch():
            genome_name = read.reference_name
            if genome_name in organism_coverage:
                print('exists')
                continue
            if organism != None and organism != genome_name:
                print('specified and not{}{}'.format(genome_name,organism))
                continue

            # Process one organism
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
            organism_coverage[genome_name] = (bins_covered / self.genome_lengths[genome_name]) * 100
            if organism_coverage == {}:
                return {'None': 0}
        return organism_coverage

    def stats(self, **kwargs):
        """
        File  |  Genome  |  Percent Coverage  |  Total Mapped Reads  |  Mapped Reads > 50 bp

        :param kwargs:
        :return:
        """
        # Setting Kwargs and defaults
        if kwargs.get('write_file', False):
            sys.stdout = open(kwargs['write_file'], 'w')
        else:
            kwargs['write_file'] = False
        organism = kwargs.get('organism', None)
        file_name = kwargs.get('file_name', None)
        min_read_len = kwargs.get('min_read_length', 50)
        min_cov_depth = kwargs.get('min_coverage_depth', 1)

        header = '\t'.join(['file', 'genome', 'percent_coverage', 'total reads mapped', 'reads mapped > {} bp'.format(min_read_len) + '\n'])
        if kwargs['write_file']:
            sys.stdout.write(header)
        results = [header]

        for f in self.input_files:
            # if a specific file is specified and this file isn't it, continue
            if file_name != None and f != file_name:
                continue
            f_coverages = self.quick_percent_coverages(f, organism, min_cov_depth)

            for genome, stats in Sam_Reader.read_counts(f, min_read_len).items():
                stats = [str(x) for x in stats]
                line = '\t'.join([f, genome, str(f_coverages.get(genome, 'None')), stats[0], stats[1]]) + '\n'
                if kwargs['write_file']:
                    sys.stdout.write(line)
                results.append(line)
        return results

    def per_base_stats(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        # Setting Kwargs and defaults
        kwargs['write_file'] = kwargs.get('write_file', False)
        organism = kwargs.get('organism', None)
        file_name = kwargs.get('file_name', None)
        min_read_len = kwargs.get('min_read_length', 50)

        if organism == None and len(self.genome_lengths.keys()) > 1:
            sys.stderr.write("Organism name not specified for per_base_stats and more than one organism is present,\n"
                             "try setting organism    .per_base_stats(organism=......)\n"
                             "Available organism names are: {}".format(', '.join(self.genome_lengths.keys())))
        else:
            organism = list(self.genome_lengths.keys())[0]

        header = '\t'.join(['file', 'genome', 'percent_coverage', 'total reads mapped',
                            'reads mapped > {} bp'.format(min_read_len) + '\n'])


        # Initialize a list for every position in the genome, with an empty dictionary
        base_positions = [{"A": 0, "C": 0, "G": 0, "T": 0, "N": 0, "Gap": 0} for i in range(self.genome_lengths[organism])]


        if kwargs['write_file']:
            outfile = open(kwargs['write_file'], 'w')
            header = "\t".join(['Position', 'Consensus', 'Percent', 'A', 'C', 'G', 'T', 'N' 'Gap\n'])
            outfile.write(header)

        import pickle
        if 'save.p' in os.listdir():
            pos_dict = pickle.load(open("save.p", "rb"))
        else:

            for f in self.input_files:
                # if a specific file is specified and this file isn't it, continue
                if file_name != None and f != file_name:
                    continue

                bamfile = pysam.AlignmentFile(f, 'rb')
                for p in bamfile.pileup(contig=organism):
                    for pilups in p.pileups:
                        if pilups.query_position:
                            bp = pilups.alignment.query_sequence[pilups.query_position]
                        else:
                            bp = 'Gap'
                        base_positions[p.reference_pos][bp] = base_positions[p.reference_pos].get(bp, 0) + 1
                    if kwargs['write_file']:
                        pos_dict = base_positions[p.reference_pos]
                        consensus = max(pos_dict, key=pos_dict.get)
                        percent = float(pos_dict[consensus]) / sum(list(pos_dict.values()))
                        line = [p.reference_pos, consensus, percent*100, pos_dict['A'], pos_dict['C'], pos_dict['G'], pos_dict['T'], pos_dict['N'], pos_dict['Gap']]
                        line = [str(x) for x in line]
                        line[-1] = line[-1] + '\n'
                        outfile.write('\t'.join(line))
            pickle.dump(pos_dict, open("save.p", "wb"))



        if kwargs['write_file']:
            output_path = kwargs['write_file'] + '_{}.csv'.format(organism)
            with open(output_path, 'w') as outfile:
                header = "\t".join(['Position', 'Consensus', 'Percent', 'A', 'C', 'G', 'T', 'N' 'Gap\n'])
                outfile.write(header)
                for index, pos_dict in enumerate(base_positions):
                    consensus = max(pos_dict, key=pos_dict.get)
                    try:
                        percent = float(pos_dict[consensus]) / sum(list(pos_dict.values()))
                    except:
                        percent = 0.0
                    line = [index, consensus, round(percent * 100, 2), pos_dict['A'], pos_dict['C'], pos_dict['G'],
                            pos_dict['T'], pos_dict['N'], pos_dict['Gap']]
                    line = [str(x) for x in line]
                    line[-1] = line[-1] + '\n'
                    outfile.write('\t'.join(line))

        return base_positions




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='ouput directory')
    parser.add_argument('-n', help='Some Number', type=int)
    parser.add_argument('-v', help='Verbose', action='store_true')
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)



    data = Sam_Reader(args.input)
    if not args.output:
        args.output = ''
    print(data)
    data.per_base_stats( write_file=args.output )
