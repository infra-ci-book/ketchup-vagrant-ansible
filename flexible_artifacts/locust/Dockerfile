FROM centos:7
ENV container docker

ENV ANSIBLE_VERSION 2.4.2.0
ENV LINT_VERSION 3.4.21
ENV LOCUST_VERSION 0.8
ENV PYZMQ_VERSION 17.0.0
ENV GEVENT_VERSION 1.3.1

COPY locustfile.py locustfile.py

RUN export LANG=C; \
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7; \
    yum install -y epel-release && \
    yum install -y git && \
    yum install -y "ansible-${ANSIBLE_VERSION:?}" && \
    yum install -y "ansible-lint-${LINT_VERSION:?}" && \
    yum install -y python2-pip gcc-c++ && \
    yum clean all

RUN pip install --disable-pip-version-check locust=="${LOCUST_VERSION}" pyzmq=="${PYZMQ_VERSION}" gevent=="${GEVENT_VERSION}"
