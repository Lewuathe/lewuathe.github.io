---
title: "Presto Docker Container with Graviton 2 Processor"
layout: post
date: 2020-08-07 13:39:59 +0900
image: 'assets/img/posts/2020-08-07-run-presto-on-graviton2-processor/catch.jpg'
description:
tag: ['Java', 'Presto', 'ARM', 'AWS']
blog: true
author: "Kai Sasaki"
---

I recently tried to run [Presto](https://prestosql.io/) on Arm architecture system to evaluate how it can cost-effectively achieve faster performance as part of my work. Thanks to AWS, we can make use of server machines having Arm processors such as Graviton 1/2. We have succeeded in experimenting without having much difficulty. The result of the research was described in the following articles.

- [Presto Experiment with Graviton Processor](https://prestosql.io/blog/2019/12/23/Presto-Experiment-with-Graivton-Processor.html)
- [High Performance SQL: AWS Graviton2 Benchmarks with Presto and Arm Treasure Data CDP](https://blog.treasuredata.com/blog/2020/03/27/high-performance-sql-aws-graviton2-benchmarks-with-presto-and-arm-treasure-data-cdp/)

But I have found that they do not uncover the full detail of how to set up the Docker environment and steps to build an Arm-supporting docker image. Graviton 2 is now publicly available. We can even personally try the processor for running the distributed system like Presto. Therefore, I'm going to restate the aspect of the process step by step here.

The topics this article will cover are:
- How to install docker engine in the Arm machine
- How to build Arm-supporting docker image for Presto
- How to run the Arm-supporting container in Graviton 2 instance

## Setup Graviton 2

I used the Ubuntu 18.04 (LTS) built for the Arm64 platform. The AMI id is `ami-0d221091ef7082bcf`. As it does not contain a docker engine inside, we need to install it manually. The instance type I used is [m6g.medium](https://aws.amazon.com/ec2/instance-types/m6/).
Once the instance is ready, follow the below steps.

### Setup the Repository

Install necessary packages first.

```
$ sudo apt-get update

$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

Add docker's official GPG key.

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Verify the key.

```
$ sudo apt-key fingerprint 0EBFCD88

pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]
```

Finally, add the repository for installing the docker engine for the Arm platform.

```
$ sudo add-apt-repository \
   "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

### Install Docker Engine

```
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

See the list of available versions.

```
$ apt-cache madison docker-ce
docker-ce | 5:19.03.12~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.11~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.10~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.9~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.8~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.7~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.6~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.5~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
docker-ce | 5:19.03.4~3-0~ubuntu-bionic | https://download.docker.com/linux/ubuntu bionic/stable arm64 Packages
...
```

I choose the latest one, `5:19.03.12~3-0~ubuntu-bionic`.

Install the package.

```
$ sudo apt-get install \
    docker-ce=5:19.03.12~3-0~ubuntu-bionic \
    docker-ce-cli=5:19.03.12~3-0~ubuntu-bionic \
    containerd.io
```

To run the docker command without root permission, add the user into the `docker` group.

```
$ sudo usermod -aG docker ubuntu
```

Login into the instance again to reflect the latest user setting.

## Build the Docker Image

Let's build an Arm-supporting image from the source. Put the following Dockerfile under any directory as you like. I put it under `/path/to/presto-arm64v8`.

```Dockerfile
FROM arm64v8/openjdk:11

RUN \
    set -xeu && \
    apt-get -y -q update && \
    apt-get -y -q install less && \
    apt-get -q clean all && \
    rm -rf /var/cache/yum && \
    rm -rf /tmp/* /var/tmp/* && \
    groupadd presto --gid 1000 && \
    useradd presto --uid 1000 --gid 1000 && \
    mkdir -p /usr/lib/presto /data/presto && \
    chown -R "presto:presto" /usr/lib/presto /data/presto

ARG PRESTO_VERSION
COPY --chown=presto:presto presto-server-${PRESTO_VERSION} /usr/lib/presto

EXPOSE 8080
USER presto:presto
ENV LANG en_US.UTF-8
CMD ["/usr/lib/presto/bin/run-presto"]
```

We also need a script to launch the process as follows. The following file is put under `/path/to/presto-arm64v8/bin/run-presto`.

```sh
#!/bin/bash

set -xeuo pipefail

if [[ ! -d /usr/lib/presto/etc ]]; then
    if [[ -d /etc/presto ]]; then
        ln -s /etc/presto /usr/lib/presto/etc
    else
        ln -s /usr/lib/presto/default/etc /usr/lib/presto/etc
    fi
fi

set +e
grep -s -q 'node.id' /usr/lib/presto/etc/node.properties
NODE_ID_EXISTS=$?
set -e

NODE_ID=""
if [[ ${NODE_ID_EXISTS} != 0 ]] ; then
    NODE_ID="-Dnode.id=${HOSTNAME}"
fi

exec /usr/lib/presto/bin/launcher run ${NODE_ID} "$@"

```

Afterward, we can build the latest presto.

```sh
$ cd /path/to/presto
$ ./mvnw -T 1C install -DskipTests
```

Make sure to find the artifact under `/path/to/presto/presto-server/target`. Finally, the following commands will provide the docker image supporting Arm architecture.

```sh
$ export PRESTO_VERSION=340-SNAPSHOT
$ export WORK_DIR=/path/to/presto-arm64v8

# Copy presto server module
$ cp /path/to/presto/presto-server/target/presto-server-${PRESTO_VERSION}.tar.gz ${WORK_DIR}
$ tar -C ${WORK_DIR} -xzf ${WORK_DIR}/presto-server-${PRESTO_VERSION}.tar.gz
$ rm ${WORK_DIR}/presto-server-${PRESTO_VERSION}.tar.gz
$ cp -R /path/to/bin default ${WORK_DIR}/presto-server-${PRESTO_VERSION}

docker buildx build ${WORK_DIR} \
    --platform linux/arm64/v8 \
    -f Dockerfile --build-arg "PRESTO_VERSION=340-SNAPSHOT" \
    -t "presto:${PRESTO_VERSION}-arm64v8" \
    --load
```

The image you want should be listed in the list of images.

```sh
$ docker images
REPOSITORY                                                            TAG                    IMAGE ID            CREATED             SIZE
presto                                                                340-SNAPSHOT-arm64v8   cf9c4124516f        3 hours ago         1.25GB
```

## Run the Container

We can transfer the image by using `save` and `load` command of docker. The following command will serialize the image in the `tar.gz` format so that we can copy the image to the Graviton2 instance through the network. It will take several minutes to complete.

```sh
$ docker save presto:340-SNAPSHOT-arm64v8 | gzip > presto-arm64v8.tar.gz
```

Copy the image to the instance. It will also take several minutes.

```sh
$ scp -i ~/.ssh/mykey.pem \
    presto-arm64v8.tar.gz ubuntu@XXXXXXX.amazonaws.com:/home/ubuntu
```

Using the `load` command will bring the image into the executable format in the instance.

```
$ ssh -i ~/.ssh/mykey.pem ubuntu@XXXXXX.amazonaws.com
$ docker load < presto-arm64v8.tar.gz
```

Finally, you get there.

```
$ docker run -p 8080:8080 \
    -it presto:340-SNAPSHOT-arm64v8
...
WARNING: Support for the ARM architecture is experimental
...
```

Note that Arm support is still an experimental feature as the warning message says. Please let [the community know](https://github.com/prestosql/presto/issues) if you find something wrong using Presto in the Arm platform.

Thanks.

## Reference

- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Presto Docker Image](https://github.com/prestosql/presto/tree/master/docker)
- [AWS Graviton Processor](https://aws.amazon.com/ec2/graviton/)
- [Presto Experiment with Graviton Processor](https://prestosql.io/blog/2019/12/23/Presto-Experiment-with-Graivton-Processor.html)
- [High Performance SQL: AWS Graviton2 Benchmarks with Presto and Arm Treasure Data CDP](https://blog.treasuredata.com/blog/2020/03/27/high-performance-sql-aws-graviton2-benchmarks-with-presto-and-arm-treasure-data-cdp/)