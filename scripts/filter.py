import json
vis_data = "../result/vis_data.json"
miRNA_Count_cut_off = 3
output_path = "../result/vis_data_filtered.json"


# Read JSON file and convert it to a dictionary
with open(vis_data, 'r') as json_file:
    data_dict = json.load(json_file)

for gene in data_dict:
    after_filter = []
    for data in data_dict[gene]['miRNA']:
        if data['count'] >= miRNA_Count_cut_off:
            after_filter.append(data)
    data_dict[gene]['miRNA'] = after_filter

with open(output_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)