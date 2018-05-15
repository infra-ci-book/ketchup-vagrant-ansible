FROM centos:7
ENV container docker

ENV PIP_VERSION 10.0.1
ENV ANSIBLE_VERSION 2.4.2.0
ENV LINT_VERSION 3.4.21
ENV LOCUST_VERSION 0.8
ENV PYZMQ_VERSION 17.0.0

COPY locustfile.py locustfile.py

RUN export LANG=C; \
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7; \
    yum install -y epel-release && \
    yum install -y git && \
    yum install -y "ansible-${ANSIBLE_VERSION:?}" && \
    yum install -y "ansible-lint-${LINT_VERSION:?}" && \
    yum install -y python-pip gcc-c++ && \
    yum clean all

RUN pip install --upgrade pip=="${PIP_VERSION:?}" && \
    pip install locust=="${LOCUST_VERSION:?}" pyzmq=="${PYZMQ_VERSION:?}"
