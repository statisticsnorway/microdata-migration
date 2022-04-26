import sys
import json
import datetime

"""Creates a datastore_versions.json

    Parameters
    ----------
    Parameters are hardcoded in main:
    input_file : str
        A file with the response of http://{{fdbmetadata}}/v.0.2/catalogs/RAIRD/dataStoreVersions
    output_file : str
        The file to be created

    Returns
    -------
    Nothing for now
    """


def __to_seconds_since_epoch(releaseTime: str):
    dt = datetime.datetime.strptime(releaseTime, '%Y-%m-%d %H:%M:%S')
    return round(dt.timestamp())


def __transform_version(from_version):

    datastructure_updates = []
    for data_revision in from_version["dataRevision"]:
        datastructure = {
            "name": data_revision["name"],
            "description": data_revision["description"],
            "releaseStatus": data_revision["releaseStatus"],
            "operation": data_revision["operationType"],
        }
        datastructure_updates.append(datastructure)

    transformed_version = {
        "version": f'{from_version["version"]}.0',
        "description": from_version["description"],
        "releaseTime": __to_seconds_since_epoch(from_version["releaseTime"]),
        "languageCode": "no",
        "dataStructureUpdates": datastructure_updates
    }
    return transformed_version


def create_datastore_versions(input_file: str, output_file: str):

    with open(input_file) as f:
        versions_15 = json.load(f)

    list_of_versions = []
    for from_version in versions_15:
        list_of_versions.append(__transform_version(from_version))

    datastore_versions = {"name": "no.ssb.fdb.m2",
                          "label": "Migrert no.ssb.fdb",
                          "description": "Migrert datastore fra microdata 1.5 opp til v. 14",
                          "versions": list_of_versions}

    with open(output_file, "w") as f:
        json.dump(datastore_versions, f, indent=2)
    print (f'New datastore_versions file: {output_file}')


def main(argv):
    input_file = "/Users/vak/temp/dataStoreVersions_14_0_0_fra_prod_pp.json"
    output_file = "/Users/vak/temp/datastore_versions_14_0_0_0_M2.json"
    create_datastore_versions(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])