#!/bin/sh

set -e

IMAGE="centos:centos7"
KETCHUP_NAME=$(uuidgen)
KETCHUP_NGINX_NAME=$(uuidgen)
TEST_DIR="/tmp/ansible_test_runner"
ANSIBLE_PACKAGE_URL="https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64"
ANSIBLE_PACKAGE_NAME="ansible-2.4.3.0-1.el7.ans.noarch.rpm"

docker run --detach --privileged --volume="$PWD":$TEST_DIR:rw --name $KETCHUP_NAME $opts $IMAGE /sbin/init
docker run --detach --privileged --volume="$PWD":$TEST_DIR:rw --name $KETCHUP_NGINX_NAME $opts $IMAGE /sbin/init

# Prepare to launch test playbook
docker exec $KETCHUP_NAME yum install -y $ANSIBLE_PACKAGE_URL/$ANSIBLE_PACKAGE_NAME
docker exec $KETCHUP_NGINX_NAME yum install -y $ANSIBLE_PACKAGE_URL/$ANSIBLE_PACKAGE_NAME

# Launch test playbook for ketchup
docker exec $KETCHUP_NAME       /bin/bash -c "cd $TEST_DIR/tests && ansible-playbook -i travis_test_inventory -t ketchup       travis_test_ketchup.yml"

# Launch test playbook for ketchup_nginx
docker exec $KETCHUP_NGINX_NAME /bin/bash -c "cd $TEST_DIR/tests && ansible-playbook -i travis_test_inventory -t ketchup_nginx travis_test_ketchup.yml"

#
# [EOF]
#
