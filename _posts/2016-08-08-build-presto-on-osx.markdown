---
title: "Build Presto on OSX"
layout: post
date: 2016-08-08 20:25:45 +0900
image: 'images/'
description:
tag: ["Presto", "OSX"]
blog: true
jemoji:
author: lewuathe
---

As described [here](http://www.lewuathe.com/blog/multi-node-presto-cluster-on-docker/), we cannot run Presto package build on OSX. Mainly it was caused by JNI side issue and machine architecture. I knew the issue from [Issue 3849](https://github.com/prestodb/presto/issues/3849).

> It looks like you're running on ppc64. Presto only supports x86_64 on Linux (required for bundled Hadoop JNI libraries) and has many assumptions about the architecture being little endian.

I couldn't run Presto build on OSX when I deploy on Ubuntu docker container due to this issue. But I don't have any Linux machine easily. (Of course I can launch EC2 instance sometimes though.) So I found a workaround to run Presto without Linux machine. It can be done with [presto-build](https://github.com/Lewuathe/presto-build).

[https://github.com/Lewuathe/presto-build](https://github.com/Lewuathe/presto-build)

<!-- more -->

# Why presto-build?

Presto built on OSX does not work with Linux because of JNI issue. We will see not found BSDVirtualMachine exception. And also Presto only supports x86_64 on Linux as described [here](https://github.com/prestodb/presto/issues/3849). So the easiest way to build Presto on Linux running x86_64 machine. But how can we build without Linux (like me!). I want to described a way to build Presto which can run on Linux without Linux here.

# How to build

## 1. Clone repository

```bash
$ git clone git@github.com:Lewuathe/presto-build.git
```

## 2. Set presto project directory

```bash
$ export PRESTO_HOME=/path/to/presto
```

## 3. Remove presto-doc

Due to incompatibility with PPC64 architecture. The detail is written [here](https://github.com/prestodb/presto/issues/3849).

```
$ cd /path/to/presto
$ vi pom.xml
```

Here, you need to comment out presto-doc from module

```
<!-- <module>presto-docs</module> -->
```


## 4. Start docker container

```
$ cd presto-build
$ ./start-build-env.sh
```

Now you can build presto package on this container. The simplest command to build is

```
$ ./mvnw clean package -DskipTests
```

presto-build is distributed under MIT License. Please feel free to let me know if you know any other workaround to build Presto on OSX.

Thank you.
