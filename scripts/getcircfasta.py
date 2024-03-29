#! /usr/bin/env python
# This script is aimed to get circRNA exon sequences
#### Iput:
#--- circRNA coordinates
#--- reference genome fasta file
#--- exon annotation bedfile

## NOTICE
# The circRNA coordinates, reference genome and exon annotation should be the same release version,
# the circRNA coordinates should match with exon annotation coordinates, i.e. for chromosome1: chr1 or 1

#### Output: a fasta file with sequence and circRNA coordinates

# import
from pybedtools import BedTool
from optparse import OptionParser

usage = "usage: %prog -f genomefastafile -c circcoordinates -e exonbedfile -o outputfile"
parser = OptionParser(usage=usage)
parser.add_option("-f", "--fasta", dest="fasta",
                  help="The reference genome fasta file")
parser.add_option("-c", "--circ", dest="circ",
                  help="tab delimited circRNA coordinates")
parser.add_option("-e", "--exon", dest="exon",
                  help="tab delimited exon annotation file, bedfile format")
parser.add_option("-m", "--maxL", dest="maxL", type='int', default=int(5000),
                  help="Maximum length of the circRNA exon sequence.")
parser.add_option("-o", "--output", dest="output",
                  help="output circRNA sequence in a fasta format")                  
(options, args) = parser.parse_args()


def getfa(fasta):
    # a string to store fasta sequence
    #print 'NOTE: Remove the duplicated exons in the exon file!'
    regionSet = set() # A set to store the exon regions to avoid duplicates
    seq = ''

    for index, itm in enumerate(fasta):
        if itm.startswith('>'):
            if itm not in regionSet:
                seq=seq+fasta[index+1].strip('\n')
                regionSet.add(itm)
                
    return seq

# read the circRNA one by one
circfile = open(options.circ).read().splitlines()
annotation = BedTool(options.exon)
fasta = BedTool(options.fasta)

def intersectCirc(circfile,annotation,fasta):
    output = open(options.output,'w')
    
    for itm in circfile:
        circ = BedTool([itm])
        a = annotation.intersect(circ, s = True)
        #print(len(a))
        a = a.sequence(fi=fasta, s = True)
        fa = open(a.seqfn).readlines()
        seq = getfa(fa)
        
        if len(seq) < options.maxL:
            # write in a fasta format
            output.write('>' +itm + '\n')
            output.write(seq+'\n')
            
    output.close()
        
intersectCirc(circfile=circfile,annotation=annotation,fasta=fasta)
