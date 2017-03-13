---
layout: post
blog: true
title: "Making storm cluster for development"
date: 2015-01-12 19:04:58 +0900
comments: true
categories: ["Storm", "Development"]
author: Kai Sasaki
---

When you develop big data processing platform such as [Hadoop](http://hadoop.apache.org/), [Spark](http://spark.apache.org/) and [Storm](http://storm.apache.org/), you need to construct a cluster. You can create it with whichever virtual machines and real server. Personally it is hard to obtain real servers. Setting up networks and configurations are tough work. So you might use virtual machines, [EC2](http://aws.amazon.com/ec2/) , [VirtualBox](https://www.virtualbox.org/). Today I'd like to introduce some options to create your own storm cluster for development of new features and investigation of problems.

<!-- more -->

## [storm-deploy](https://github.com/nathanmarz/storm-deploy)

[storm-deploy](https://github.com/nathanmarz/storm-deploy) is Clojure scripts for creating storm cluster on Amazon EC2. This is developed by [Nathan Marz](https://github.com/nathanmarz) who is the lead of storm project. You can regard this project as the official one supported by apache storm project. And also creating process is very simple.

```
$ lein deploy-storm --stop --name mycluster
```

However there seems to be no active development on it and I faced some problems which is not fixed original master branch when I used `storm-deploy`. So I think you cannot use original `storm-deploy` as itself.

## [Wirbelsturm](https://github.com/miguno/wirbelsturm)

Wirbelstrum uses puppet and vagrant for configuration. I confirmed this tool is working with vagrant v1.6.5. (This does't work with vagrant above v1.7.x). Preparing your environment if you have not develop ruby project, and creating cluster takes some time. But what you have to do is very simple.

```sh
$ git clone https://github.com/miguno/wirbelsturm.git
$ cd wirbelsturm
$ ./bootstrap     # <<< May take a while depending on how fast your Internet connection is.
$ vagrant up      # <<< ...and this step also depends on how powerful your computer is.
```

I think this is the best tool if you want to only getting started or try storm platform. In this time I want to try my own storm project which is added new feature by my own. I cannot found any easy way to change configuration about base storm repository and branch name. It means it is hard to try my own feature developed on storm cluster. This fact cannot enable me to reach my goal.

## [storm-vagrant](https://github.com/ptgoetz/storm-vagrant)

This project is maintained by [P. Taylor Goetz](https://github.com/ptgoetz) who is one of the committer of storm project. You can call this semi-official project supported by apache committers. This is the lightest project introduced by this post. The essence is included in `Vagrantfile`

```rb
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define "zookeeper" do |zookeeper|
    # Define zookeeper virtual machine
  end

  config.vm.define "nimbus" do |nimbus|
    # Define nimbus virtual machine
  end

  config.vm.define "supervisor1" do |nimbus|
    # Define supervisor1 virtual machine
  end

  config.vm.define "supervisor2" do |nimbus|
    # Define supervisor2 virtual machine
  end
end
```

All configuration is done with shell script. So all you have to know is the knowledge about vagrant. It is easy to understand and modify storm-vagrant. Unfortunately it looks no active development on this project. So I decided to fork this project and modify for my own goal. I want to make it for general purpose as possible. At last I'll share through here. Thank you.
