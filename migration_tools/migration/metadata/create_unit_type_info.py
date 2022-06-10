import requests
import json

"""Takes a file with all database table names and creates a text file with a unique list
   of all variables and their unit types.
    
   Example database tables input file:
     AFPO1992FDT_MOTTAK__1_0
     AFPO2011FDT_GRAD__1_0
     AFPO2011FDT_GRAD__3_0
     ....
     
   Example of output file:
   
    AFPO1992FDT_MOTTAK__1_0, ident.UnitType: PERSON, measure.UnitType: None, measure.format: None
    AFPO2011FDT_GRAD__1_0, ident.UnitType: PERSON, measure.UnitType: None, measure.format: None
    AFPO2011FDT_GRAD__3_0, ident.UnitType: PERSON, measure.UnitType: None, measure.format: None
   
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
output_file = "/Users/vak/temp/pseudo-split/raird_all_tables_unit_type_info.txt"
# ------------- runtime parameters --------------

if get_from_prod:
    fdbmetadata_url = "http://pl-raird-app-p2.ssb.no:8085/v.0.2/catalogs/RAIRD/dataSets/<dataset_name>?version=<dataset_version>"
else:
    fdbmetadata_url = "http://pl-raird-app-qa2.ssb.no:8085/v.0.2/catalogs/RAIRD/dataSets/<dataset_name>?version=<dataset_version>"

with open(database_tables) as f:
    table_list = f.read().splitlines()

metadata = []

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

    metadata.append(f'{dataset}, ident.UnitType: {identifier_unit_type}, '
                    f'measure.UnitType: {measure_unit_type}, measure.format: {measure_format}')

with open(output_file, 'w') as f:
    f.write('\n'.join(metadata))