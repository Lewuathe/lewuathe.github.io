---
layout: post
blog: true
title: "Multiple Hadoop Cluster on Docker"
date: 2015-09-16 21:02:58 +0900
comments: true
categories: ["Hadoop", "Docker"]
author: Kai Sasaki
---

As a hadoop developer, there are several times when I want to create multiple node hadoop cluster more easily.
First I came up with using VirtualBox and Vagrant. But it was very slow to launch one cluster. Besides the more nodes we added,
the slower launching time be. I cannot wait to check each change and debug it. Every developers may think so.

<!-- more -->

[Docker](https://www.docker.com/) is an open platform for building, shipping and running distributed applications.
This software sufficiently fits this use case. Docker is a container service not a virtual machine. So it is light and faster launching.
I searched hadoop cluster image for docker. But I cannot find good one which seems to be maintained active. Some images cannot be used now
at latest Docker or MacOSX.

This is the reason why I crated [docker-hadoop-cluster](https://github.com/Lewuathe/docker-hadoop-cluster). This is the modified version of [sequenceiq/hadoop-docker](https://github.com/sequenceiq/hadoop-docker). With `docker-hadoop-cluster`, you can build multiple node hadoop cluster
on your laptop about one minute. This is not for production only for development and tutorial. So `docker-hadoop-cluster` can deploy arbitrary hadoop package build by yourself. Here is the instruction how to use this image.

# Build images

`hadoop-base` is a base image of hadoop service. This image includes JDK, hadoop package configurations etc. This image also can include your self-build hadoop package. In order to bind your hadoop package, `hadoop-X.Y.Z.tar.gz` package assumed be put under `hadoop-base` directory.
Then it's the time to build image.

```
$ cp hadoop-3.0.0-SNAPSHOT.tar.gz hadoop-base
$ cd hadoop-base
$ docker build -t lewuathe/hadoop-base .
```

Next one is the image for master server. This image includes master service such as namenode and resource manager.

```
$ cd hadoop-master
$ docker build -t lewuathe/hadoop-master .
```

The last one is for slave services. This image includes slave service such as datanode and node manager.

```
$ cd hadoop-slave
$ docker build -t lewuathe/hadoop-slave .
```

# Run cluster

`docker-hadoop-cluster` includes launching script.

```
## Create hadoop cluster with 5 slave nodes.
$ bin/build_cluster.sh --slaves 5 launch

## Destroy your previsout hadoop cluster.
$ bin/build_cluster.sh --slaves 5 destroy
```

# Welcome patches

The biggest thing I want to do was to create **maintained image for hadoop cluster**. Although it might be difficult to do this alone,
anyone can contribute and help this images. This is why I published this image. If you have any questions or are interested in this projects, please let me know. Thank you!
