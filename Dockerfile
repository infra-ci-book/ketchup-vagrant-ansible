FROM centos:7

ENV container docker
ENV ANSIBLE_VERSION 2.4.2.0
ENV ANSIBLE_LINT_VERSION 3.4.21

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
    yum install -y ansible-${ANSIBLE_VERSION:?} && \
    yum install -y ansible-lint-${ANSIBLE_LINT_VERSION:?} && \
    yum clean all

VOLUME ["/sys/fs/cgroup","/bin"]
