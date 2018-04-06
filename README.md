# ketchup-vagrant-ansible

ketchup-vagrant-ansible is a playbook what is able to deply ketchup CMS and Nginx frontend.

## Requirements

- Ansible >= 2.4.0.0
- CentOS >= 7.4

---

CentOS:

```
yum -y update
yum -y install ansible
reboot
```


## How to launch a playbook each operation:

### 1. You can follow the following steps to deploy ketchup and Nginx at the same time:

```
$ ansible-playbook -i hosts/ketchup/inventory site.yml
```

### 2. You can create and boot a server instance:

```
$ ansible-playbook -i hosts/ketchup/inventory -e 'instance_name=FOO' -e 'instance_action=start' instance.yml
```

### 3. You can shutdown a server instance:

```
$ ansible-playbook -i hosts/ketchup/inventory -e 'instance_name=FOO' -e 'instance_action=stop' instance.yml
```

### 4. You can terminate a server instance:

```
$ ansible-playbook -i hosts/ketchup/inventory -e 'instance_name=FOO' -e 'instance_action=terminate' instance.yml
```


## How to configuration this playbook

### Inventory Variables

You can modify the following parameters in the inventory(`hosts/ketchup/inventory`) file:

```
[vagrant]
127.0.0.1

[ketchup]
192.168.33.12        # IPAddress or hostname of your ketchup server

[ketchup_nginx]
192.168.33.13        # IPAddress or hostname of your Nginx frontend


[all:vars]
ketchup_host=192.168.33.12        # IPAddress or hostname of your ketchup CMS
ketchup_port=80                   # Port number of your ketchup CMS

[vagrant:vars]
ansible_connection=local
instance_provider=vagrant         # You can specify a provider name like 'vagrant'
instance_name=''                  # A name of your target server instance on your IaaS
instance_action=''                # Choose an action from start, stop, and terminate.

[ketchup:vars]
ansible_ssh_user=vagrant
ansible_ssh_private_key_file="~/vagrant/infraci/.vagrant/machines/ketchup/virtualbox/private_key"

#ketchup_host=192.168.33.12       # IPAddress or hostname of your ketchup CMS
#ketchup_port=8080                # Port number of your ketchup CMS
#nginx_http_port=80               # Port number of your Ngninx proxy

ketchup_repos="https://github.com/infra-ci-book/app-contents.git"
ketchup_app_path="app-contents/applications/ketchup_Linux_x86_64.tar.gz"
ketchup_data_dir="app-contents/contents/data"

[ketchup_nginx:vars]
ansible_ssh_user=vagrant
ansible_ssh_private_key_file="~/vagrant/infraci/.vagrant/machines/ketchup-nginx/virtualbox/private_key"

nginx_http_port=80
```

## Dependencies

None.

## Installation

This assumes that you've installed the base dependencies and you're running on CentOS.

```
git clone https://github.com/infra-ci-book/ketchup-vagrant-ansible
```

## License

Apache-2.0
