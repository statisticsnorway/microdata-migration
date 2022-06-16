import os
import json

"""Reads the name of csv files in a directory and produces a bash script with conversion command for each file.
   Looks into corresponding json file for temporality and data type.

    Parameters
    ----------
    csv_files_dir : str
        Directory with csv files to be converted to parquet.
    metadata_files_dir : str
        Directory with json files needed for conversion to parquet.
    bash_file_dir : str
        Directory to place the generated bash script.
    workspace : str
        The directory where converting til parquet takes place.
        We need it here to make sure unneeded files are deleted after conversion
        (csv and enhanced csv)    
        
    Returns
    -------
    Nothing for now
    """

# ------------- runtime parameters --------------
csv_files_dir = "/Users/vak/projects/github/M.2.0/microdata-migration/migration_tools/tests/resources/parquet/csv"
metadata_all_files_dir = "/Users/vak/projects/github/M.2.0/microdata-migration/migration_tools/tests/resources/parquet/metadata"
bash_file_dir = "/Users/vak/projects/github/M.2.0/microdata-migration/migration_tools/tests/resources/parquet/bash"
workspace = "/microdata/migration/data/workspace"


# ------------- runtime parameters --------------


def extract_version_from(metadata_all_file: str):
    split_base = metadata_all_file.split("__")
    metadata_all_version = f'{split_base[1].split(".")[0]}_{split_base[1].split(".")[1]}'
    return metadata_all_version


def is_patch_version(metadata_all_file: str):
    split_base = metadata_all_file.split("__")
    if split_base[1].split(".")[2] != "0" or split_base[1].split(".")[3] != "0":
        return True
    return False


def to_enhanced(csv_file_name: str):
    return f'{csv_file_name.split(".")[0]}_enhanced.csv'


# 1. Reads temporality and data type for all datasets from all versions into dictionary in memory
all_datasets_in_all_versions = {}
for root, dirs, files in os.walk(metadata_all_files_dir):
    metadata_all_file_name: str
    for metadata_all_file_name in files:
        if is_patch_version(metadata_all_file_name):
            continue
        print(f'Reads temporality and dataType from all datasets in {metadata_all_file_name}')
        metadata_all_file_version = extract_version_from(metadata_all_file_name)
        metadata_all_file_path = f'{metadata_all_files_dir}/{metadata_all_file_name}'
        with open(metadata_all_file_path) as json_file:
            json_dict = json.load(json_file)
            dataStructures = json_dict['dataStructures']
            for dataset in dataStructures:
                dataset_name = dataset['name']
                temporality = dataset['temporality'].upper()
                data_type = dataset['measureVariable']['dataType'].upper()

                key = f'{dataset_name}__{metadata_all_file_version}'
                value = {'temporality': temporality, 'data_type': data_type}
                all_datasets_in_all_versions[key] = value

print('Metadata dict loaded in memory ...')

with open("../templates/convert_to_parquet.template") as f:
    convert_to_parquet_template = f.read().splitlines()

# 2. Checks metadata dictionary for each csv file and writes the command to bash script
cmd_list = []
for root, dirs, files in os.walk(csv_files_dir):
    csv_file_name: str
    for csv_file_name in files:
        dataset_name_and_version = csv_file_name.split('.')[0]
        if dataset_name_and_version in all_datasets_in_all_versions:
            metadata = all_datasets_in_all_versions[dataset_name_and_version]
            temporality = metadata['temporality']
            data_type = metadata['data_type']
            convert_commands = map(lambda line: line.replace('<TEMPORALITY>', temporality)
                                   .replace('<DATATYPE>', data_type)
                                   .replace('<CSV_FILE_NAME>', csv_file_name)
                                   .replace('<ENHANCED_CSV_FILE_NAME>', to_enhanced(csv_file_name))
                                   .replace('<WORKSPACE>', workspace),
                                   convert_to_parquet_template)
            cmd_list.extend(list(convert_commands))
            continue
        print(f'{dataset_name_and_version} not found in any of metadata_all files')

bash_script_path = f'{bash_file_dir}/convert_to_parquet.sh'
with open(bash_script_path, mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(list(cmd_list)))

print(f'Bash script generated: {bash_script_path}')
