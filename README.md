BAM_Scripts is a collection of tools grouped into two main functions.
1) Getting publicly available data from the Sequence Read Archive (SRA) and using read mapping (Bowtie2) to search for matching reads.
2) Analyzing and visualizing data stored in .BAM or .SAM files, as well as many common tasks such as removing matches below a certain length, splitting files based on organism, retrieving XML metadata from SRA runs.

### Getting Started
#### 1. Finding SRA data to work with

The SRA provides a great interactive search functionality for finding data sets.  Use this to find runs that you are interested in and when you are done, download the run list as a file called "SraRunAcc.txt". *#TODO: Insert picture here*. 
Place this in the "Input" folder of the project. \
**Note: If you are using the makefile to simplify downloading, it is *very* important that you do not rename SraRunAcc.txt**

#### 2. Add FASTA genomes to the Input/Genomes folder

Whether you are looking for a bacteria, phage or even just a region of DNA, add the FASTA format file to the Input/Genomes folder. When using the Makefile, these will automatically be combined and a Bowtie2 index will be constructed.
#### 3. Generating BAM files

Now that you have your datasets and target DNA chosen, it is time to start downloading and scanning SRA runs. From a terminal in the main direcory (../BAM_Scripts/) type:
>make split_BAM_files

This will:
 * Download 100,000 reads for each SRA run (in the FASTQ format).
 * Create a Bowtie2 index of all FASTA files in the Input/Genomes/ folder.
 * Scan each of the downloaded data sets with Bowtie 2 - creating SAM files in the Input/SAM_files/ folder.
 * Convert the SAM files to BAM files and index them.
 * Lastly, the BAM files in Input/raw_BAM_files/ will be split by organism into new folders in Output/split_BAM_files/<organism_name_here>/.
 
#### 4. Take a peek inside those BAM files with bam_stats.py
Since BAM files aren't human readable, if you want to see what was found, try running bam_stats.py:
> python bin/bam_stats.py -i Output/split_BAM_files/<organism_name_here>/ -o Output/bam_stats.csv

This will output a CSV document (bam_stats.csv) that is viewable in any spreadsheet program.

### Requirements

This project requires the following programs:
1) The [SRA toolkit](https://github.com/ncbi/sra-tools/wiki/HowTo:-Binary-Installation) to download datasets.
2) [Samtools/HTSlib](http://www.htslib.org/download/) to convert SAM to BAM files and index them.
3) [Bowtie 2](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#obtaining-bowtie-2) for read mapping.
4) [Python](https://www.python.org/downloads/) with the module [Pysam](https://github.com/pysam-developers/pysam) installed and optionally [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) if you plan on working with XML metadata files.

*Note: if you are using the Makefile, these programs must also have the appropriate PATH variable setup. This can be checked by running:*
>make test

Additionally, a demo is available by running(TODO):
>make demo



