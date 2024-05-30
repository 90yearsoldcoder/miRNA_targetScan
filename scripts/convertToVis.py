import re
import json

fasta_path = "../result/CircRNAseq_post.fa"
targetScan_path = "../result/CircRNA_targetScan_result.txt"
bsp_left = 15
bsp_right = 15
gene_type = 'circular'
anno_type = "miRNA"
output_path = "../result/vis_data.json"

dic_anno2key = {}
cur_key = 0


def parseFastaLine(line: str):
    line_sp = line.strip().split('\t')
    gene = line_sp[0]
    #print(gene)
    if "backsp" in gene:
        return None
    seq = line_sp[-1]
    return (gene, seq)

def readFasta(dic, fasta_path):
    with open(fasta_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp = parseFastaLine(line)
            if tmp == None:
                continue
            gene, seq = tmp
            if gene in dic:
                print(f'${gene} is reduplicate')
            dic[gene] = {}
            dic[gene]['type'] = gene_type
            dic[gene]['seq'] = seq
            dic[gene][anno_type] = []


def parseTargetScanRe(line, dic):
    line_sp = line.strip().split('\t')

    backsp_flag = True if 'backsp' in line_sp[0] else False

    gene = re.sub(r'\(backsp,15\+15\)', '', line_sp[0])
    anno_name = line_sp[1]
    st = int(line_sp[3])
    ed = int(line_sp[4])
    l = len(dic[gene]['seq'])

    if backsp_flag:
        st = l - (bsp_left - st)
        ed = ed - bsp_left
    addAnnotationToDic(dic, gene, anno_name, st, ed)

def addAnnotationToDic(dic, gene, anno_name, st, ed):
    global cur_key
    #print(gene, anno_name, st, ed)
    collection = dic[gene][anno_type]
    for item in collection:
        if item["name"] == anno_name:
            item['count'] += 1
            item['positions'].append([st, ed])
            return
    
    if anno_name not in dic_anno2key:
        dic_anno2key[anno_name] = cur_key
        cur_key += 1

    collection.append({
        "name": anno_name,
        "key": dic_anno2key[anno_name],
        "count": 1,
        "positions": [
          [st, ed],
        ]
    })


def readTargetScanRe(dic, targetScan_path):
    with open(targetScan_path, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parseTargetScanRe(line, dic)

if __name__ == "__main__":
    dic = {}
    readFasta(dic, fasta_path)
    #print(dic)
    readTargetScanRe(dic, targetScan_path)

    with open(output_path, 'w') as json_file:
        json.dump(dic, json_file, indent=4)