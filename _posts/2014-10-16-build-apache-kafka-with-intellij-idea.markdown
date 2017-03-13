---
layout: post
blog: true
title: "Build Apache Kafka with IntelliJ IDEA"
date: 2014-10-16 20:15:34 +0900
comments: true
categories: ['Kafka', 'Build']
author: Kai Sasaki
---

[Apache Kafka](http://kafka.apache.org/) is today's topic. I am getting started developing realtime data processing platform which uses [Apache Storm](https://storm.incubator.apache.org/). 
Storm receives data from Kafka as messages. So I'd like to learn the architecture of Kafka and how to build it. 

<!-- more -->

You can learn [here](http://kafka.apache.org/documentation.html) very detail. So I am going to introduce how to build Kafka project on MacOSX and IntelliJ IDEA.

# Gradle
Kafka is the project made by [Gradle](http://www.gradle.org/). Of course you can download and compile gradle itself [here](http://www.gradle.org/). But if your machine is MacOSX, you can install with Homebrew more easily.

    $ brew install gradle

That's all!

# Build
You can checkin Kafka source code repository.

    $ git clone http://git-wip-us.apache.org/repos/asf/kafka.git kafka

And build whole project with gradle.

    $ cd kafka
    $ gradle

OK. You can get all built files under `gradle/wrapper/*`. In this directory, there is a class which generate IntelliJ setting.
You can use it with this command.

    $ ./gradlew idea

If there are no problem through this process, all you have to do is finished except one thing. Just open it with IntelliJ IDEA.

![screenshot](/images/posts/2014-10-16-gradle-and-kafka/screenshot.png)

It very easy, isn't it? All process is written in [here](https://cwiki.apache.org/confluence/display/KAFKA/Developer+Setup). Of course you can also use Eclipse.

Thank you!

