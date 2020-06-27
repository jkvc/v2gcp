import os
import json
import shutil

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def list_json(cmd, save_filename):
    save_filapath = os.path.join(
        SCRIPT_DIR, save_filename
    )
    if os.path.exists(save_filapath):
        os.remove(save_filapath)
    retval = os.system(f'{cmd} --format=json > {save_filapath}')
    assert retval == 0, f'[{cmd}] failed'

    with open(save_filapath) as f:
        data = json.load(f)
    return data


def list_firewall_rules():
    cmd = 'gcloud compute firewall-rules list'
    firewall_data = list_json(cmd, 'firewall_rules.json')
    return firewall_data


def list_isntance_templates():
    cmd = 'gcloud compute instance-templates list'
    data = list_json(cmd, 'instance_templates.json')
    return data


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


def get_display_name(instance):
    name = instance['name']
    zone = instance['zone'].split('/')[-1]
    return name + '@' + zone
