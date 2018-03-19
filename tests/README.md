# ketchup-vagrant-ansible test

ketchup-vagrant-ansible is a playbook what is able to deply ketchup CMS and Nginx frontend.

## Requirements

- Ansible >= 2.4.0.0
- CentOS >= 7.4

---

Test Docker Images(CentOS):

```
yum clean all
yum update -y
yum install -y "https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.4.3.0-1.el7.ans.noarch.rpm";
```

## How to test a playbook by console:

### You can take the following steps to test ketchup and Nginx by command line:

```
$ cd ./tests
$ ansible-playbook -i ../hosts/ketchup/inventory ketchup_test.yml --syntax-check
$ ansible-playbook -i ../hosts/ketchup/inventory ketchup_test.yml
$ ansible-playbook -i ../hosts/ketchup/inventory ketchup_nginx_test.yml --syntax-check
$ ansible-playbook -i ../hosts/ketchup/inventory ketchup_nginx_test.yml
```

## How to test a playbook by GitLab CI:

### 1. You can clone repository from GitHub to GitLab:
1. Access to `http://192.168.33.10` or `http://[your host ip address]` and login as your account
2. Create New Project and import project from `https://github.com/infra-ci-book/ketchup-vagrant-ansible`    

    ![](https://github.com/infra-ci-book/ketchup-vagrant-ansible/raw/master/tests/images/01.JPG)

3. Check project import successfully

    ![](https://github.com/infra-ci-book/ketchup-vagrant-ansible/raw/master/tests/images/02.JPG)

### 2. Setup config for insecure docker registry:
1. Access to GitLab Runner host
2. Change docker systemd config

```
$ vi /etc/systemd/system/docker.service
-- ExecStart=/usr/bin/dockerd
++ ExecStart=/usr/bin/dockerd --insecure-registry registry.gitlab.example.com:4567
$ systemctl daemon-reload
$ systemctl restart docker
```

### 3. Setup hosts for docker registry:
1. Access to GitLab host and Runner host
2. Change hosts file
```
$ vi /etc/hosts (add the line)
192.168.33.10  registry.gitlab.example.com
```

### 4. Add SSH Private Key
1. Login to GitLab as your account again and go to "ketchup-vagrant-ansible" project
2. Select [Secret Values] from [Settings]>[CI/CD]
3. Set your private key(.ssh/infraci) named as "VAGRANT_PRIVATE_KEY"

    ![](https://github.com/infra-ci-book/ketchup-vagrant-ansible/raw/master/tests/images/03.JPG)

4. Register variables from [Add new variable]

### 5. CI/CD Pipeline
1. Login to GitLab as your account again.   
2. Select "ketchup-vagrant-ansible" project and [CI/CD]>[Pipelines]  
3. Push [Run pipeline] to run jobs

## Dependencies

None.

## License

Apache-2.0
