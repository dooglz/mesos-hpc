#!/bin/bash
docker kill mesos_master
docker kill mesos_slave
sleep 1
docker rm mesos_master
docker rm mesos_slave
set -e
docker network rm mesos_net || docker network create mesos_net
sleep 1
docker build --tag mesos:master -f mesos-master.dockerfile .
docker build --tag mesos:slave -f mesos-slave.dockerfile .
docker run --network mesos_net --hostname=mesos_master -p 5050:5050 -td --name mesos_master mesos:master
docker run --network mesos_net --hostname=mesos_slave -p 5051:5051 --privileged -td --name mesos_slave mesos:slave
