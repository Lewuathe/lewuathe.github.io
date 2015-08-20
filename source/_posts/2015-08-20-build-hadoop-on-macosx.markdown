---
layout: post
title: "Build Hadoop on Mac OSX"
date: 2015-08-20 18:32:49 +0900
comments: true
categories: ["Hadoop", "Docker"]
author: Kai Sasaki
---

Building Hadoop on MacOSX is a little tough work. You have to pay attention to the version of JDK and `ProtocolBuffer`.
In spite of this fact, there are some times when you want to use other versions in case of building other tools.
Especially there might be a lot of cases when you want to use JDK8 and it is even recommended.

<!-- more -->

Today, I found Hadoop can be build in [Docker](https://www.docker.com/) container according to the attached instruction on OSX.
I am also a novice of Docker. So I have a little knowledge and experience of Docker container. But Hadoop projects gives you
setting up script for you and instruction. Although these were already fully written in `BUILDING.txt`,

```sh
## First make sure Homebrew has been installed ( http://brew.sh/ )
$ brew install docker boot2docker
$ boot2docker init -m 4096
$ boot2docker start
$ $(boot2docker shellinit)
$ ./start-build-env.sh
```

That's all. It's easy way. There seems to be some issues about performance within `boot2docker`. Anyway it's the easiest way
to build Hadoop on MacOSX. Try it!!
