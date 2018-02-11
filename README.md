# ketchup-vagrant-ansible

ketchup-vagrant-ansible is a playbook what is able to deply ketchup CMS and Nginx frontend.

## How to launch this playbook

You can follow the following steps to deploy ketchup and Nginx at the same time:

```
$ ansible-playbook -i hosts/ketchup/inventory ketchup.yml
```

## How to configuration this playbook

You can modify the following parameters in the inventory(`hosts/ketchup/inventory`) file:

```
[ketchup]
192.168.33.12        # IPAddress or hostname of your ketchup server

[ketchup_nginx]
192.168.33.13        # IPAddress or hostname of your Nginx frontend


[all:vars]
ketchup_host=192.168.33.12        # IPAddress or hostname of your ketchup CMS
ketchup_port=80                   # Port number of your ketchup CMS

[ketchup:vars]
ansible_ssh_user=vagrant
ansible_ssh_private_key_file="~/vagrant/infraci/.vagrant/machines/ketchup/virtualbox/private_key"

use_epel_repo=True                # If you want to use official Nginx package, set it to False
use_nginx_proxy=False             # If you want to use Nginx proxy with ketchup CMS in the same host, set it to True
#ketchup_host=192.168.33.12       # IPAddress or hostname of your ketchup CMS
#ketchup_port=8080                # Port number of your ketchup CMS
#nginx_http_port=80               # Port number of your Ngninx proxy

ketchup_repos="https://github.com/infra-ci-book/app-contents.git"
ketchup_app_path="app-contents/applications/ketchup_Linux_x86_64.tar.gz"
ketchup_data_dir="app-contents/contents/data"

[ketchup_nginx:vars]
ansible_ssh_user=vagrant
ansible_ssh_private_key_file="~/vagrant/infraci/.vagrant/machines/ketchup-nginx/virtualbox/private_key"

use_epel_repo=True
use_nginx_proxy=True

nginx_http_port=80
```
