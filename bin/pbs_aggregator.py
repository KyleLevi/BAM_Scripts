import sys
import os
import argparse

"""
Position        Consensus       Percent A       C       G       T       N       Gap
0       A       0.0     0       0       0       0       0       0
1       A       0.0     0       0       0       0       0       0
2       A       0.0     0       0       0       0       0       0
3       A       0.0     0       0       0       0       0       0
4       A       0.0     0       0       0       0       0       0
5       A       0.0     0       0       0       0       0       0
6       A       0.0     0       0       0       0       0       0"""

def aggregate(dir):
    positions = [[0,0,0,0,0,0] for i in range(98000)]
    for f in os.listdir(dir):
        with open(f, 'r') as infile:
            for line in infile:
                if line.startwith("Pos"):
                    header = line
                    continue
                line = line.replace('\n', '').split('\t')
                pos = int(line[0])
                positions[pos][0] += int(line[3])
                positions[pos][1] += int(line[4])
                positions[pos][2] += int(line[5])
                positions[pos][3] += int(line[6])
                positions[pos][4] += int(line[7])
                positions[pos][5] += int(line[8])
    with open(args.outfile, 'w') as outfile:
        outfile.write(header)
        mapping = {0: 'A', 1: 'C', 2: 'G', 3: 'T', 4: 'N', 5: 'Gap'}
        for index, line in enumerate(positions):
            consensus = mapping[line.index[max(line)]]
            try:
                percent = float(max(line)) / sum(line)
            except:
                percent = 0.0
            line = [index, consensus, round(percent * 100, 2), line[0], line[1], line[2], line[3], line[4], line[5]]
            line = [str(x) for x in line]
            line[-1] = line[-1] + '\n'
            outfile.write('\t'.join(line))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Input File', required=True)
    parser.add_argument('-v', help='Verbose', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    positions = [[0,0,0,0,0,0] for i in range(98000)]
    print(len(positions), len(positions[0]))
    for f in os.listdir(args.input):
        with open(args.input + f, 'r') as infile:
            for line in infile:
                if line.startswith("Pos"):
                    header = line
                    continue
                line = line.replace('\n', '').split('\t')
                pos = int(line[0])
                positions[pos][0] += int(line[3])
                positions[pos][1] += int(line[4])
                positions[pos][2] += int(line[5])
                positions[pos][3] += int(line[6])
                positions[pos][4] += int(line[7])
                positions[pos][5] += int(line[8])
    with open(args.outfile, 'w') as outfile:
        outfile.write(header)
        mapping = {0: 'A', 1: 'C', 2: 'G', 3: 'T', 4: 'N', 5: 'Gap'}
        for index, line in enumerate(positions):
            consensus = mapping[line.index[max(line)]]
            try:
                percent = float(max(line)) / sum(line)
            except:
                percent = 0.0
            line = [index, consensus, round(percent * 100, 2), line[0], line[1], line[2], line[3], line[4], line[5]]
            line = [str(x) for x in line]
            line[-1] = line[-1] + '\n'
            outfile.write('\t'.join(line))
