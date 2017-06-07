


## Runs bam_stats.py for each BAM file in Output/BAM_files/ and outputs to Output/BAM_stats_output.csv
bam_stats:
	for f in Input/BAM_files/*.bam; do \
	python bin/bam_stats.py -i $$f -o Output/BAM_stats_output.csv -l 50; \
	done

## Downloads the FULL (BIG FILE SIZE) runs in Input/SraAccList.txt to Input/Metagenomes (.fastQ format not .sra)
full_sra_download:
	while read l; do \
	echo "Downloading $$l"; \
	fastq-dump --outdir Input/Metagenomes/ --skip-technical --readids --dumpbase --clip $$l; \
	done <Input/SraAccList.txt

## Downloads 100k reads, scans, and deletes
test1:
	
heatmap: coverage_depth_csv
	python bin/csv_to_heatmap.py -i Output/coverage_depth.csv -o "Output/heatmap_$(date +"%d%b%H%M")"

## Makes a coverage depth CSV from BAM files for visualization
# Here is the code executed for reference:
# echo "How long is the genome used to create these BAM files? (Overestimate if you don't know exactly)"
# read genome_length
# echo "How many pieces should the genome be broken into? Please chose a value less than 500; large values will not show up well as each point requires at least 1 pixel)"
# read chunk_size
# python bin/bam_to_heatmap_csv.py -i Input/BAM_files/ -o Output/bam_heatmap.csv -l $genome_length -n $chunk_size
coverage_depth_csv:
	bash bin/coverage_depth_csv.sh








