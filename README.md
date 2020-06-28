# v2gcp

## dependency

need a unix-like environment, the scripts invokes commands such as `ssh`, `scp`, `ssh-keygen`.

need python 3.7 and above, and some dependencies:

```
pip install qrcode termcolor
```

## GCP

### prerequisites

first you need a gcp account with an active project. note down the project id.

follow https://cloud.google.com/sdk/install to install the commandline `gcloud`, then login:

```bash
gcloud auth login
# follow the browser prompt
gcloud config set project [PROJECT_ID]
```

run `python gcp_setup_prereq.py` to install prerequisites, this generates an ssh keypair if there isnt one in the repo already, setup os login with that keypair, setup a firewall rule, and create an instance template.

### start a server instance

(auto start instance under construction)

once there is one or more instances running, run `python gcp_setup_servers.py`. this will scan the project for all running instance, install v2ray on them and start the server. re-run the script as you make new instances. 

### read the server configs

#### v2rayU / v2rayNG

once there is one or more instances running with v2ray server set up, run `python gcp_get_v2rayu_configs.py` get configs from each running server. the script will print a qr code for each server, and vmess:// URIs for all servers.

copy all vmess URIs and use use "import from clipboard" to add all servers. scan qr codes individually if more covnenient.
