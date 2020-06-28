import os
import json
import shutil
from termcolor import cprint

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def run_cmd_save_output(cmd, save_filename):
    save_filapath = os.path.join(
        SCRIPT_DIR, save_filename
    )
    if os.path.exists(save_filapath):
        os.remove(save_filapath)
    retval = os.system(f'{cmd} > {save_filapath}')
    assert retval == 0, f'[{cmd}] failed'

    with open(save_filapath) as f:
        data = json.load(f)
    return data


def run_gcloud_cmd_format_json(cmd, save_filename):
    cmd = f'{cmd} --format=json'
    return run_cmd_save_output(cmd, save_filename)


def list_firewall_rules():
    cmd = 'gcloud compute firewall-rules list'
    firewall_data = run_gcloud_cmd_format_json(cmd, '.firewall_rules.json')
    return firewall_data


def list_isntance_templates():
    cmd = 'gcloud compute instance-templates list'
    data = run_gcloud_cmd_format_json(cmd, '.instance_templates.json')
    return data


def list_instances():
    cmd = 'gcloud compute instances list'
    data = run_gcloud_cmd_format_json(cmd, '.instances.json')
    return data


def instance_is_running(instance):
    return instance['status'] == 'RUNNING'


def get_display_name(instance):
    name = instance['name']
    zone = instance['zone'].split('/')[-1]
    return name + '@' + zone


def get_ssh_username():
    configs = run_gcloud_cmd_format_json(
        'gcloud config list', '.config.json'
    )
    username = configs['core']['account']
    username = username.replace('@', '_')
    username = username.replace('.', '_')
    return username


def get_external_ip(instance):
    return instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']


def get_ssh_configs():
    instances_data = list_instances()
    ssh_configs = []
    for instance in instances_data:
        if not instance_is_running(instance):
            cprint(f'{get_display_name(instance)} is not running, skip', 'red')
            continue
        config = {
            'external_ip': get_external_ip(instance),
            'username': get_ssh_username(),
            'sshkey': None,
            'display_name': get_display_name(instance)
        }
        ssh_configs.append(config)
    return ssh_configs
