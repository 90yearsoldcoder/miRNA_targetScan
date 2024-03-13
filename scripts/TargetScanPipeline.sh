#!/bin/bash -l
# bash TargetScanPipeline.sh CircRNAlist_pde4b 

inputbed=../example/example.bed
ref_fasta=../../GRCh38.primary_assembly.genome.fa
ref_exon=../../casa/mtLin/sambabi/miRNA_targetScan/TargetScanPipeline.sh


module load python3
module load bedtools

#prepare result folder
mkdir ../result

#Get CircRNA fasta file
python getcircfasta.py -f ${ref_fasta} -c ${inputbed} -e ${ref_exon} -o ../result/CircRNAseq_no_backsplicing.fa

#Processed 
awk 'NR%2{printf "%s ",$0;next;}1' CircRNAlist.fa | awk '{print $4"::"$1":"$2"-"$3,"9606",$9}' | sed 's/>//g' |  awk 'BEGIN{OFS="\t";} {gsub("T","U",$3);print}' >  CircRNAlist_pro.fa

#Run Targetscan
targetscan_70.pl miR_Family_info_all.txt CircRNAlist_pro.fa ${1}_result
