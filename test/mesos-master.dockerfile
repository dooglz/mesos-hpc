
FROM ubuntu:xenial
LABEL maintainer="Dooglz"

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF && \
    echo "deb http://repos.mesosphere.io/ubuntu xenial main" | tee /etc/apt/sources.list.d/mesosphere.list && \
    apt update && \
    apt install -y curl iputils-ping mesos && \
    rm -rf /var/lib/apt/lists/*

RUN service zookeeper stop && \
    echo manual | tee /etc/init/mesos-slave.override && \
    echo mesos_master | tee /etc/mesos-master/hostname && \
    echo hpc_test_cluster | tee /etc/mesos-master/cluster  && \
    echo zk://mesos_master:2181/mesos | tee /etc/mesos/zk && \
    echo server.1=mesos_master:2888:3888 | tee -a /etc/zookeeper/conf/zoo.cfg && \
    echo dataLogDir=/var/log/zookeeper | tee -a /etc/zookeeper/conf/zoo.cfg && \
    echo 1 | tee /etc/zookeeper/conf/myid && \
    mkdir -p /usr/lib/jvm/java-9-openjdk-amd64/conf/management/ && \
    touch /usr/lib/jvm/java-9-openjdk-amd64/conf/management/management.properties && \
    echo  /usr/share/zookeeper/bin/zkServer.sh start | tee -a /go.sh && \
    echo  mesos-master start --zk=zk://mesos_master:2181/mesos --no-hostname_lookup true --registry=in_memory --log_dir=/var/log/mesos| tee -a /go.sh && \
    chmod +x /go.sh

EXPOSE 5050 2181 2888 3888
CMD ["/bin/bash", "/go.sh"]
#ENTRYPOINT [ "mesos-master", "--no-hostname_lookup", "true","--registry=in_memory"]