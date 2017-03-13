---
layout: post
blog: true
title: "Drill Cookbook"
date: 2015-04-21 21:05:37 +0900
comments: true
categories: ["Drill"]
author: Kai Sasaki
---

Recently I read [Apache Drill](http://drill.apache.org/) documents, source code and paper. My major task and interest were focused on realtime processing and Hadoop resource management. So I have no knowledge about adhoc query platforms in spite of the fact that I am a big data developer.So in this chance I decided to learn more about SQL platforms which are build on Hadoop such as Hive, Presto and Drill. The most interesting one among these platforms to me is Apache Drill because it is a newest one. And I think it supports Dremel architecture most faithfully(Of course it is my opinion). So my target is set as Apache Drill.

<!-- more -->

Especially today, I want to talk about drill-cookbook I wrote the other day in order to test drill cluster more easily.

[drill cookbook](https://supermarket.chef.io/cookbooks/drill)

# What can we do with this cookbook?

This cookbook enables us to

* Deploy drillbit from released package.
* Deploy drillbit from self package build by yourself.
* Launch ZooKeeper server.
* Start drillbit daemon.

You can do anything necessary other than creating data source. Even if you want to connect external data source such as HDFS or HBase,
only you have to do is launching these services on the same machine. You will find correspond cookbooks. There are several [serverspec](http://serverspec.org/) test in this cookbook.

But I think it is insufficient. Moreover, these cannot be run automatically.
ChefDK and test-kitchen didn't work properly on [TravisCI](travis-ci.org). I send a email about this issue, and received a reply.
I heard that TravisCI was now preparing new virtual machine infrastructure. I'm looking forward when the day this new technology is released.
Of course patches are always welcome. If you have find any other nice way to do continuous integration on this cookbook, please let me know.

Thank you.
