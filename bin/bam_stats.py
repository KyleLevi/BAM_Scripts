import argparse
import pysam
import os
import sys
from sam_stats import Sam_Reader

### Outdated
# def samstats(infile, csvoutfile, min_read_length=50):
#     """
#     Reads in a single SAM/BAM file and outputs to a CSV file the following information:
#     :param infile: String, The location and name of the SAM/BAM file to be read  EX: '~/Desktop/SRR3403834.sam'
#     :param csvoutfile: String, The location and name of the CSV file to append  EX:  '~/Desktop/bamfile_statistics.csv'
#     :param min_read_length: Int, The value that determines which matches are "Clean"
#     :return: None - Output is written to csvoutfile
#     """
#
#     # stats = [] holds all of the outputs -
#     # [0] = run accession EX: SRR3403834
#     # [1] = Genome the read mapped to EX: JQ995537
#     # [2] = # of matches
#     # [3] = Avg Match Length
#     # [4] = Total Matched Bases
#     # [5] = Clean # of Matches
#     # [6] = Clean Avg Match Length
#     # [7] = Clean Total Matched Bases
#     # [8] = Matches lost to "Cleaning"
#     # [9] = Increase in Avg Match Length from "Cleaning"
#     # [10] = Total Bases Lost to "Cleaning"
#
#     # stats[0] - run accession
#     run_acc = infile.split('.')[0].split('/')[-1]
#
#     if infile.endswith('.sam'):
#         readtype = 'r'
#     elif infile.endswith('.bam'):
#         readtype = 'rb'
#     else:
#         sys.stderr.write('infile {} does not end with .sam or .bam, trying as samfile...\n'.format(infile))
#         readtype = 'r'
#     try:
#         samfile = pysam.AlignmentFile(infile, readtype)
#     except Exception as e:
#         sys.stderr.write('Infile {} could not be opened by pysam, check that it is a BAM/SAM file\n{}\n'.format(infile,e))
#         sys.exit()
#
#     # [1-4]
#     refnames = {}  # {organism: {'total_matches': [], 'total_bases': [], 'stats': [run_acc, refname]}}
#     read_count = 0
#     for read in samfile.fetch():
#         read_count += 1
#         refname = read.reference_name
#         if refname not in refnames:
#             refnames[refname] = {'total_matches': [], 'total_bases': [], 'stats': [run_acc, refname]}
#         x, y = read.get_cigar_stats()
#         refnames[refname]['total_matches'].append(int(x[0]))
#         refnames[refname]['total_bases'].append(int(sum(x)))
#
#     if read_count == 0:  # If no reads
#         sys.stderr.write('No reads in file: {}, exiting\n'.format(infile))
#         return
#
#     for k, v in refnames.items():
#         total_bases = v['total_bases']
#         total_matches = v['total_matches']
#
#         v['stats'].append(len(total_matches))
#         v['stats'].append(int(sum(total_matches)/len(total_bases)))
#         v['stats'].append(int(sum(total_matches)))
#
#         # [5-7]
#         clean_matches = [x for x in total_matches if x >= min_read_length]
#         clean_total_bases = [x for i, x in enumerate(total_bases) if total_matches[i] >= min_read_length]
#         v['stats'].append(len(clean_matches))
#         if len(clean_total_bases) == 0:
#             v['stats'].append(0)
#         else:
#             v['stats'].append(int(sum(clean_matches)/len(clean_total_bases)))
#         v['stats'].append(int(sum(clean_matches)))
#
#         # [8-10]
#         stats = v['stats']
#         v['stats'].append(stats[5]-stats[2])
#         v['stats'].append(stats[6]-stats[3])
#         v['stats'].append(stats[7]-stats[4])
#
#         # Format and output
#         stats = map(str, v['stats'])
#         outstring = ','.join(stats)
#         os.system('echo {} >> {}'.format(outstring, csvoutfile))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads a SAM or BAM file and appends a CSV file with information about the matched reads')
    parser.add_argument('-i', '--input', help='Name of the input .sam file to be read', required=True)
    parser.add_argument('-o', '--output', help='Name of the CSV file to append')
    parser.add_argument('-l', '--length', help='Ignore matches shorter than -l base pairs, default is 50', type=int)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.length:
        args.l = 50

    data = Sam_Reader(args.input)
    if not args.output:
        args.output = ''
    print(data)
    data.per_base_stats( write_file=args.output )

