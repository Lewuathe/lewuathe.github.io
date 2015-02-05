---
layout: post
title: "Storm cluster on EC2 with vagrant provider"
date: 2015-02-05 20:34:50 +0900
comments: true
categories: ["AWS", "Storm"]
author: Kai Sasaki
---

The other day, I released [storm deployment tool for QA and development](https://github.com/Lewuathe/storm-devenv), [storm-devenv](https://github.com/Lewuathe/storm-devenv). I update this tool to create cluster on both EC2 and VirtualBox. VirtualBox of course provides us enough
power to check my storm patches is valid or not. But there are some cased when I want to check it on the environment which
is more close to production's one. So it is EC2 for us. storm-devenv now supports EC2 deployment as on VirtualBox.

<!-- more -->

## How to use

You have to install these packages in advance.

* [Vagrant](https://www.vagrantup.com/)
* [Oracle VirtualBox](https://www.virtualbox.org/)
* [vagrant-aws](https://github.com/mitchellh/vagrant-aws)

## Deployment on VirtualBox

As described in [this post](http://www.lewuathe.com/blog/2015/01/16/your-own-cluster-with-storm-devenv/), you have to
build your own storm code because storm-denenv is developed for checking and testing your new feature written for storm itself.
After all packages are setup, the only rest of you task is below one command.

```
$ export VAGRANT_CWD=./providers/virtualbox && vagrant up
```

## Deployment on EC2

In the case of EC2, there is some information you have to obtain in advance. This is the list which you have to set in your environment variables.

* `AMI_ID`: Available AMI's ID
* `AWS_REGION`: Region of EC2 instances
* `AWS_INSTANCE_TYPE`: EC2 Instance type
* `AWS_VPC_SUBNET_ID`: Avalable subnet ID
* `AWS_KEYPAIR_NAME`: Key pair name which you have
* `AWS_SECURITY_GROUPS`: Available security group
* `AWS_ACCESS_KEY_ID`: You AWS access key ID
* `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
* `AWS_PRIVATE_KEYPATH`: The full path of your AWS key pair

Once you finished setup these values in your `env`, all you have to do is one command.

```
$ export VAGRANT_CWD=./providers/aws && vagrant up
```

You can see five instances was launched in your selected region
Although I think it enables us to hack storm code itself more easily, there are some obstacles to make it better tool as possible. So if you have any questions or find any issues please let me know [here](https://github.com/Lewuathe/storm-devenv/issues). Patches are always welcome!
I hope you can enjoy hacking storm itself. Thank you.
