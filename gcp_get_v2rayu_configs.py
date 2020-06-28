import os
import json
from utils import *
from pprint import pprint
import base64
import qrcode
from termcolor import cprint


def get_v2ray_server_config(config):
    display_name = config['display_name']
    cprint(f'getting config from [{display_name}]', 'yellow')

    username = config['username']
    external_ip = config['external_ip']
    public_key, private_key = get_ssh_key()

    config_save_path = os.path.join(SCRIPT_DIR, f'.{display_name}_config.json')
    get_config_cmd = f'scp -i {private_key} -o StrictHostKeyChecking=no {username}@{external_ip}:/etc/v2ray/config.json {config_save_path} > /dev/null 2>&1'
    get_config_retval = os.system(get_config_cmd)
    assert get_config_retval == 0

    with open(config_save_path) as f:
        config_data = json.load(f)
    return config_data


def get_v2rayu_uri(display_name, external_ip, server_config):
    v2rayu_config = {
        "port": str(server_config['inbounds'][0]['port']),
        "ps": display_name,
        "tls": "none",
        "id": server_config['inbounds'][0]['settings']['clients'][0]['id'],
        "aid": str(server_config['inbounds'][0]['settings']['clients'][0]['alterId']),
        "v": "2",
        "host": "",
        "type": "none",
        "path": "",
        "net": "tcp",
        "add": external_ip,
        "sec": "auto"
    }
    uri_content = json.dumps(v2rayu_config, separators=(',', ':'))
    uri_encoded = 'vmess://' + \
        base64.b64encode(uri_content.encode('ascii')).decode('ascii')
    return uri_encoded


if __name__ == "__main__":
    ssh_configs = get_ssh_configs()

    uris = []
    for ssh_config in ssh_configs:
        try:
            server_config = get_v2ray_server_config(ssh_config)
            uri = get_v2rayu_uri(
                ssh_config['display_name'],
                ssh_config['external_ip'],
                server_config
            )
            uris.append(uri)

            # build and print qrcode
            cprint(f'showing qrcode of [{ssh_config["display_name"]}]', 'cyan')
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
            )
            qr.add_data(uri)
            qr.print_ascii()

        except AssertionError:
            cprint(
                f'Failed to get config from [{ssh_config["display_name"]}]', 'red')

    cprint('All URIs in one blob:', 'cyan')
    for uri in uris:
        print(uri)
