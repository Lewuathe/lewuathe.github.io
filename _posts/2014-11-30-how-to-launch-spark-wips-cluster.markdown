---
layout: post
blog: true
title: "How to launch WIP Spark cluster"
date: 2014-11-30 00:30:30 +0900
comments: true
categories: ["Spark", "EC2"]
author: Kai Sasaki
---

In the process of development spark, it is not uncommon to investigate the performance of development version on EC2 cluster.
However, this development version is of course work on process. So I thought it was difficult to launch with ec2 script included 
spark project. But today I found there is an easy way to do that with only one option.

<!-- more -->

Do you have already spark code which is attached your patch? OK, first you have to push it to remote repository.

## Push it

    $ cd your-spark-project
    $ git push origin your-spark-branch

## Record commit hash
Retrive from your repository with ec2 script, git commit hash is needed such as cfaf9be21141856c2b9ec5bb795fe53c2a222176 

    $ git log
    commit cfaf9be21141856c2b9ec5bb795fe53c2a222176
    Author: your-name <your-name@example.com>
    Date:   Sun Nov 30 00:12:08 2014 +0900
  
    Add docs about spark-git-repo option 

However this hash code is a little long to hand type. You can use short version and confirm it on GitHub's commits page.

![commit-hash](/images/posts/2014-11-30-how-to-ec2-spark-cluster/commit-hash.png)

All you need is this only 7 characters. This is the beyond half way to complete it. How easy is it!
At last you type launch commoand with spark-ec2 script.

## Launch

    $ ./spark-ec2 -k <Your EC2 keyname> \ 
                  -i <Your EC2 keyfile path> \
                  --slaves=3 \  
                  --spark-git-repo=https://github.com/<Your name>/spark.git \
                  --spark-version=<Commit hash> launch your-spark-cluster 

You obtain your patched spark cluster. You can run any applications on this cluster and look into some metrics through ganglia which is automatically
setup with this script. This is the great way to investigate your spark on real cluster.

Thank you.

