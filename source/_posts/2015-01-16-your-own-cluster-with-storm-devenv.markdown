---
layout: post
title: "Your own cluster with storm-devenv"
date: 2015-01-16 09:13:49 +0900
comments: true
categories: ["storm", "Vagrant"]
author: Kai Sasaki
---

As written in [this post](http://www.lewuathe.com/blog/2015/01/12/making-storm-cluster-for-development/),
I developed a tool for constructing storm cluster more easily.
When you want to add new features or investigate some bugs issued by others,
this tool will be useful. Usually this kind of tools can only construct a cluster
with released packages. [storm-devenv](https://github.com/Lewuathe/storm-devenv)
enables us to construct storm cluster with your own storm code on your local machine.
Vagrant and VirtualBox make is possible. I think that we can apply same process to AWS
EC2 instances by using Vagrant. So I choose Vagrant as constructing tool.
And as provisioning tool, I wrote chef cookbooks which is a de fact tool for configuration tool.
I'd like to introduce storm-devenv mode detail in this post.

<!-- more -->

storm-devenv repository is [here](https://github.com/Lewuathe/storm-devenv).
If you are familiar with Vagrant and Chef cookbooks, you can easily understand all codebase.

## Prerequisites

storm-devenv uses Vagrant and Chef therefore first you have to install these software.
Chef packages are listed in `Gemfile` so first restore rubygems.

```
$ cd storm-devenv
$ bundle install
```

Vagrant can be installed from [here](https://www.vagrantup.com/downloads.html). storm-devenv uses VirtualBox as provider.
You have to also install VirtualBox from [here](https://www.virtualbox.org/wiki/Downloads).
When you have done, almost all tasks have been finished.

## Build your own storm code

storm-devenv is for development of storm code itself. So if you have no storm code as tar format, I recommend you to build it.
You can see how to build in [DEVELOPER.md](https://github.com/apache/storm/blob/master/DEVELOPER.md). Or if you want to try with
released package, please download from [official link](https://storm.apache.org/downloads.html). These packages should be put on
`site-cookbooks/storm/files/default`.

## Launch Cluster

At last, all you have to do is a command.

```
$ vagrant up
```

It will take about 10 minutes. Of course this time depends on your environment and machine spec. You can confirm the state
of this cluster from [http://192.168.50.4:8080](http://192.168.50.4:8080/index.html), if you don't change your nimbus host ip.

## Future works

storm-devenv has several improvement points.

* Storm cookbook should be under one version controle separately
* Support AWS EC2
* Make it easy to construct selfmade storm

I'd like to debug and develop improvements with storm-devenv from now. If you have any idea and opinion please let me know.
Thank you.
