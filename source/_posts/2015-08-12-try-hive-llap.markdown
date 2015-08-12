---
layout: post
title: "Try Hive LLAP"
date: 2015-08-12 21:06:12 +0900
comments: true
categories: ["Hive", "Big Data"]
author: Kai Sasaki
---

Do you know Hive LLAP? This is [stinger-next project of Hive](http://hortonworks.com/blog/stinger-next-enterprise-sql-hadoop-scale-apache-hive/).
With LLAP, you can pass a sub-second query to Hive. However this project is in progress now. You cannot use this with released Hive.
Today I'd like to describe how to try LLAP in you cluster.

<!-- more -->

Building Hive LLAP is very tough work especially under development state. So there is a project to build Hive LLAP more easily. This is [tez-autobuild](https://github.com/t3rmin4t0r/tez-autobuild). The `llap` branch of this project was created for building Hive LLAP resolving dependencies.

First you have to clone `llap` branch of this project.

```sh
$ git clone -b llap https://github.com/t3rmin4t0r/tez-autobuild.git
```

And build it.

```sh
$ cd tez-autobuild
$ make clean dist install
```

Hive LLAP is now run on Slider. So you can build Slider package with this command.

```
$ make run
```

You can see a package such as `llap-slider-12Aug2015` on current directory. Under this directory, there are several configurations for deploying Hive LLAP with Slider. You can deploy LLAP with `run.sh`.

```
$ cd llap-slider-12Aug2015
$ ./run.sh
```

In order to confirm whether LLAP is running, you can check ResourceManager UI like a normal YARN application. That's all. You can connect LLAP with `hive` command included in this package.

```
$ ./dist/hive/bin/hive
```

**Live Long and Prosper!**
