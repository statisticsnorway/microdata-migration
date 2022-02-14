import requests
import json


"""Creates a metadata_all file for each datastore version, either from qa or prod env.

    Parameters
    ----------
    get_from_prod : Boolean
        Where to get the files from. True for production, False for qa.
    output_dir : str
        The output directory.

    Returns
    -------
    Nothing for now
    """

# ------------- runtime parameters --------------
get_from_prod = True
output_dir = "/Users/vak/temp/metadata-all-prod"
# ------------- runtime parameters --------------

if get_from_prod:
    data_store_url = "http://pl-raird-app-p2.ssb.no:8084/metadata/data-store"
    metadata_all_str = "http://pl-raird-app-p2.ssb.no:8084/metadata/all?version=<placeholder>"
else:
    data_store_url = "http://pl-raird-app-qa2.ssb.no:8084/metadata/data-store"
    metadata_all_str = "http://pl-raird-app-qa2.ssb.no:8084/metadata/all?version=<placeholder>"

data_store_dict = requests.get(data_store_url).json()

for dic in data_store_dict["versions"]:
    for key in dic:
        version_value = dic[key]
        if key == "version" and not version_value.startswith('0.0.0'):
            metadata_all_url = metadata_all_str.replace("<placeholder>", version_value)
            print (metadata_all_url)
            metadata_all_dict = requests.get(metadata_all_url).json()

            json_file = f"{output_dir}/metadata_all__{version_value}.json"
            print(json_file)
            j = json.dumps(metadata_all_dict, indent=4)
            f = open(json_file, 'w')
            print(j, file=f)
            f.close()
