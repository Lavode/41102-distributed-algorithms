#!/bin/bash

function as_vagrant {
    cmd=$@
    echo "Executing as vagrant: $cmd"
    su -c "$@" vagrant
}

export DEBIAN_FRONTEND=noninteractive

apt-get -y update && apt-get -y dist-upgrade && apt-get -y autoremove

apt-get -y install golang vim curl

as_vagrant 'go get github.com/etcd-io/etcd'
as_vagrant 'cd go/src/go.etcd.io/etcd/etcdctl && go build'
as_vagrant 'go get github.com/mattn/goreman'

as_vagrant 'mkdir etcdproj && cd etcdproj && ln -s ~/go/bin/etcd && ln -s ~/go/src/go.etcd.io/etcd/etcdctl/etcdctl && ln -s ~/go/bin/goreman && ln -s /mnt/project_1/proj01/Procfile'
