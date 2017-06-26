import os
import sys
import argparse
import pysam
import math


def bam_base_distribution(infile):
    """
    Reads in a single BAM file or directory containing BAM files and returns
    a dictionary of base counts at each position.
    EX:  this def returns "base_positions", a list of dicts, and
    base_positions[300]["A"] will give you the number of times "A" occurs at position 300
    :param infile: String, input file or directory
    :return: List containing dictionaries
    """

    # This list stores information about the bases at each position in the genome and is the return
    base_positions = []

    if infile.endswith('/'):
        file_list = os.listdir(infile)
        file_list = [(infile + f) for f in file_list]
    else:
        file_list = [infile]
    for f in file_list:
        if not f.endswith('.bam'):
            if not f.endswith('.bai'):
                sys.stderr.write('{} Does not end in .bam, skipping...\n'.format(f))
            continue
        try:
            bamfile = pysam.AlignmentFile(f, 'rb')
        except Exception as e:
            sys.stderr.write(f + ' Could not be read by pysam\n' + e + '\n')
            continue

        for p in bamfile.pileup():
            for pilups in p.pileups:
                if pilups.query_position:
                    bp = pilups.alignment.query_sequence[pilups.query_position]
                else:
                    bp = 'N'
                try:
                    if p.reference_pos >= len(base_positions):
                        while p.reference_pos >= len(base_positions):
                            base_positions.append({})
                    base_positions[p.reference_pos][bp] = base_positions[p.reference_pos].get(bp, 0) + 1
                except Exception as e:
                    sys.stderr.write(str(e)+'\n')
                    continue
    return base_positions


def condense_to_size(input_list, new_list_size=100):
    chunk_size = int(math.ceil(float(len(input_list))/new_list_size))  # math.ceil only returns ints in python 3+
    newlist = []
    for n in range(0, len(input_list), chunk_size):
        newlist.append(sum(input_list[n:n + chunk_size]) / chunk_size)
    return newlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Takes in a BAM file or directory containing BAM files and outputs 1 - the conservation'
                    'of each base in the genome.  The default format is a CSV file for a heatmap, and '
                    '-f can be used to create a full CSV with detailed informaion about each position')
    parser.add_argument('--input', '-i', help='Input file', required=True)
    parser.add_argument('--output', '-o', help='Output file', required=True)
    parser.add_argument('--number-splits', '-n', help='Number of sections to group the genome into.'
                                   'Anything over 500 may not show up well in a heatmap.', type=int)
    parser.add_argument('--full', '-f', help='Output the full base distribution (to view in a spreadsheet)'
                                   'and not just the CSV for a heatmap', action="store_true")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    if not args.number_splits:
        args.number_splits = 100

    full_base_dist = bam_base_distribution(args.input)

    if args.full:
        output = []
        for position_dict in full_base_dist:
            if sum(position_dict.values()) == 0:
                conservation = '0'
            else:
                conservation = str(float(max(position_dict.values())) / sum(position_dict.values()))
            if max(position_dict.values()) == 0:
                max_base = 'N'
            else:
                max_base = max(position_dict, key=position_dict.get)
            output.append(','.join([max_base, str(position_dict["A"]), str(position_dict["C"]), str(position_dict["G"]),
                                    str(position_dict["T"]), str(position_dict["N"]), conservation]))
        with open(args.output, 'w') as outfile:
            outfile.write('\n'.join(output))

    else:
        conservation_list = []
        for position_dict in full_base_dist:
            if sum(position_dict.values()) == 0:
                conservation_list.append(0)
            else:
                conservation_list.append(1 - float(max(position_dict.values())) / sum(position_dict.values()))
        conservation_list = condense_to_size(conservation_list, args.number_splits)
        with open(args.output, 'w') as outfile:
            outfile.write(','.join(map(str, conservation_list)))
    sys.exit(0)
