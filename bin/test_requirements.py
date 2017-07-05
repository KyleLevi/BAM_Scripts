import sys
import subprocess


#This python script will test if all of the required programs are installed
sys.stdout.write("Testing to see if required programs are installed.\nNote: This does not test all aspects"
                 " of each program, only that it is installed and setup with PATH a variable.\n"
                 "More on PATH variables here: http://www.linfo.org/path_env_var.html\n")
try:
    import pysam
    sys.stdout.write('Pysam\tOK\n')
except:
    sys.stdout.write('Pysam\tFailed\n')

try:
    import bs4
    sys.stdout.write('BS4(optional)\tOK\n')
except:
    sys.stdout.write('BS4(optional)\tFailed\n')

proc = subprocess.Popen('fastq-dump --help', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while proc.poll() is None:
    commandResult = proc.wait()
if commandResult is 0:
    sys.stdout.write('SRA Toolkit\tOK\n')
else:
    sys.stdout.write('SRA Toolkit\tFailed\n')

proc = subprocess.Popen('bowtie2 --help', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while proc.poll() is None:
    commandResult = proc.wait()
if commandResult is 0:
    sys.stdout.write('Bowtie 2\tOK\n')
else:
    sys.stdout.write('Bowtie 2\tFailed\n')

proc = subprocess.Popen('which samtools', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while proc.poll() is None:
    commandResult = proc.wait()
if commandResult is 0:
    sys.stdout.write('Samtools\tOK\n')
else:
    sys.stdout.write('Samtools\tFailed\n')
