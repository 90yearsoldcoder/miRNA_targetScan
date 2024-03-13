# miRNA_targetScan for circRNA
A miRNA targetScan pipeline based on [targetScan](https://www.targetscan.org/vert_80/).
This pipeline is for circRNA and include the back-splicing regions

# Dependency
bedtools

python3

# Usage
## 1. Prepare input data
* Input data should be a bed file with at least first five columns, including chromosome, start, end, gene_symbol, score(can be any value), strand.
* The example input data can be found ```example/example.bed```
* Notice: The first column, chromosome, should be in the same format with your reference fasta file. e.g, GRCh38 use format chr1 to represent chromosome1, then the first col in your input bed file should be in format chr1 instead of 1.

## 2. Prepare reference
* Genome assembly reference(fasta). Make sure you are using the same reference with any previous steps(e.g. alignment, DCC, circexplorers).
* Genome annotation exons files(bed format). 
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
    - If you are a BU SCC user, an example can found at `/restricted/projectnb/casa/mtLin/sambabi/miRNA_targetScan/gencode.v26.primary_assembly.annotation_exons.bed`. Plz remeber to update it to coordinate with your reference version.

## 3.Convert bed file to sequence file(fasta)
```
# go to the root dir of the repo
cd miRNA_targetScan

# prepare result folder
mkdir result

# Convert
python ./scripts/getcircfasta.py -f path/to/GRChXX.primary_assembly.genome.fa -c path/to/input.bed -e path/to/exons.bed -o result/CircRNAseq_no_backsplicing.fa
```

# temp block(remove after developing)
```
python ./scripts/getcircfasta.py -f ../GRCh38.primary_assembly.genome.fa -c ./example/example.bed -e ../gencode.v26.primary_assembly.annotation_exons.bed -o result/CircRNAseq_no_backsplicing.fa
```


