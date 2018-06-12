import sys
import os
import argparse
from sam_stats import Sam_Reader
import pysam
import subprocess

my_files = Sam_Reader('../Input/BAM_Files/', check_files=False)
out = pysam.Samfile('001895.1.sam', 'w', template=pysam.AlignmentFile(my_files.input_files[0]))
for read in my_files.reads(min_len=30, organism='NC_001895.1', verbose=True):
   out.write(read)
new_filename = '001895.1.sam'

if not new_filename.endswith('.sam'):
    new_filename = new_filename + '.sam'
bamfile = new_filename.replace('.sam', '.bam')
convert_to_bam = ["samtools", "view", "-bS", new_filename]
sort_bamfile = ["samtools", "sort", bamfile, bamfile.replace('.bam', '')]
index_bamfile = ["samtools", "index", bamfile, bamfile.replace('.bam', '.bai')]

sys.stdout.write('Converting {} to BAM file, sorting, and indexing...'.format(new_filename))
ret_code = subprocess.call(convert_to_bam, stdout=open(bamfile, 'w'))
if ret_code != 0:
    sys.stderr.write("Error running command \"{}\"\n".format(' '.join(convert_to_bam)))
ret_code = subprocess.call(sort_bamfile)
if ret_code != 0:
    sys.stderr.write("Error running command \"{}\"\n".format(' '.join(sort_bamfile)))
ret_code = subprocess.call(index_bamfile)
if ret_code != 0:
    sys.stderr.write("Error running command \"{}\"\n".format(' '.join(index_bamfile)))
