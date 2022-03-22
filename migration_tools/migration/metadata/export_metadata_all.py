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

released_versions = [
    dic["version"] for dic in data_store_dict["versions"]
    if not dic["version"].startswith('0.0.0')
]


def to_underscored_version(version: str) -> str:
    if version.count('.') > 2:
        version = '.'.join(version.split('.')[:-1])
    version = version.replace('.', '_')
    return version


for version in released_versions:
    metadata_all_url = metadata_all_str.replace("<placeholder>", version)
    print(metadata_all_url)
    metadata_all_dict = requests.get(metadata_all_url).json()

    json_file_path = f"{output_dir}/metadata_all__{to_underscored_version(version)}.json"
    print(json_file_path)

    with open(json_file_path, 'w') as f:
        json.dump(metadata_all_dict, f, indent=2)
