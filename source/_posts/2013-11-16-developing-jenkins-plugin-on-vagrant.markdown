---
layout: post
title: "Developing Jenkins plugin on Vagrant"
date: 2013-11-16 21:09
comments: true
categories: ["Jenkins", "Vagrant", "Ubuntu"]
author: Kai Sasaki
---

Recently I investigate the scalability of Jenkins. In my idea, I want to make hot standby Jenkins server with NFS. So the plugins which enable us to do that are required. And for my study, I decided to develop on Vagrant and VirtualBox. It costs me very little because there is no need to get real server.  So in this post, I will describe how to set up your jenkins plugin environment on your vagrant Ubuntu.

## Start vagrant

My `Vagrantfile` is below. Before this, you should download precise64 box on vagrant [site](http://www.vagrantbox.es/)

```
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network :forwarded_port, guest: 8080, host: 8080

 end
```
Jenkins plugin server starts on port 8080. So you need to write guest port 8080. Host port can be written any number.
And start vagrant.

```
$ vagrant up
```

## Set up maven3

Jenkins plugins are build with Maven. In this time, Maven3 can build sample plugin easily, so I recommend that you download maven3.

```
$ sudo apt-get install maven
```

## Write settings.xml

Write settings.xml as below.

```
<settings>
  <pluginGroups>
    <pluginGroup>org.jenkins-ci.tools</pluginGroup>
  </pluginGroups>

  <profiles>
    <!-- Give access to Jenkins plugins -->
    <profile>
      <id>jenkins</id>
      <activation>
        <activeByDefault>true</activeByDefault> <!-- change this to false, if you don't like to have it on per default -->
      </activation>
      <repositories>
        <repository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </pluginRepository>
      </pluginRepositories>
    </profile>
  </profiles>
  <mirrors>
    <mirror>
      <id>repo.jenkins-ci.org</id>
      <url>http://repo.jenkins-ci.org/public/</url>
      <mirrorOf>m.g.o-public</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

## JDK!!

I failed to create my plugin in this time bacause of lack of JDK. Ubuntu 12.04 LTS doesn't have JDK in own image. You have to install it.

```
$ sudo apt-get install default-jdk
```

## Build plugin

Building plugin with maven command.

```
$ mvn install
```

And demonstrate your plugin.

```
$ mvn hpi:run
```

You can see Jenkins web UI on http://localhost:8080/jenkins unless maven command has not exit.
So now, I can get multi Jenkins server for mutual mount on NFS. My Jenkins study has been continued.
