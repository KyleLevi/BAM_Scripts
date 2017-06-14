


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

#Makes split BAM files in the OUTPUT folder from BAM files in INPUT folder
split_BAM_files: raw_BAM_files
	for file in Input/raw_BAM_files/*.bam; do \
	echo "Splitting $$file, and writing to Output/split_BAM_files ..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	python bin/split_bam.py -i Input/raw_BAM_files/$$file.bam -o Output/split_BAM_files/ -l 50; \
	done
	echo "Indexing BAM files in Output/split_BAM_files..."
	for file in Output/split_BAM_files/*.bam; do \
	samtools index $$file; \
	done

# Converts SAM files to BAM files and splits by organism, sorts and indexes them one at a time.
raw_BAM_files: SAM_files
	for file in Input/SAM_files/*.sam; do \
	echo "Converting, sorting and indexing $$file..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	samtools view -bS Input/SAM_files/$$file.sam | samtools sort - Input/raw_BAM_files/$$file; \
	samtools index Input/raw_BAM_files/$$file.bam; \
	done

# Scans all of the files in the SRA folder with Bowtie 2 and outputs the results to SAM files in the SAM_Files folder
SAM_files: bowtie2_index, small_sra_download
	for file in Input/SRA_datasets/*.fastq; do \
	echo "Scanning $$file with Bowtie 2..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	bowtie2 -q -x Input/Genomes/all_genomes --no-unal  Input/SRA_datasets/$$file.fastq  -S Input/SAM_files/$$file.sam; \
	done

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
	fastq-dump --outdir Input/SRA_datasets/ -N 100001 -X 200000 --skip-technical --readids  --dumpbase --clip $$l; \
	done <Input/SraAccList.txt
# Removes SAM/BAM files and SRA downloads.  Genomes remain.


# REVERTS THE PROJECT TO "git clone" STATUS.  AKA When you first downloaded BAM_Scripts
make hard_clean:
	-rm -r Input Output
	mkdir Input Output Input/raw_BAM_files Input/Genomes Input/SAM_files Input/SRA_datasets Input/xml_metadata







