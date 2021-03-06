import getopt
import sys
import json

# Appends a new variable to a metadata_all json file.

def append_metadata_all(metadata_file: str, metadata_all_file: str):
    with open(metadata_file) as f:
        dataset = json.load(f)
    with open(metadata_all_file) as f:
        metadata_all = json.load(f)

    if isinstance(dataset, list):
        metadata_all["dataStructures"].append(dataset[0])
    else:
        metadata_all["dataStructures"].append(dataset)

    metadata_all_enriched_file = metadata_all_file.replace(".json", "_enriched.json")
    with open(metadata_all_enriched_file, "w") as f:
        json.dump(metadata_all, f, indent=2)
    print (f'New metadata-all file: {metadata_all_enriched_file}')


def get_user_input(argv):
    command = 'append_metadata_all.py -v <metadata.json> -m <metadata-all.json>'
    try:
        opts, args = getopt.getopt(
            argv, "hv:m:", ["metadata=", "metadata-all="]
        )
        if not opts:
            print(command)
            sys.exit()
    except getopt.GetoptError:
        print(command)
        sys.exit(2)
    for opt, value in opts:
        if opt == '-h':
            print('Appends metadata-all with metadata from a json file\n')
            print(command)
            sys.exit()
        elif opt in ("-v", "--metadata"):
            metadata_file = value
        elif opt in ("-m", "--metadata-all"):
            metadata_all_file = value
    return metadata_file, metadata_all_file


def main(argv):
    metadata_file, metadata_all_file = get_user_input(argv)
    append_metadata_all(metadata_file, metadata_all_file)


if __name__ == "__main__":
    main(sys.argv[1:])