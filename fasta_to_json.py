import argparse
import json

# 定义读取 FASTA 文件的函数
def read_fasta_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def process_fasta_and_generate_json(input_path, output_path):
    # 读取 FASTA 文件
    fasta_content = read_fasta_file(input_path)

    # 处理 FASTA 数据
    fasta_lines = fasta_content.split('\n')
    formatted_fasta = ""
    for line in fasta_lines:
        if line.startswith('>'):
            if formatted_fasta:
                formatted_fasta += '\n'
            formatted_fasta += line + '\n'
        else:
            formatted_fasta += line 

    # 创建 JSON 结构
    json_data = {
        "input_sequence_text": formatted_fasta,
        "peptide_length_range": [8, 9, 10],
        "alleles": "HLA-A*02:01,HLA-A*01:01,HLA-A*02:03,HLA-A*02:06,HLA-A*03:01,HLA-A*11:01,HLA-A*23:01,HLA-A*24:02,HLA-A*26:01,HLA-A*30:01,HLA-A*30:02,HLA-A*31:01,HLA-A*32:01,HLA-A*33:01,HLA-A*68:01,HLA-A*68:02,HLA-B*07:02,HLA-B*08:01,HLA-B*15:01,HLA-B*35:01,HLA-B*40:01,HLA-B*44:02,HLA-B*44:03,HLA-B*51:01,HLA-B*53:01,HLA-B*57:01,HLA-B*58:01",
        "predictors": [
            {
                "type": "binding",
                "method": "netmhcpan_el"
            },
            {
                "type": "processing",
                "method": "basic_processing",
                "mhc_binding_method": "netmhcpan_ba",
                "proteasome": "immuno",
                "tap_precursor": 1,
                "tap_alpha": 0.2
            },
            {
                "type": "immunogenicity",
                "mask_choice": "default"
            }
        ]
    }

    # 写入 JSON 文件
    with open(output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"JSON 文件已成功创建并写入数据到 {output_path}。")

# 设置命令行参数解析
parser = argparse.ArgumentParser(description='Process FASTA files and output JSON.')
parser.add_argument('input_fasta', help='Path to the input FASTA file')
parser.add_argument('output_json', help='Path to the output JSON file')

# 解析命令行参数
args = parser.parse_args()

# 调用函数
process_fasta_and_generate_json(args.input_fasta, args.output_json)

