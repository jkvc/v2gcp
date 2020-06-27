import os
import json
import shutil

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def run_gcloud_cmd_format_json(cmd, save_filename):
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
    firewall_data = run_gcloud_cmd_format_json(cmd, 'firewall_rules.json')
    return firewall_data


def list_isntance_templates():
    cmd = 'gcloud compute instance-templates list'
    data = run_gcloud_cmd_format_json(cmd, 'instance_templates.json')
    return data


def list_instances():
    cmd = 'gcloud compute instances list'
    data = run_gcloud_cmd_format_json(cmd, 'instances.json')
    return data


def get_display_name(instance):
    name = instance['name']
    zone = instance['zone'].split('/')[-1]
    return name + '@' + zone
