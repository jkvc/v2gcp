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
    instance_name = instance['name']
    cprint(f'>>> begin setup [{get_display_name(instance)}]', 'yellow')

    zone = instance['zone'].split('/')[-1]
    run_setup_script_cmd = f'gcloud compute ssh --zone {zone} {instance_name} < {SETUP_SCRIPT_FILEPATH}'
    run_setup_script_retval = os.system(run_setup_script_cmd)
    assert run_setup_script_retval == 0
    cprint(f'>>>  done setup [{get_display_name(instance)}]', 'green')
    print()


if __name__ == "__main__":
    instances = list_instances()
    for instance in instances:
        run_client_setup(instance)
