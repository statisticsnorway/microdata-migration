import requests
import json

"""Takes a file with all database table names and creates a json file with a unique list
   of all variables and their unit types.
    
   Example database tables input file:
     AFPO1992FDT_MOTTAK__1_0
     AFPO2011FDT_GRAD__1_0
     AFPO2011FDT_GRAD__3_0
     ....
     
   Example of output file:  
   
   result_dict = {
    "VARIABLE_NAME":[
            {"dataset": "VARIABLE_NAME__1_0", "identifier" : "PERSON", "measure": null, "format": null},
            {"dataset": "VARIABLE_NAME__2_0", "identifier" : "PERSON", "measure": null, "format": null},
            {"dataset": "VARIABLE_NAME__3_0", "identifier" : "PERSON", "measure": null, "format": null}
        ]
    }
   
   
    Parameters
    ----------
    database_tables : str
        The input file.
    get_from_prod : Boolean
        Where to get the metadata from. True for production, False for qa.
    output_file : str
        The output file.

    Returns
    -------
    Nothing for now
    """

# ------------- runtime parameters --------------
database_tables = "/Users/vak/temp/pseudo-split/raird_all_tables-db-p1_2022-06-01.txt"
get_from_prod = False
output_file = "/Users/vak/temp/pseudo-split/raird_all_tables_unit_type_info.json"
# ------------- runtime parameters --------------

if get_from_prod:
    fdbmetadata_url = "http://pl-raird-app-p2.ssb.no:8085/v.0.2/catalogs/RAIRD/dataSets/<dataset_name>?version=<dataset_version>"
else:
    fdbmetadata_url = "http://pl-raird-app-qa2.ssb.no:8085/v.0.2/catalogs/RAIRD/dataSets/<dataset_name>?version=<dataset_version>"

with open(database_tables) as f:
    table_list = f.read().splitlines()

result_dict = {}

for dataset in table_list:
    dataset_name = dataset.split('__')[0]
    dataset_version = f'{dataset.split("__")[1].replace("_", ".")}.0'
    url = fdbmetadata_url.replace("<dataset_name>", dataset_name).replace("<dataset_version>", dataset_version)

    dataset_metadata: dict = requests.get(url).json()

    if len(dataset_metadata) == 0:
        print(f'{dataset} : FDBMetadata returned empty result.')
        continue

    identifier_unit_type = dataset_metadata.get('identifier')[0].get('unitType').get('name')

    if dataset_metadata.get('measure').get('unitType'):
        measure_unit_type = dataset_metadata.get('measure').get('unitType').get('name')
    else:
        measure_unit_type = None

    if dataset_metadata.get('measure').get('format'):
        measure_format = dataset_metadata.get('measure').get('format')
    else:
        measure_format = None

    if dataset_name in result_dict:
        result_dict[dataset_name].append(
            {"dataset": dataset, "identifier": identifier_unit_type, "measure": measure_unit_type,
             "format": measure_format}
        )
    else:
        result_dict[dataset_name] = [
            {"dataset": dataset, "identifier": identifier_unit_type, "measure": measure_unit_type,
             "format": measure_format}
        ]

with open(output_file, "w") as f:
    json.dump(result_dict, f, indent=2)