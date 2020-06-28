import os
from utils import *

FIREWALL_RULE_NAME = 'v2gcp-allow-all'
INSTANCE_TEMPLATE_NAME = 'v2gcp-template'

if __name__ == "__main__":
    # make a firewall rule network tag that allow all port ingress
    firewall_rule_data = list_firewall_rules()
    firewall_rule_exists = False
    for rule in firewall_rule_data:
        if rule['name'] == FIREWALL_RULE_NAME:
            firewall_rule_exists = True

    if not firewall_rule_exists:
        firewall_rule_cmd = (
            f'gcloud compute firewall-rules create '
            f'{FIREWALL_RULE_NAME} --description="allow all port ingress" '
            f'--direction=INGRESS --priority=1000 --network=default '
            f'--action=ALLOW --rules=all --source-ranges=0.0.0.0/0 '
            f'--target-tags={FIREWALL_RULE_NAME}'
        )
        firewall_rule_ret = os.system(firewall_rule_cmd)
        assert firewall_rule_ret == 0

    # make an instance template
    instance_template_data = list_isntance_templates()
    instance_template_exists = False
    for template in instance_template_data:
        if template['name'] == INSTANCE_TEMPLATE_NAME:
            instance_template_exists = True

    if not instance_template_exists:
        instance_template_cmd = (
            f'gcloud compute instance-templates create '
            f'{INSTANCE_TEMPLATE_NAME} --machine-type=f1-micro '
            f'--network-tier=PREMIUM --maintenance-policy=MIGRATE '
            f'--scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append '
            f'--tags={FIREWALL_RULE_NAME} --image=ubuntu-1604-xenial-v20200611 '
            f'--image-project=ubuntu-os-cloud --boot-disk-size=10GB '
            f'--boot-disk-type=pd-standard --boot-disk-device-name={INSTANCE_TEMPLATE_NAME} '
            f'--no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring '
            f'--reservation-affinity=any'
        )
        instance_template_ret = os.system(instance_template_cmd)
        assert instance_template_ret == 0
