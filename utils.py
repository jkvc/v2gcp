import os
import json
import shutil

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def list_instances():
    instances_data_filepath = os.path.realpath(
        os.path.join(
            SCRIPT_DIR, 'instances_data.json'
        )
    )
    if os.path.exists(instances_data_filepath):
        os.remove(instances_data_filepath)

    cmd = f'gcloud compute instances list --format=json > {instances_data_filepath}'
    retval = os.system(cmd)
    assert retval == 0, f'[{cmd}] failed'

    with open(instances_data_filepath) as f:
        instances_data = json.load(f)
    return instances_data
