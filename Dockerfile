FROM centos:centos7
ENV container docker
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
export LANG=C;\
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7;\
yum clean all;\
yum update -y;\
yum install -y "http://mirror.centos.org/centos/7/updates/x86_64/Packages/git-1.8.3.1-12.el7_4.x86_64.rpm";\
yum install -y "https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.4.3.0-1.el7.ans.noarch.rpm";
VOLUME ["/sys/fs/cgroup","/bin"]
