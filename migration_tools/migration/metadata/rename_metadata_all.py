import os

""" Renames all metadata-all files in given directory:
    From metadata_all__14.0.0.0.json to metadata_all__14_0_0.json 
"""

def to_underscored_version(version: str) -> str:
    if version.count('.') > 2:
        version = '.'.join(version.split('.')[:-1])
    version = version.replace('.', '_')
    return version


def main():

    folder = "/Users/vak/temp/metadata-all-prod"
    for count, filename in enumerate(os.listdir(folder)):
        if filename.startswith("metadata_all__"):
            version = filename.removeprefix("metadata_all__").removesuffix(".json")
            src =f"{folder}/{filename}"
            dst =f"{folder}/{'metadata_all__'}{to_underscored_version(version)}.json"
            print (src)
            print (dst)
            os.rename(src, dst)


if __name__ == '__main__':
    main()
