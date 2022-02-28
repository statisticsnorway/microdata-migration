import json
import tarfile

"""Generates a dictionary with csv files location within tar files and writes it to disk as json.

    Parameters
    ----------
    output_dir : str
        Where to place the generated file.
        
    Returns
    -------
    Nothing for now
    """

# ------------- runtime parameters --------------
output_dir = "/microdata/migration/data/tar_files"
# ------------- runtime parameters --------------

tar_files_root = "/microdata/migration/data/tar_files"
tar_p1_1 = f'{tar_files_root}/sl-raird-db-p1/sl-raird-db-p1_1.tar'
tar_p1_2 = f'{tar_files_root}/sl-raird-db-p1/sl-raird-db-p1_2.tar'
tar_p2_1 = f'{tar_files_root}/sl-raird-db-p2/sl-raird-db-p2_1.tar'
tar_p2_2 = f'{tar_files_root}/sl-raird-db-p2/sl-raird-db-p2_2.tar'
tar_p3_1 = f'{tar_files_root}/sl-raird-db-p3/sl-raird-db-p3_1.tar'
tar_p3_2 = f'{tar_files_root}/sl-raird-db-p3/sl-raird-db-p3_2.tar'
tar_p4_1 = f'{tar_files_root}/sl-raird-db-p4/sl-raird-db-p4_1.tar'
tar_p4_2 = f'{tar_files_root}/sl-raird-db-p4/sl-raird-db-p4_2.tar'
tar_qa1_1 = f'{tar_files_root}/sl-raird-db-qa1/sl-raird-db-qa1_1.tar'
tar_qa1_2 = f'{tar_files_root}/sl-raird-db-qa1/sl-raird-db-qa1_2.tar'
tar_qa2_1 = f'{tar_files_root}/sl-raird-db-qa2/sl-raird-db-qa2_1.tar'
tar_qa2_2 = f'{tar_files_root}/sl-raird-db-qa2/sl-raird-db-qa2_2.tar'

csv_file_location = {}
for filename in [tar_p1_1, tar_p1_2, tar_p2_1, tar_p2_2, tar_p3_1, tar_p3_2,
                 tar_p4_1, tar_p4_2, tar_qa1_1, tar_qa1_2, tar_qa2_1, tar_qa2_2]:

    print(f'Opens {filename}')
    file_obj = tarfile.open(filename,"r")
    namelist = file_obj.getnames()
    for name in namelist:
        csv_file_location[name] = filename
    file_obj.close()

output_file = f'{output_dir}/csv_file_location.json'
with open(output_file, 'w') as json_file:
    json.dump(csv_file_location, json_file)

print(f'csv_file_location.json generated: {output_file}')
