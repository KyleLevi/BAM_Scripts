import sys
import os
import argparse


class M8_Reader:

    def __init__(self, path_to_m8_files):
        self.input_files = []

        if not os.path.isdir(path_to_m8_files):
            if path_to_m8_files.endswith('.m8'):
                self.input_files = [path_to_m8_files]
            else:
                sys.stdout.write("Input is a file (not a folder) that does not end in .m8 - aborting")
                sys.exit(1)
        else:
            if not path_to_m8_files.endswith('/'):
                path_to_m8_files = path_to_m8_files + '/'
            for f in os.listdir(path_to_m8_files):
                self.input_files.append(path_to_m8_files + f)

    def __str__(self):
        return "{} .m8 files total: {}".format(len(self.input_files), ', '.join(self.input_files))

    def hits(self):
        header = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore', 'protein', 'match']
        file_stats = {}  # {file_name: {protiein: hits, protein2: hits, ...]
        for f in self.input_files:
            file_stats[f] = {}
            with open(f, 'r') as infile:
                for line in infile:
                    line = line.split('\t')
                    file_stats[f][line[1]] = file_stats[f].get(line[1], 0) + 1
        return file_stats


# data = M8_Reader("t/")
# print(data)
# print(data.hits())

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

