---
title: "Professional Hadoop"
layout: post
date: 2016-06-09 21:02:02 +0900
image: 'images/'
description:
tags: ["Hadoop", "Book"]
blog: true
jemoji:
---

[Wiley](http://as.wiley.com/) gave me another chance to write a book about Big Data technology. This was offered at the almost same time
when I started to write [Spark book](http://www.lewuathe.com/blog/spark-in-production/) that is introduced previously because they expected me
to write something about Hadoop too. So [this is a book](http://shop.oreilly.com/product/9781119267171.do) about Hadoop especially for deep dive into core Hadoop technology and recent version which has a lot of advanced and cutting edge features.

[![Professional Hadoop](/images/posts/2016-06-09-professional-hadoop/professional_hadoop.png)](http://shop.oreilly.com/product/9781119267171.do)

<!-- more -->

You may have read [Hadoop Definitive guide](http://shop.oreilly.com/product/0636920021773.do) at least once.
This is one of the best technical book I've ever read. Almost all of my initial knowledge around Hadoop was owe totally to this book.
So I hope "Professional Hadoop" can also become good resource to Hadoop developers or administrators just as me when I read the definitive guide.
Hadoop is actively developed even now and takes aggressive and challenging features into itself because the potential and possibility of
Big Data technology is seeing an unlimited horizon. Since Hadoop is a core technology of this field, we need to keep up with fast-changing trend.

This is the book including the latest and challenging Hadoop technologies in recent years. I've written chapter2 and chapter3, storage and computation.
HDFS is a well known storage layer system of Hadoop. I introduced some basics of HDFS architecture, tools and how to operate it. The most fun part for me was a section
about HDFS Erasure Coding. HDFS Erasure Coding is now actively developed and under tested though it is not released yet. Even though you have to build Hadoop by yourself
and interface, API can be changed by its release, I wanted to introduce some points of this cutting edge technology.

Chapter3 was written about mainly MapReduce. To be honest, I found several features and configurations around MapReduce framework through this writing.
I was surprised that even such mature framework has several points to be learned with fresh feeling, though it might be just due to my inexperience.
Taking the fact into consideration that MapReduce is running now on a lot of enterprise system, enhancement of knowledge of distributed execution engine such
as MapReduce can contribute to our system's reliability and performance.

I also wrote the integration between Hadoop and cloud service. Nowadays it is not necessarily the best solution to use Hadoop on-premise and operate by themselves.
So knowing what we can do with cloud based Hadoop is an important knowledge if we want to use Hadoop in low cost and on stable environment. Of course one of the best solution is [Treasure Data](https://www.treasuredata.com/)! Treasure Data is a cloud based data management platform and also a big user and developer of Hadoop and
including ecosystems. I introduced the merit and features of Treasure Data from the viewpoint of cloud based Hadoop in a section.

The last but not least, the co-authors of this book are very famous and experienced engineers. I feel embarrassed to be listed in these authors.
But it was a good chance to motivate me to learn various thing further. The stimulus from them and the book must have a good influence on my attitude
as a software engineer. I cannot say thank you enough to co-authors and publishers, Wiley and [Bleeding Edge press](bleedingedgepress.com).
It was a impressive event for me.

Thanks you so much.
