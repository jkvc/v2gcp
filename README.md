# v2gcp

```
pip install qrcode
```

## setup gcloud

first, follow https://cloud.google.com/sdk/install to install the commandline util `gcloud`

login with `gcloud`
```bash
gcloud auth login
# then follow the browser prompt

gcloud config set project [PROJECT_ID]
```

generate ssh keys if it's not there already 

```bash
ssh-keygen -b 4096
# use the default output directory, which is ~/.ssh/
```

setup os-login

```bash
gcloud compute project-info add-metadata --metadata enable-oslogin=TRUE
gcloud compute os-login ssh-keys add --key-file ~/.ssh/id_rsa.pub
```


