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
     [
          {
            "name": "AFPO1992FDT_MOTTAK",
            "identifier": "PERSON",
            "measure": null
          },
          {
            "name": "ARBEIDSFORHOLD_PERSON",
            "identifier": "JOBB",
            "measure": "PERSON"
          }
     ] 
   
   
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
get_from_prod = True
output_file = "/Users/vak/temp/pseudo-split/raird_all_tables_unit_type_info.json"
# ------------- runtime parameters --------------

if get_from_prod:
    fdbmetadata_url = "http://pl-raird-app-p2.ssb.no:8085/v.0.2/catalogs/RAIRD/dataSets/<dataset_name>"
else:
    fdbmetadata_url = "http://pl-raird-app-qa2.ssb.no:8085/v.0.2/catalogs/RAIRD/dataSets/<dataset_name>"

with open(database_tables) as f:
    table_list = f.read().splitlines()

metadata = []

for dataset in table_list:
    dataset_name = dataset.split('__')[0]
    dataset_metadata: dict = requests.get(fdbmetadata_url.replace("<dataset_name>", dataset_name)).json()

    if len(dataset_metadata) == 0:
        print(f'{dataset_name} : FDBMetadata returned empty json.')
        continue

    if not any(d['name'] == dataset_name for d in metadata):
        identifier_unit_type = dataset_metadata.get('identifier')[0].get('unitType').get('name')
        if dataset_metadata.get('measure').get('unitType'):
            measure_unit_type = dataset_metadata.get('measure').get('unitType').get('name')
        else:
            measure_unit_type = None

        metadata.append(
            {"name": dataset_name, "identifier": identifier_unit_type, "measure": measure_unit_type}
        )

with open(output_file, "w") as f:
    json.dump(metadata, f, indent=2)