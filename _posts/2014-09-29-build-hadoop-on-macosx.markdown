---
layout: post
blog: true
title: "Build Hadoop on MacOSX"
date: 2014-09-29 20:59:22 +0900
comments: true
categories: ["Hadoop", "MacOSX"]
author: Kai Sasaki
---

I am not a veteran Java developer. I don't understand the detail of Java development environment such as build tool or some type of libraries.
Today, I realised that I need to develop or understand architecture of Hadoop. Hadoop seems to use some kind of Java development tools. Maven, ProtocolBuffer, CMake and so on.
So in this article I want to record my environment for building hadoop projects on MacOSX.

<!-- more -->

# Prerequisites

* JDK 1.6+
* Maven 3.0 or later
* ProtocolBuffer 2.5.0
* CMake 2.6 or newer (if compiling native code)
* Zlib devel (if compiling native code)
* openssl devel ( if compiling native hadoop-pipes )
* Internet connection for first build (to fetch all Maven and Hadoop dependencies)

You also can see this list on [BUILDING.txt](https://github.com/apache/hadoop/blob/trunk/BUILDING.txt). On MacOSX, you don't need to install JDK and openssl.
Within this list, all you need to install are CMake and ProtocolBuffer.

## ProtocolBuffer

Download from [here](https://code.google.com/p/protobuf/downloads/list). After unziping it, you can walk ordinal steps.

    $ ./configure
	$ make
	$ make install

## CMake
You can install CMake with Homebrew. It is the easiest way.

    $ brew install cmake

All dependencies are installed on your machine now. Let's checkout hadoop source code.

# Hadoop Project

    $ svn checkout http://svn.apache.org/repos/asf/hadoop/common/trunk/

Notice: I tried hadoop GitHub repository, but it was very slow to download it. I recommend you to checkout from svn repository.

And build it.

    $ mvn package -DskipTests -Pdist -Dtar

Because of some broken tests, you have to write `skipTests` option. With this command you can command line tools and jar files in `hadoop-dist/target/hadoop-X.X.X-SNAPSHOT` 

    $ bin/hadoop version
	Hadoop X.X.X-SNAPSHOT
	Subversion https://svn.apache.org/repos/asf/hadoop/common -r 1511192
	Compiled by hadoopworld on 2013-08-07T07:01Z
	From source with checksum c8f4bd45ac25c31b815f311b32ef17
	This command was run using ~/work/trunk/hadoop-dist/target/hadoop-X.X.X-SNAPSHOT

All configuration files are under hadoop-dist directory. You can rewrite xml files to change Pseudo distributed mode from stand alone mode.
After finishing all tasks, I found nothing was hard. I want study the detail of architecture and codebase of hadoop and start writing some patches for hadoop project.
Thank you.
