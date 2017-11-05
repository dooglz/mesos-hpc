
FROM ubuntu:xenial
LABEL maintainer="Dooglz"

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF && \
    echo "deb http://repos.mesosphere.io/ubuntu xenial main" | tee /etc/apt/sources.list.d/mesosphere.list && \
    apt update && \
    apt install -y curl iputils-ping mesos && \
    rm -rf /var/lib/apt/lists/*

RUN service zookeeper stop && \
    echo manual | tee /etc/init/mesos-master.override  && \
    echo manual | tee /etc/init/zookeeper.override && \
    apt -y remove --purge zookeeper

CMD ["--work_dir=/var/lib/mesos/slave", "--master=zk://mesos_master:2181/mesos", "--no-systemd_enable_support"]
ENTRYPOINT ["mesos-slave"]