---
layout: post
blog: true
title: "How to build Storm 0.8.x"
date: 2014-11-24 11:03:57 +0900
comments: true
categories: ["Storm", "build"]
author: Kai Sasaki
---

First of all, current release is now 0.9.x. So this article won't be needed for who don't need to build older version of Storm like me.
Yes, I needed to build 0.8.x on myself. This was a little tough work because the change and availability of build tool([leiningen](http://leiningen.org/))
I hope you all don't have to build older version at your work :)

<!-- more -->

# Set up environment

## Install leiningen

You have to instlal [leiningen](http://leiningen.org/) 1.x, because storm 0.8.x `project.clj` requires it.

    (if-not (re-find #"^1\..*$" lein-version)
      (do (println (str "ERROR: requires Leiningen 1.x but you are using " lein-version))
        (System/exit 1)))

You can download from [here](https://github.com/technomancy/leiningen/releases/tag/1.7.1)
And install it into anywhere you like. (For me, I pleced it under `/opt/)
Then self install for leiningen.

    $ lein self-install

You may see error message about rlwrap. Please install it too.

    $ wget http://dl.fedoraproject.org/pub/epel/6/x86_64/rlwrap-0.41-1.el6.x86_64.rpm
	$ rpm -ivh rlwrap-0.41-1.el6.x86_64.rpm

## Install dependencies about message queue

Storm 0.8.x is depend on ZeroMQ and JZMQ. Install these packages.

### JZMQ
* [JZMQ](https://github.com/zeromq/jzmq)

### ZeroMQ
    $ yum -y install zeromq zeromq-devel

# Build Storm

## Change repository url scheme

This was the most big problem. I was annoyed for about 1 hour. Current sonatype repository is provided with https protocol.
But redirect does not work when I built it. So you have to rewrite `project.clj`.

    $ wget https://github.com/nathanmarz/storm/archive/0.8.2.zip
    $ unzip 0.8.2.zip
    $ chmod +x 0.8.2/bin/build_release.sh
    $ cd 0.8.2

And reqrite project.clj

     :repositories {"sonatype" "http://oss.sonatype.org/content/groups/public/"}
     ;; Rewrite to this. |
     :repositories {"sonatype" "https://oss.sonatype.org/content/groups/public/"}

OK, so it has been all done to build storm project. Let's do it.

    $ bin/build_release.sh

You will be able to find *jar file below target.
Thank you.

