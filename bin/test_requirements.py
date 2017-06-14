import os
import sys
import argparse
import subprocess

#This python script will test if all of the required programs are installed
try:
    import pysam
    sys.stdout.write('Pysam\tOK\n')
except:
    sys.stdout.write('Pysam\tFailed\n')

try:
    import bs4
    sys.stdout.write('BS4\tOK\n')
except:
    sys.stdout.write('BS4\tFailed\n')

proc = subprocess.Popen('fastq-dump -X 2 SRR3403834', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while proc.poll() is None:
    commandResult = proc.wait()
if not commandResult is 0:







'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('-i', help='Input file', required=True)
    parser.add_argument('-o', help='Output file', required=True)
    parser.add_argument('-l', help='', type=int)
    parser.add_argument('-f', help='', action="store_true")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
'''