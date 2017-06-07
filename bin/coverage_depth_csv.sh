echo ''
echo "How long is the genome used to create these BAM files? (Overestimate if you don't know exactly)"
read genome_length
echo ''
echo "How many pieces should the genome be broken into? Please choose a value less than 500; large values will not show up well as each point requires at least 1 pixel)"
read chunk_size
echo ''
echo "Starting bam_to_heatmap_csv.py"
python bin/coverage_depth_csv.py -i Output/BAM_files/ -o Output/coverage_depth.csv -l $genome_length -n $chunk_size
if [ "$?" -eq "0" ]; then
   echo "Success!";
fi
