FROM centos:7

ENV container docker
ENV ANSIBLE_VERSION 2.4.2.0
ENV ANSIBLE_RPM https://github.com/infra-ci-book/support/raw/master/obsoleted/ansible-2.4.2.0-2.el7.noarch.rpm
ENV ANSIBLE_LINT_VERSION 3.4.21
ENV ANSIBLE_LINT_RPM https://github.com/infra-ci-book/support/raw/master/obsoleted/ansible-lint-3.4.21-1.el7.centos.noarch.rpm

COPY ./ ./

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
     systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*;\
    rm -f /etc/systemd/system/*.wants/*;\
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*;\
    rm -f /lib/systemd/system/anaconda.target.wants/*;\
    yum install -y epel-release && \
    yum install -y git && \
    yum install -y ${ANSIBLE_RPM:?} && \
    yum install -y ${ANSIBLE_LINT_RPM:?} && \
    yum clean all

VOLUME ["/sys/fs/cgroup","/bin"]
