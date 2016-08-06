---
title: "Multi node Presto cluster on docker"
layout: post
date: 2016-08-06 21:02:10 +0900
image: 'images/'
description:
tag: ["Presto", "SQL"]
blog: true
jemoji:
author: lewuathe
---

Recently I'm getting started using [Presto](http://prestodb.io). This is a distributed SQL query engine like Hive.
I'm working on Hadoop, Hive until now. So I have though there are a lot of similarity between Hive and Presto.
This is almost true in terms of user interface and SQL syntax. But Presto does not depend on Hadoop distributed
architecture. Resource scheduling, fault tolerance and query execution are done by Presto itself. Presto can be
introduced as a ecosystem of Hadoop family, but it does not use Hadoop totally. Of course we can find someone
try to use [Presto on YARN](http://teradata.github.io/presto/docs/141t/server-installation.html) and it can be
integrated.

<!-- more -->

As I did as Hadoop engineer, I want to read code and try to change codebase of Presto because it is the shortest way
to understand internal architecture and some of tips to use distributed system efficiently.

Presto install instruction can be found [official documentation](https://prestodb.io/docs/current/installation/deployment.html)
or [Teradata documentation](http://teradata.github.io/presto/docs/141t/server-installation.html). These instructions are written
mainly for production usage. However I want to try Presto easily for development usage, which means we can build, launch, test cycle
fast.

So that's the reason why I wrote [docker-presto-cluster](https://github.com/Lewuathe/docker-presto-cluster). docker-presto-cluster
was made for same reason of the [docker-hadoop-cluster](https://github.com/Lewuathe/docker-hadoop-cluster).
I want to deploy self-build package onto multi node cluster easily. docker-hadoop-cluster enabled me to do so. I think we can
same development style of Presto by using docker-presto-cluster.

The usage is very simple.

- 1 Build base image which includes presto server package and install dependencies.

```
$ cd presto-base
$ docker build -t lewuathe/presto-base:latest .
```

- 2 Build coordinator and worker container images with docker-compose.

```
$ docker-compose build
```

- 3 Launch multi node Presto cluster on docker container.

```
$ docker-compose up -d
```

That's it. You can see Presto coordinator UI from http://localhost:8080 since docker container expose 8080 port number.
One thing to note is that it does not support self-build package deploy. As defined in Dockerfile, it downloads the latest
released package. The reason why I did this workaround was that I couldn't launch Presto cluster with self-build package
on OSX due to BSD virtual machine type error. I'm not sure why this error was thrown, but OSX build package does not work
on Linux machine like docker container. (Of course you can run OSX build package on OSX)

I'm investigating the reason. At the same time, I'm now preparing docker image to build Presto package which provides us
Presto build environment on Linux. After this, we can deploy self-build Presto package more easily.

Thanks.
