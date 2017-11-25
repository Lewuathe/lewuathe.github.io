---
title: "Maven Wrapper Home"
layout: post
date: 2017-11-22 16:01:39 +0900
image: 'images/'
description:
tag: ["Maven", "Java"]
blog: true
author: "lewuathe"
---

Maven wrapper is a library to make maven build easy. You do not need to install maven manually thanks to maven wrapper because it automatically install the specific maven version into your project. Since I usually use [gradle wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) and [sbt-extras](https://github.com/paulp/sbt-extras), it was very easy to use maven wrapper as well in my Java project. 

But I had a trouble to build a project after switching user. For example, I wanted to create build environment by `root` user but building the project itself should be done by non-priviledged user. I initially thought it can be achieved by `sudo -u lewuathe`:

```
$ sudo -u lewuathe ./mvnw install 
```

But it failed due to `FailNotFoundException`.

```
Exception in thread "main" java.io.FileNotFoundException: /home/lewuathe/.m2/wrapper/dists/apache-maven-3.3.9-bin/2609u9g41na2l7ogackmif6fj2/apache-maven-3.3.9-bin.zip.part (No such file or directory)
    at java.io.FileOutputStream.open0(Native Method)
    at java.io.FileOutputStream.open(FileOutputStream.java:270)
    at java.io.FileOutputStream.<init>(FileOutputStream.java:213)
    at java.io.FileOutputStream.<init>(FileOutputStream.java:162)
```

I was disapponted of this because I believed maven wrapper automatically :( I read [the source code of maven wrapper](https://github.com/takari/maven-wrapper) and finally found a solution. Maven wrapper gets the base directory where maven is installed from [`MAVEN_USER_HOME`](https://github.com/takari/maven-wrapper/blob/02106acbaf8f4695ba40b8da9a0449cb0b204663/src/main/java/org/apache/maven/wrapper/MavenWrapperMain.java#L37) environment variable.

So finally what we need to do is this:

```
$ mkdir /home/lewuathe/.m2
$ MAVEN_USER_HOME=/home/lewuathe/.m2 sudo -u lewuathe ./mvnw ...
```

It worked!


