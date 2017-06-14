


# Runs bam_stats.py for each BAM file in Output/BAM_files/ and outputs to Output/BAM_stats_output.csv
bam_stats:
	for f in Input/BAM_files/*.bam; do \
	python bin/bam_stats.py -i $$f -o Output/BAM_stats_output.csv -l 50; \
	done

	
heatmap: coverage_depth_csv
	python bin/csv_to_heatmap.py -i Output/coverage_depth.csv -o "Output/heatmap_$(date +"%d%b%H%M")"

# Makes a coverage depth CSV from BAM files for visualization
# see bin/coveragedepth.sh
coverage_depth_csv:
	bash bin/coverage_depth_csv.sh

# Converts SAM files to BAM files, sorts and indexes them one at a time.
BAM_files:
	while read l; do \
	echo "Converting, sorting and indexing $$l..."; \
	samtools view -bS Input/SAM_files/$$l.sam | samtools sort - Input/BAM_files/$$l; \
	samtools index Input/BAM_files/$$l.bam; \
	done <Input/SraAccList.txt

# Scans all of the files in the SRA folder with Bowtie 2 and outputs the results to SAM files in the SAM_Files folder
SAM_files:
	while read l; do \
	echo "Scanning $$l with Bowtie 2..."; \
	bowtie2 -q -x Input/Genomes/all_genomes --no-unal  Input/SRA_datasets/$$l.fastq  -S Input/SAM_files/$$l.sam; \
	done <Input/SraAccList.txt

# Constructs a single bowtie 2 index from everything in the Input/Genomes/ folder
bowtie2_index:
	-rm Input/Genomes/all_genomes*
	cat Input/Genomes/*.fasta > Input/Genomes/all_genomes.fna
	bowtie2-build Input/Genomes/all_genomes.fna Input/Genomes/all_genomes	

# Downloads the FULL (BIG FILE SIZE) runs in Input/SraAccList.txt to Input/Metagenomes (.fastQ format not .sra).  
# Please don't do this unless you know what you are doing.
full_sra_download:
	while read l; do \
	echo "Downloading $$l"; \
	fastq-dump --outdir Input/Metagenomes/ --skip-technical --readids --split-files --dumpbase --clip $$l; \
	done <Input/SraAccList.txt

# Downloads 100k reads from every run in SraAccList.txt (By default it will download reads 100,000 to 200,000 - 
#  this may not work with SRA runs with less than 200,000 reads)
small_sra_download:
	while read l; do \
	echo "Downloading $$l"; \
	fastq-dump --outdir Input/Metagenomes/ -N 100001 -X 200000 --skip-technical --readids  --dumpbase --clip $$l; \
	done <Input/SraAccList.txt







