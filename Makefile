# This Makefile contains helpfull commands for downloading and analyzing data from the SRA.
# They can be run from the terminal by typing "make comand_name".  EX: Make BAM_stats
# Even if you never use these commands here, they provide a good example of ways to use the python
#  scripts included in this project.

test:
	python bin/test_requirements.py

demo:
	#Demo SRA accession list
	echo "SRR3403834.sra\nSRR3403835.sra\nSRR3403836.sra\n" > Sra_Acc_List.txt
	#Download 100k reads from each dataset
	while read l; do \
	echo "Downloading $$l"; \
	fastq-dump --outdir Input/SRA_datasets/ -N 100001 -X 200000 --skip-technical --readids  --dumpbase --clip $$l; \
	done <Input/SraAccList.txt


#---------------Applying Python Scripts to BAM files---------------

# Runs bam_stats.py for each BAM file in Output/BAM_files/ and outputs to Output/BAM_stats_output.csv
BAM_stats:
	for f in Input/BAM_files/*.bam; do \
	python bin/bam_stats.py -i $$f -o Output/BAM_stats_output.csv -l 50; \
	done

# Turn your CSV files into heatmaps! Open this python file (bin/csv_to_heatmap.py) and
#  edit lines 64-70 to change what the heatmap looks like.
# Here is a good starting place for the Seaborn Heatmap: http://seaborn.pydata.org/generated/seaborn.heatmap.html
coverage_depth_heatmap: coverage_depth_csv
	python bin/csv_to_heatmap.py -i Output/coverage_depth.csv -o "Output/coverage_heatmap_$(date +"%d%b%H%M")"

conserved_regions_heatmap: conserved_regions_csv
	python bin/csv_to_heatmap.py -i Output/conserved_regions.csv -o "Output/conservation_heatmap_$(date +"%d%b%H%M")"

# Makes a coverage depth CSV from BAM files for visualization
coverage_depth_csv:
	python bin/coverage_depth_csv.py --number-splits 200 -i Output/split_BAM_files/ -o Output/coverage_depth.csv

# Makes a CSV file containing the conservation of each base
conserved_regions_csv:
	python bin/conservation_csv.py --number-splits 200 -i Output/split_BAM_files/ -o Output/conserved_regions.csv


#---------------Downloading SRA datasets and Generating BAM files---------------

#Makes split BAM files in the OUTPUT folder from BAM files in INPUT folder
split_BAM_files: raw_BAM_files
	for file in Input/raw_BAM_files/*.bam; do \
	echo "Splitting $$file, and writing to Output/split_BAM_files ..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	python bin/split_bam.py -i Input/raw_BAM_files/$$file.bam -o Output/split_BAM_files/ -l 50; \
	done
	echo "Indexing BAM files in Output/split_BAM_files..." ; \
	for file in Output/split_BAM_files/*.bam; do \
	samtools index $$file; \
	done

only_split_BAM_files:
	for file in Input/raw_BAM_files/*.bam; do \
	echo "Splitting $$file, and writing to Output/split_BAM_files ..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	python bin/split_bam.py -i Input/raw_BAM_files/$$file.bam -o Output/split_BAM_files/ -l 50; \
	done
	echo "Indexing BAM files in Output/split_BAM_files..."; \
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

only_raw_BAM_files:
	for file in Input/SAM_files/*.sam; do \
	echo "Converting, sorting and indexing $$file..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	samtools view -bS Input/SAM_files/$$file.sam | samtools sort - Input/raw_BAM_files/$$file; \
	samtools index Input/raw_BAM_files/$$file.bam; \
	done

# Scans all of the files in the SRA_datasets folder with Bowtie 2 and outputs the results to SAM files in the SAM_Files folder
SAM_files: bowtie2_index small_sra_download
	for file in Input/SRA_datasets/*.fastq; do \
	echo "Scanning $$file with Bowtie 2..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	bowtie2 -q -x Input/Genomes/all_genomes --no-unal  Input/SRA_datasets/$$file.fastq  -S Input/SAM_files/$$file.sam; \
	done

only_SAM_files:
	for file in Input/SRA_datasets/*.fastq; do \
	echo "Scanning $$file with Bowtie 2..."; \
	file=$$(echo "$$file" | rev | cut -d"/" -f1 | rev); \
	file=$$(echo "$$file" | cut -d"." -f1); \
	bowtie2 -q -x Input/Genomes/all_genomes --no-unal  Input/SRA_datasets/$$file.fastq  -S Input/SAM_files/$$file.sam; \
	done

# Constructs a single bowtie 2 index from everything in the Input/Genomes/ folder
bowtie2_index:
	-rm Input/Genomes/all_genomes.*
	cat Input/Genomes/*.fasta > Input/Genomes/all_genomes.fna
	bowtie2-build Input/Genomes/all_genomes.fna Input/Genomes/all_genomes	

# Downloads 100k reads from every run in SraAccList.txt (By default it will download reads 100,000 to 200,000 - 
#  if there are less than 100,000 reads it will download nothing)
small_sra_download:
	while read l; do \
	echo "Downloading $$l"; \
	fastq-dump --outdir Input/SRA_datasets/ -N 100001 -X 200000 --skip-technical --readids  --dumpbase --clip $$l; \
	done <Input/SraAccList.txt

# Downloads the FULL (BIG FILE SIZE) runs in Input/SraAccList.txt to Input/Metagenomes (.fastQ format not .sra).
# Please don't do this unless you know what you are doing.
full_sra_download:
	while read l; do \
	echo "Downloading $$l"; \
	fastq-dump --outdir Input/SRA_datasets/ --skip-technical --readids --split-files --dumpbase --clip $$l; \
	#This next line will delete the .sra file from ~/ncbi/public/sra; \
	-rm ~/ncbi/public/sra/$$l.sra; \
	done <Input/SraAccList.txt

# Deletes everything in the Input and Output folders
make hard_clean:
	-rm -r Input Output
	mkdir Input Output Input/raw_BAM_files Input/Genomes Input/SAM_files Input/SRA_datasets Input/xml_metadata

# Removes SAM/BAM files and SRA downloads.  Genomes remain.
soft_clean:
	-rm Input/SRA_datasets/* Input/SAM_files/* Input/raw_BAM_files/*





