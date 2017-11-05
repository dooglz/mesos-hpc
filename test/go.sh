#!/bin/bash
set -e
docker network rm mesos_net || docker network create mesos_net
docker build --tag mesos:master -f mesos-master.dockerfile .
docker build --tag mesos:slave -f mesos-slave.dockerfile .
docker run --network mesos_net --hostname=mesos_master -p 5050:5050 -td --name mesos_master mesos:master
docker run --network mesos_net --hostname=mesos_slave --privileged -td --name mesos_slave mesos:slave
