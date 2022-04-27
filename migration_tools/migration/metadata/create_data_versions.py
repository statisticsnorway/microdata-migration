import sys
import json

"""Creates a list of files named data_versions__<major>_<minor>_<patch>_0.json

    Parameters
    ----------
    Parameters are hardcoded in main:
    
    datastore_versions_file : str
        A json file with the response of http://{{fdbmetadata}}/v.0.2/catalogs/RAIRD/dataStoreVersions
    
    table_names_file : str
        A file created by /home/vak/sql/dump_all_table_names.sql on sl-raird-db-p1 
    
    data_directory_tree_file : str
        A json file showing the structure of data direcorty in a datastore. Can be produced like this:
            [vak@sl-mdata-app-p1 data]$ pwd
            /microdata/datastores/NO-SSB-FDB/data
            [vak@sl-mdata-app-p1 data]$ tree -J > data_directory_tree.json
        This file is needed in order to detect weather a dataset is partitioned or not.    
            
    output_dir : The directory where files are created
    
    Returns
    -------
    Nothing for now
    """

error_msg_list = []

def __sort_table_list(list_of_tables: list):
    list_of_tables.sort(key=lambda x: (int((x.split("__")[1]).split("_")[0]), int((x.split("__")[1]).split("_")[1])),
                        reverse=True)

def __find_parquet_file_or_directory(data_directory_tree: list, dataset_name: str, version: str):
    dataset_name_and_version = f'{dataset_name}__{version}'

    directory_structure = data_directory_tree[0]
    contents = directory_structure["contents"]

    dataset_directory = next((item for item in contents if item["name"] == dataset_name), None)
    if dataset_directory:
        directory_contents = dataset_directory["contents"]
        parquet_dir = next((item for item in directory_contents if item["name"] == dataset_name_and_version), None)
        parquet_file = next((item for item in directory_contents if item["name"] == f'{dataset_name_and_version}.parquet'), None)
        if parquet_dir:
            return parquet_dir["name"]
        elif parquet_file:
            return parquet_file["name"]
        else:
            error_msg_list.append(f'{dataset_name_and_version} : Nor partitioned directory neither single parquet file found.')
    else:
        error_msg_list.append(f'{dataset_name} : A database table with this name exists but there are no metadata for this dataset.')


def create_data_versions(datastore_versions_file: str, table_names_file: str, data_directory_tree_file: str, output_dir: str):
    with open(datastore_versions_file) as f:
        datastore_versions = json.load(f)

    with open(data_directory_tree_file) as f:
        data_directory_tree = json.load(f)

    with open(table_names_file) as f:
        table_list = f.read().splitlines()
    __sort_table_list(table_list)

    for datastore_version in datastore_versions:
        version = datastore_version["version"]
        filename = f'{output_dir}/data_versions__{version.replace(".", "_")}_0.json'

        datastore_version_major = int(version.split(".")[0])
        datastore_version_minor = int(version.split(".")[1])

        data_versions_dict = {}
        for table in table_list:
            table_name = table.split('__')[0]
            table_version = table.split('__')[1]
            table_version_major = int(table_version.split("_")[0])
            table_version_minor = int(table_version.split("_")[1])

            if table_version == '0_0':
                continue
            if table_name in data_versions_dict.keys():
                continue

            if datastore_version_major >= table_version_major:
                if datastore_version_major == table_version_major:
                    if datastore_version_minor >= table_version_minor:
                        data_versions_dict[table_name] = \
                            __find_parquet_file_or_directory(data_directory_tree, table_name, table_version)
                else:
                    data_versions_dict[table_name] = \
                        __find_parquet_file_or_directory(data_directory_tree, table_name, table_version)

        with open(filename, "w") as f:
            json.dump(data_versions_dict, f, indent=2)

    log = list(set(error_msg_list))
    for element in log:
        print(element)


def main(argv):
    datastore_versions_file = "/Users/vak/temp2/datastoreVersions-prod_up_to_14_0_0_pp.json"
    table_names_file = "/Users/vak/temp2/raird_all_tables-db-p1_up_to_14_0_0.txt"
    data_directory_tree_file = "/Users/vak/temp2/data_directory_tree.json"

    output_dir = "/Users/vak/temp2/data_versions"
    create_data_versions(datastore_versions_file, table_names_file, data_directory_tree_file, output_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
