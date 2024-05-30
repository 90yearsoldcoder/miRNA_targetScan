import argparse

def generate_gRNA(sequence, left_arm, right_arm):
    if len(sequence) < left_arm + right_arm:
        raise ValueError("Length of sequence is less than the sum of left and right arms")
    # Generate sequence for the left arm
    left_arm_sequence = sequence[-left_arm:]
    # Generate sequence for the right arm
    right_arm_sequence = sequence[:right_arm]
    # Generate sequence for the gRNA
    gRNA_sequence = left_arm_sequence + right_arm_sequence
    return gRNA_sequence

parser = argparse.ArgumentParser(description="add backsplicing region for CIRCRNA seq")
parser.add_argument("-i", "--input", help="Path to input circRNA seq fasta file", required=True)
parser.add_argument("-o", "--output", help="Path to output circRNA seq fasta file", required=True)
parser.add_argument("-L", "--Left", help="the length of left arm", required=False, default=15)
parser.add_argument("-R", "--Right", help="the length of right arm", required=False, default=15)
args = parser.parse_args()


bsp_length = args.Left + args.Right
with open(args.input, 'r') as input_file, open(args.output, 'w') as output_file:
    cur_gene_line = ""
    for line in input_file:
        output_file.write(line)
        if line.startswith('>'):
            cur_gene_line = line
            continue
        cur_gene_line_sp = cur_gene_line.split('\t')
        cur_gene_line_sp[3] += f"(backsp,{args.Left}+{args.Right})"
        cur_gene_line = "\t".join(cur_gene_line_sp)
        output_file.write(cur_gene_line)
        output_file.write(generate_gRNA(line.strip(), args.Left, args.Right) + "\n")
