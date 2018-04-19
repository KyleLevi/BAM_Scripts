"""
M8_Reader! This package is designed to read .m8 files produced by diamond blastx, specifically with a command
to include the actual DNA sequence matched to the protein. This information is not provided by default when using
diamond. use the argument 	 -f 6  qseqid sseqid pident length mismatch qstart qend sstart send evalue bitscore sseq qseq
This will give the same output, with the addition of two extra fields, sseq and qseq.  The whole command is:
diamond blastx -f 6  qseqid sseqid pident length mismatch qstart qend sstart send evalue bitscore sseq qseq -d Input/Proteins/all_diamond_db -q Input/SRA_datasets/$$l.fastq  -o Input/RAP_Results/$$l.m8; \


"""


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
        self.header = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore', 'protein', 'match']


    def __str__(self):
        return "{} .m8 files total: {}".format(len(self.input_files), ', '.join(self.input_files))

    def hits(self, **kwargs):
        only_this_protein = kwargs.get('protein', None)
        only_this_file = kwargs.get('file_name', None)

        file_stats = {}  # {file_name: {protiein: hits, protein2: hits, ...]
        for f in self.input_files:
            if only_this_file != None and f.split('/')[-1] != only_this_file:
                continue
            file_stats[f] = {}
            with open(f, 'r') as infile:
                for line in infile:
                    line = line.split('\t')
                    if only_this_protein != None and line[1] != only_this_protein:
                        continue
                    file_stats[f][line[1]] = file_stats[f].get(line[1], 0) + 1
        return file_stats

    def matches(self, **kwargs):
        only_this_protein = kwargs.get('protein', None)
        only_this_file = kwargs.get('file_name', None)
        no_stops = kwargs.get('no_stops', False)
        for f in self.input_files:
            with open(f, 'r') as infile:
                if only_this_file != None and only_this_file != f:
                    continue
                for line in infile:
                    match = Match(line)
                    if no_stops and '*' in match.qprot:
                        continue
                    if only_this_protein != None and only_this_protein != match.protein:
                        continue
                    yield match

    def protein_stats(self):


class Match:
    CODON_TABLE = {"TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
                   "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
                   "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
                   "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
                   "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
                   "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
                   "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
                   "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
                   "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
                   "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
                   "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
                   "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
                   "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
                   "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
                   "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
                   "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G"}

    def __init__(self, line):
        line = line.replace('\n', '').split('\t')
        self.qseqid = line[0]
        self.protein = line[1]
        self.pident = float(line[2])
        self.length = int(line[3])
        self.mismatch = int(line[4])
        self.qstart = int(line[5])
        self.qend = int(line[6])
        self.sstart = int(line[7])
        self.send = int(line[8])
        self.evalue = float(line[9])
        self.bitscore = float(line[10])
        self.sprot = line[11]
        self.qseq = line[12]
        self.qprot = ''.join([Match.CODON_TABLE[self.qseq[i:i+3]] for i in range(0,len(self.qseq), 3)])



    def __str__(self):
        line = [self.protein, self.evalue, self.length]
        return "\t".join([str(x) for x in line])


data = M8_Reader("t/")
for match in data.matches():
    if match.evalue < .0000000001:
        print(match.qprot)
        print(match.sprot)
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

