import os
import json
from utils import *
from pprint import pprint
import base64
import qrcode


def get_config(client_name):
    print(f'getting config from [{client_name}]')
    config_save_path = os.path.join(SCRIPT_DIR, f'{client_name}_config.json')
    get_config_cmd = f'gcloud compute scp {client_name}:/etc/v2ray/config.json {config_save_path} > /dev/null'
    get_config_retval = os.system(get_config_cmd)
    assert get_config_retval == 0

    with open(config_save_path) as f:
        config_data = json.load(f)
    return config_data


def build_v2rayu_config(instance, config):
    zone = instance['zone'].split('/')[-1]
    v2rayu_config = {
        "port": str(config['inbounds'][0]['port']),
        "ps": instance['name'] + '@' + zone,
        "tls": "none",
        "id": config['inbounds'][0]['settings']['clients'][0]['id'],
        "aid": str(config['inbounds'][0]['settings']['clients'][0]['alterId']),
        "v": "2",
        "host": "",
        "type": "none",
        "path": "",
        "net": "tcp",
        "add": instance['networkInterfaces'][0]['accessConfigs'][0]['natIP'],
        "sec": "auto"
    }
    return v2rayu_config


def build_v2rayu_uri(v2rayu_config):
    uri_content = json.dumps(v2rayu_config, separators=(',', ':'))
    uri_encoded = 'vmess://' + \
        base64.b64encode(uri_content.encode('ascii')).decode('ascii')
    return uri_encoded


if __name__ == "__main__":
    instances_data = list_instances()

    uris = []

    for instance in instances_data:
        name = instance['name']
        config_data = get_config(name)
        v2rayu_config = build_v2rayu_config(instance, config_data)
        uri = build_v2rayu_uri(v2rayu_config)
        uris.append(uri)

    print('\n'*3)
    for uri in uris:
        print(uri)

    for i, instance in enumerate(instances_data):
        uri = uris[i]
        name = instance['name']
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )
        qr.add_data(uri)
        print(f'showing qrcode of [{name}]')
        qr.print_ascii()
