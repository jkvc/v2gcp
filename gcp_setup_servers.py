from pprint import pprint
from utils import *
from termcolor import cprint

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SETUP_SCRIPT_FILEPATH = os.path.realpath(
    os.path.join(
        SCRIPT_DIR, 'v2ray_server_setup_start.sh'
    )
)


def run_server_setup(ssh_config):
    display_name = ssh_config['display_name']
    username = ssh_config['username']
    external_ip = ssh_config['external_ip']
    public_key, private_key = get_ssh_key()

    cprint(f'>>> begin setup [{display_name}]', 'yellow')
    run_setup_script_cmd = f'ssh -i {private_key} -o StrictHostKeyChecking=no {username}@{external_ip} < {SETUP_SCRIPT_FILEPATH}'
    run_setup_script_retval = os.system(run_setup_script_cmd)
    assert run_setup_script_retval == 0
    cprint(f'>>>  done setup [{display_name}]', 'green')


if __name__ == "__main__":
    ssh_configs = get_ssh_configs()
    for ssh_config in ssh_configs:
        try:
            run_server_setup(ssh_config)
        except AssertionError:
            cprint(
                f'Failed to setup [{ssh_config["display_name"]}]', 'red')
