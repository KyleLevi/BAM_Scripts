BAM_Scripts is a collection of tools grouped into two main functions.
1) Getting publicly available data from the Sequence Read Archive (SRA) and using read mapping (Bowtie2) to search for reads of interest.
2) Analyzing and visualizing data stored in .BAM or .SAM files.

**This project is currently in development** 

This project requires the following:\
1) The [SRA toolkit](https://github.com/ncbi/sra-tools/wiki/HowTo:-Binary-Installation) to download datasets.
2) [Samtools/HTSlib](http://www.htslib.org/download/) to convert SAM to BAM files and index them.
3) [Bowtie 2](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#obtaining-bowtie-2) for read mapping.
4) [Python](https://www.python.org/downloads/) with the module [Pysam](https://github.com/pysam-developers/pysam) installed and optionally [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) if you plan on working with XML metadata files.\




