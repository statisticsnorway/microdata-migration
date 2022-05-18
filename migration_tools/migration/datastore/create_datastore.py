import getopt
import sys
import os

"""Creates the directory structure of a datastore

    Parameters
    ----------
    root_directory : str
        The parent directory of the datastore
    datastore_name : str
        The name of the datastore. The directory created will be converted to upper case. 
    """


def create_datastore(datastore_path: str, datastore_name: str):

    os.makedirs(os.path.join(datastore_path, "data"))
    os.makedirs(os.path.join(datastore_path, "datastore"))
    os.makedirs(os.path.join(datastore_path, "metadata"))
    os.mkdir(datastore_path.replace(datastore_name, f'{datastore_name}_resultset'))
    print(f'Datastore {datastore_path} created')


def get_user_input(argv):
    command = 'create_filesystem.py -r <root_directory> -d <datastore_name>'
    try:
        opts, args = getopt.getopt(
            argv, "hr:d:", ["root_directory=", "datastore_name="]
        )
        if not opts:
            print(command)
            sys.exit()
    except getopt.GetoptError:
        print(command)
        sys.exit(2)
    for opt, value in opts:
        if opt == '-h':
            print('Creates basic filesystem for a datastore\n')
            print(command)
            sys.exit()
        elif opt in ("-r", "--root_directory"):
            root_directory = value
        elif opt in ("-d", "--datastore_name"):
            datastore_name = value.upper()
            datastore_path = f'{root_directory}/{datastore_name}'
    if not os.path.exists(root_directory):
        raise Exception(f'Root directory {root_directory} not found')
    if os.path.exists(datastore_path):
        raise Exception(f'Datastore {datastore_name} already exists')
    return datastore_path, datastore_name


def main(argv):
    datastore_path, datastore_name = get_user_input(argv)
    create_datastore(datastore_path, datastore_name)


if __name__ == "__main__":
    main(sys.argv[1:])