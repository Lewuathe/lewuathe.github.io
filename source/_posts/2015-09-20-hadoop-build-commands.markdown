---
layout: post
title: "Hadoop build commands"
date: 2015-09-20 10:32:17 +0900
comments: true
categories: ["Hadoop"]
author: Kai Sasaki
---

You might have a experience when you cannot remember the command how to build in your purpose.
How to skip tests? How to build tar.gz package? How to build native packages?

<!-- more -->

These information are in [BUILDING.txt](https://github.com/apache/hadoop/blob/trunk/BUILDING.txt).
So in this post, I'd like to file these command you may often use in your hadoop projects like a cheetsheet.

| Definition | What for? |
|:----|:----|
| -Dtar | Building package as tar.gz format with -Pdist.  |
| -Pdist | Profile for building package for distribution.   |
| -Pdocs | Generate documentation and bundle it with package with -Pdist. |
| -Pnative | Profile for building native source files. |
| -DskipTests | Skip all unit tests. |

Current `trunk` repository seems to have problem to build with JDK8. So this is the command when you want to build hadoop package simply.

```bash
$ cd hadoop
$ cd JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.7.0_71.jdk/Contents/Home mvn -Pdist,native,tar -DskipTests -Dtar clean package
```

Hadoop project depends on [ProtocolBuffer](https://developers.google.com/protocol-buffers/?hl=ja) and other projects.
But there is no need to worry about it if you have a little knowledge about [Docker](https://www.docker.com/). There is a definition and images
for building hadoop project on Docker. All these configurations are written in `start-build-env.sh`. About this script the detail was written in [this entry](http://www.lewuathe.com/blog/2015/08/20/build-hadoop-on-macosx/).

Thank you.
