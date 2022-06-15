import json
import os
import tarfile

"""Creates sql and bash scripts from a list of tables with unit type information.
 The scripts are used to distribute id's to pseudo tables partitioned by unit_type_id 
 Packs scripts into tar files.

    Parameters
    ----------
    tables_file : str
        Where to find the list of tables to dump.
    number_of_tables_in_bash_script : int
        There will be generated a number of shell scripts, where each script will contain this number of table dumps.
    output_dir : str    
        The directory to find the files generated.
        
    Returns
    -------
    Nothing for now
    """

# ------------- runtime parameters --------------
tables_file = "/Users/vak/projects/github/M.2.0/microdata-migration/migration_files/" \
              "raird_all_tables_unit_type_info_modified.json"
number_of_tables_in_bash_script = 100
output_dir = "/Users/vak/temp/pseudo_partition_files"
# ------------- runtime parameters --------------

# 1. Creates sql files
with open(tables_file) as json_file:
    table_dict = json.load(json_file)

with open("../templates/append_to_pseudo_partition.tamplate") as f:
    append_to_partition_template = f.read().splitlines()

# <PLACEHOLDER_PARTITION>
# <PLACEHOLDER_TABLE_NAME>

unit_type_to_unit_id = {
    "KURSID_1": "KURSID",
    "PERSONID_1": "FNR",
    "KJORETOY_ID": "KJORETOY_ID",
    "JOBBID_1": "JOBBID_1",
    "JOBB": "JOBBID_1",
    "KJORETOY": "KJORETOY_ID",
    "FAMILIE": "FNR",
    "FORETAK": "ORGNR",
    "HUSHOLDNING": "FNR",
    "KURS": "KURSID",
    "PERSON": "FNR",
    "VIRKSOMHET": "ORGNR"
}

for table_instance in table_dict:

    list_of_tables = table_dict[table_instance]

    for table in list_of_tables:
        table_name = table["dataset"]
        identifier_unit_id = table["identifier"]
        measure_unit_id = table["measure"]

        if identifier_unit_id in unit_type_to_unit_id:
            unit_type_id = unit_type_to_unit_id[identifier_unit_id]
            transformed_template = \
                map(lambda line:
                    line.replace('<PLACEHOLDER_TABLE_NAME>', table_name)
                    .replace('<PLACEHOLDER_PARTITION>', unit_type_id)
                    .replace('<PLACEHOLDER_COLUMN>', "unit_id"),
                    append_to_partition_template)
            file_path = f'{output_dir}/append_{table_name}_{unit_type_id}_identifier.sql'
            with open(file_path, mode='wt', encoding='utf-8') as sqlfile:
                sqlfile.write('\n'.join(list(transformed_template)))
        else:
            print(f'{table_name} has unknown unit type in identifier: {identifier_unit_id}')

        if measure_unit_id in unit_type_to_unit_id:
            unit_type_id = unit_type_to_unit_id[measure_unit_id]
            transformed_template = \
                map(lambda line:
                    line.replace('<PLACEHOLDER_TABLE_NAME>', table_name)
                    .replace('<PLACEHOLDER_PARTITION>', unit_type_id)
                    .replace('<PLACEHOLDER_COLUMN>', "value"),
                    append_to_partition_template)
            file_path = f'{output_dir}/append_{table_name}_{unit_type_id}_measure.sql'
            with open(file_path, mode='wt', encoding='utf-8') as sqlfile:
                sqlfile.write('\n'.join(list(transformed_template)))

# 2. Creates sh files
# with open("sh_script.template") as f:
#     script_template = f.read().splitlines()
#
# i = 0
# script_number = 0
# sh_script = []
#
# for root, dirs, files in os.walk(output_dir):
#     for filename in files:
#         if not filename.startswith("dump"):
#             continue
#         transformed_template = map(lambda line: line.replace('<SQL_SCRIPT>', filename), script_template)
#         sh_script.extend(list(transformed_template))
#         i += 1
#         if i != number_of_tables_in_bash_script:
#             continue
#         i = 0
#         script_number += 1
#         file_path = f'{output_dir}/dump_tables_{script_number}.sh'
#         transformed_script = map(lambda line: line.replace('<LOG_FILE>', f'dump_tables_{script_number}.log'), sh_script)
#         with open(file_path, mode='wt', encoding='utf-8') as myfile:
#             myfile.write('\n'.join(list(transformed_script)))
#         sh_script = []
#
# if len(sh_script) > 0:
#     script_number += 1
#     file_path = f'{output_dir}/dump_tables_{script_number}.sh'
#     transformed_script = map(lambda line: line.replace('<LOG_FILE>', f'dump_tables_{script_number}.log'), sh_script)
#     with open(file_path, mode='wt', encoding='utf-8') as myfile:
#         myfile.write('\n'.join(list(transformed_script)))
#
# # 3. Creates tar files
# os.chdir(output_dir)
# script_counter = 0
# for file in os.listdir('.'):
#     if file.endswith(".sh"):
#         script_counter += 1
#         tar_file = tarfile.open(f'sh_script_{script_counter}.tar', "w")
#         tar_file.add(file)
#         sh_file = open(file, 'r')
#         lines = sh_file.readlines()
#
#         for line in lines:
#             if line.startswith('#'):
#                 sql_file = f'{line.split("# ")[1].strip()}'
#                 tar_file.add(sql_file)
#         tar_file.close()
