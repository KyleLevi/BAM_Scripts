import os
import sys
import argparse
import pysam
import math


def bam_base_distribution(infile, maximum):
    '''Reads in a single BAM file or directory containing BAM files and returns
    information about each base position in the genome. The return is a 
    list of lists (python 2d array) where the X is the base position in the genome
    and the Y is the number of times each base is observed at that position. 
    EX: base_list[200][3] will be the number of times "T" is matched at base 200.
    [0] = "A"  |  [1] = "C"  |  [2]  
    '''

    # This list stores information about the bases at each position in the genome
    base_list = [[0 for x in range(5)] for y in range(maximum)]

    # This will be used as a case switch to add to sub lists
    sublist_switch = {
        "A": 0,
        "C": 0,
        "G": 0,
        "T": 0,
        "N": 0
    }
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
                    base_list[p.reference_pos][sublist_switch[bp]] += 1
                except Exception as e:
                    sys.stderr.write(e)
                    continue
    return base_list


def condense_to_size(input_list, new_list_size=100):
    chunk_size = int(math.ceil(float(len(input_list))/new_list_size))  # math.ceil only returns ints in python 3+
    newlist = []
    chunk_size = int(chunk_size)
    for n in range(0, len(input_list), chunk_size):
        newlist.append(sum(input_list[n:n + chunk_size]) / chunk_size)
    return newlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Takes in a BAM file or directory containing BAM files and outputs 1 - the conservation'
                    'of each base in the genome.  The default format is a CSV file for a heatmap, and '
                    '-f can be used to create a full CSV with detailed informaion about each position')
    parser.add_argument('--input', '-i', help='Input file', required=True)
    parser.add_argument('-o', help='Output file', required=True)
    parser.add_argument('-n', help='Number of sections to group the genome into.'
                                   'Anything over 500 may not show up well in a heatmap.', type=int)
    parser.add_argument('-m', help='Genome length, if you do not know, overestimate', type=int)
    parser.add_argument('-f', help='Output the full base distribution (to view in a spreadsheet)'
                                   'and not just the CSV for a heatmap', action="store_true")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    list_to_base_switch = {
        0: "A",
        1: "C",
        2: "G",
        3: "T",
        4: "-"
    }

    full_base_dist = bam_base_distribution(args.input, args.m)

    if args.f:
        output = []
        for sublist in full_base_dist:
            if sum(sublist) == 0:
                conservation = '0'
            else:
                conservation = str(float(max(sublist))/sum(sublist))
            if max(sublist) == 0:
                max_base = 'N'
            else:
                max_base = list_to_base_switch[sublist.index(max(sublist))]
            output.append(','.join([
                max_base,
                str(sublist[0]), str(sublist[1]), str(sublist[2]), str(sublist[3]), str(sublist[4]),
                conservation]))
        with open(args.o, 'w') as outfile:
            outfile.write('\n'.join(output))

    else:
        conservation_list = []
        for sublist in full_base_dist:
            if sum(sublist) == 0:
                conservation_list.append(0)
            else:
                conservation_list.append(1 - float(max(sublist))/sum(sublist))
        conservation_list = condense_to_size(conservation_list, args.n)
        with open(args.o, 'w') as outfile:
            outfile.write(','.join(map(str, conservation_list)))
    sys.exit(0)
