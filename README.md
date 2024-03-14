# miRNA_targetScan for circRNA
A miRNA targetScan pipeline based on [targetScan](https://www.targetscan.org/vert_80/).
This pipeline is for circRNA and include the back-splicing regions

</br>

# Dependency
* bedtools/2.31.0
* perl/v5.34.0, python3/-

</br>

# Usage
## 1. Prepare input data
* Input data should be a bed file with at least first six columns, including chromosome, start, end, gene_symbol, score(can be any value), strand.
* The example input data can be found ```example/example.bed```
* Notice: The first column, chromosome, should be in the same format with your reference fasta file. e.g, GRCh38 use format chr1 to represent chromosome1, then the first col in your input bed file should be in format chr1 instead of 1.

## 2. Prepare reference
* **Genome assembly reference(fasta)**: Make sure you are using the same reference with any previous steps(e.g. alignment, DCC, circexplorers).
* **Genome annotation exons file(bed format)**: 
    - You can generate one from [annotation gtf file](https://www.gencodegenes.org/human/releases.html).Only exons should be included in the bed file.
    - An example exons bed file looks like this
        ```
        chr1	65626122	65626234	ENSG00000116678.19_exon_18	LEPR	+
        chr1	65619939	65620023	ENSG00000116678.19_exon_1	LEPR	+
        chr1	65621352	65621458	ENSG00000116678.19_exon_2	LEPR	+
        chr1	65622905	65623384	ENSG00000116678.19_exon_3	LEPR	+
        chr1	65486405	65486506	ENSG00000237852.1_exon_1	RP4-630A11.3	+
        chr1	65493866	65494188	ENSG00000237852.1_exon_2	RP4-630A11.3	+
        chr1	65578264	65578380	ENSG00000224570.1_exon_1	RP11-430H12.2	-
        chr1	65576128	65577809	ENSG00000224570.1_exon_2	RP11-430H12.2	-
        ```
    - If you are a BU SCC user, an example can be found at `/restricted/projectnb/casa/mtLin/sambabi/miRNA_targetScan/gencode.v26.primary_assembly.annotation_exons.bed`. Plz remeber to update it to coordinate with your reference version.
* **miRNA library**
    * An out-of-date(?) version is provided at example/miR_Family_info_all.txt
    * Check the [targetScan website](https://www.targetscan.org/cgi-bin/targetscan/data_download.vert80.cgi) to follow the latest one.

## 3.Convert bed file to sequence file(fasta)
```
# go to the root dir of the repo
cd miRNA_targetScan

# prepare result folder
mkdir result

# Convert
python ./scripts/getcircfasta.py -f path/to/GRChXX.primary_assembly.genome.fa -c path/to/input.bed -e path/to/exons.bed -o result/CircRNAseq_no_backsplicing.fa
```

## 4. Add backsplicing regions to sequence file(fasta)
```
python ./scripts/addBackSplicing.py -i ./result/CircRNAseq_no_backsplicing.fa -o ./result/CircRNAseq_with_backsplicing.fa
```

## 5. Target Scan
```
awk 'NR%2{printf "%s ",$0;next;}1' ./result/CircRNAseq_with_backsplicing.fa | awk '{print $4"::"$1":"$2"-"$3,"9606",$9}' | sed 's/>//g' |  awk 'BEGIN{OFS="\t";} {gsub("T","U",$3);print}' >  ./result/CircRNAseq_post.fa

#Run Targetscan
./scripts/targetscan_70.pl path/to/miR_Family_info_all.txt ./result/CircRNAseq_post.fa ./result/CircRNA_targetScan_result.txt
```
* in the `./result/CircRNAseq_post.fa`, we use 9606 as human Species id. If your sample is not human, plz revise it.
* You can replace `path/to/miR_Family_info_all.txt` with `./example/miR_Family_info_all.txt` for test.

</br>

# (Better Option for BU SCC user) All-in-one BU SCC qsub task file
* If you are using BU SCC, you can **hardcode** the `scripts/TargetScanPipeline.sh` and submit the task as a easier way.
* You should modify the `Line 4 - 7` to convey parameters to the pipeline
* Run the pipeline
```
cd scripts
qsub TargetScanPipeline.sh
```


