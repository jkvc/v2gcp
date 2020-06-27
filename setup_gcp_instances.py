from pprint import pprint
from utils import *
from termcolor import cprint

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SETUP_SCRIPT_FILEPATH = os.path.realpath(
    os.path.join(
        SCRIPT_DIR, 'client_setup.sh'
    )
)


def run_client_setup(instance):
    client_name = instance['name']
    cprint(f'>>> setting up [{client_name}]', 'yellow')

    zone = instance['zone'].split('/')[-1]
    run_setup_script_cmd = f'gcloud compute ssh --zone {zone} {client_name} < {SETUP_SCRIPT_FILEPATH}'
    run_setup_script_retval = os.system(run_setup_script_cmd)
    assert run_setup_script_retval == 0


if __name__ == "__main__":
    instances_data = list_instances()

    for instance in instances_data:
        run_client_setup(instance)
