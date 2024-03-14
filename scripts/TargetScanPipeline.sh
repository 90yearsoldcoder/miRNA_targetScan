#!/bin/bash -l
# bash TargetScanPipeline.sh CircRNAlist_pde4b 

inputbed=../example/example.bed
ref_fasta=../../GRCh38.primary_assembly.genome.fa
ref_exon=../../casa/mtLin/sambabi/miRNA_targetScan/TargetScanPipeline.sh
miRNA_family_inf=../example/miR_Family_info_all.txt


module load python3
module load bedtools

#prepare result folder
mkdir ../result

#Get CircRNA fasta file
python getcircfasta.py -f ${ref_fasta} -c ${inputbed} -e ${ref_exon} -o ../result/CircRNAseq_no_backsplicing.fa

#Add backSplicing part to fasta
python addBackSplicing.py -i ../result/CircRNAseq_no_backsplicing.fa -o ../result/CircRNAseq_with_backsplicing.fa

#Processed 
awk 'NR%2{printf "%s ",$0;next;}1' ../result/CircRNAseq_with_backsplicing.fa | awk '{print $4"::"$1":"$2"-"$3,"9606",$9}' | sed 's/>//g' |  awk 'BEGIN{OFS="\t";} {gsub("T","U",$3);print}' >  ../result/CircRNAseq_post.fa

#Run Targetscan
targetscan_70.pl ${miRNA_family_inf} ../result/CircRNAseq_post.fa ../result/CircRNA_targetScan_result.txt
