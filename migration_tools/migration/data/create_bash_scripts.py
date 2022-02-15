import os

"""Creates sql and bash scripts from a list of tables.

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
tables_file = "/Users/vak/temp/raird_all_tables.txt"
number_of_tables_in_bash_script = 10
output_dir = "/Users/vak/temp/sql_dump_files"
# ------------- runtime parameters --------------

with open(tables_file) as f:
    table_list = f.read().splitlines()

with open("sql_table_dump.template") as f:
    table_dump_template = f.read().splitlines()

for table_name in table_list:
    transformed_table_dump = map(lambda line: line.replace('<PLACEHOLDER>', table_name), table_dump_template)
    file_path = f'{output_dir}/dump_{table_name}.sql'
    with open(file_path, mode='wt', encoding='utf-8') as sqlfile:
        sqlfile.write('\n'.join(list(transformed_table_dump)))


with open("sh_script.template") as f:
    script_template = f.read().splitlines()

i = 0
script_number = 0
sh_script = []

for root, dirs, files in os.walk(output_dir):
    for filename in files:
        if not filename.startswith("dump"):
            continue
        transformed_script = map(lambda line: line.replace('<PLACEHOLDER>', filename), script_template)
        sh_script.extend(list(transformed_script))
        i += 1
        if i != number_of_tables_in_bash_script:
            continue
        i = 0
        script_number += 1
        file_path = f'{output_dir}/dump_tables_{script_number}.sh'
        with open(file_path, mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(sh_script))
        sh_script = []

if len(sh_script) > 0:
    file_path = f'{output_dir}/dump_tables_{script_number + 1}.sh'
    with open(file_path, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(sh_script))
