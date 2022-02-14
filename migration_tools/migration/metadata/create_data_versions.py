import sys
import json

"""Creates a list of files named data_versions__<major>_<minor>_<patch>.json

    Parameters
    ----------
    Parameters are hardcoded in main:
    datastore_versions_file : str
        A file with the respons of http://{{fdbmetadata}}/v.0.2/catalogs/RAIRD/dataStoreVersions
    table_names_file : str
        A file created by script on db-qa1 /home/vak/sql/create_all_tables.sql 
        (uncertain, citrix is down right now, will check it out)
    output_dir : The directory where files are created   

    Returns
    -------
    Nothing for now
    """


def __sort_table_list(list_of_tables: list):
    list_of_tables.sort(key=lambda x: (int((x.split("__")[1]).split("_")[0]), int((x.split("__")[1]).split("_")[1])),
                        reverse=True)


def create_data_versions(datastore_versions_file: str, table_names_file: str, output_dir: str):
    with open(datastore_versions_file) as f:
        datastore_versions = json.load(f)

    with open(table_names_file) as f:
        table_list = f.read().splitlines()
    __sort_table_list(table_list)

    for datastore_version in datastore_versions:
        version = datastore_version["version"]
        filename = f'{output_dir}/data_versions__{version.replace(".", "_")}.json'

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
                        data_versions_dict[table_name] = f'{table}.parquet'
                else:
                    data_versions_dict[table_name] = f'{table}.parquet'

        with open(filename, "w") as f:
            json.dump(data_versions_dict, f, indent=2)


def main(argv):
    datastore_versions_file = "/Users/vak/temp/datastoreVersions-prod.json"
    table_names_file = "/Users/vak/temp/raird_all_tables.txt"
    output_dir = "/Users/vak/temp/data_versions"
    create_data_versions(datastore_versions_file, table_names_file, output_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
