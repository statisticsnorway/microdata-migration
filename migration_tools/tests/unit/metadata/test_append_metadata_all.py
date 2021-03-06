import json
import shutil
from migration_tools.migration.metadata import append_metadata_all


def setup_function():
    shutil.copytree(
        'tests/resources/append_metadata',
        'tests/resources/append_metadata_backup'
    )


def teardown_function():
    shutil.rmtree('tests/resources/append_metadata')
    shutil.move(
        'tests/resources/append_metadata_backup',
        'tests/resources/append_metadata'
    )


def test_append_metadata_all():
    metadata_file = "tests/resources/append_metadata/ARBLONN_ARB_HELDELTID.json"
    metadata_all_file = "tests/resources/append_metadata/metadata-all.json"
    append_metadata_all.append_metadata_all(metadata_file, metadata_all_file)
    metadata_all_enriched_file = metadata_all_file.replace(".json", "_enriched.json")

    with open(metadata_all_enriched_file) as f:
        dataset = json.load(f)
    dataset_names = [
        data_structure["name"] for data_structure in dataset["dataStructures"]
    ]
    assert "ARBLONN_ARB_HELDELTID" in dataset_names
