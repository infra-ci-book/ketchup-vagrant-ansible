FROM centos:7

ENV ANSIBLE_VERSION 2.4.2.0
ENV TARGET_APP ketchup_nginx
ENV GITLAB_IP 192.168.33.10
ENV GITLAB_REPO ketchup-vagrant-ansible

RUN rm -f "/lib/systemd/system/multi-user.target.wants/*"; \
    rm -f "/etc/systemd/system/*.wants/*"; \
    rm -f "/lib/systemd/system/local-fs.target.wants/*"; \
    rm -f "/lib/systemd/system/sockets.target.wants/*udev*"; \
    rm -f "/lib/systemd/system/sockets.target.wants/*initctl*"; \
    rm -f "/lib/systemd/system/basic.target.wants/*"; \
    rm -f "/lib/systemd/system/anaconda.target.wants/*"; \
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7; \
    yum install -y epel-release; \
    yum install -y git; \
    yum install -y ansible-"${ANSIBLE_VERSION:?}"; \
    git clone "http://${GITLAB_IP}/root/${GITLAB_REPO}.git";

WORKDIR /${GITLAB_REPO}
RUN ansible-playbook -e 'artifact=containered' -i ./flexible_artifacts/hosts/ketchup/inventory -l "${TARGET_APP}" ./"${TARGET_APP}".yml

WORKDIR /
RUN rm -fr /"${GITLAB_REPO:?}"

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80/tcp
STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]
