---
title: "Tuning G1 GC algorithm on JVM"
layout: post
date: 2016-10-21 23:33:47 +0900
image: 'images/'
description:
tag: ["JVM", "Java", "GC"]
blog: true
jemoji:
author: "lewuathe"
---

Recently I faced the necessity to tune garbage collection of our Java application. The application is [Presto](https://prestodb.io/)
, distributed query execution engine. It requires a lot of memory but needs to achieve high throughput and low latency.
So I read a book about tuning Java applications.

[![Java Performance](/images/java_performance.png)](https://www.oreilly.co.jp/books/9784873117188/)

Since Presto uses G1 GC algorithm, I want to summarize how to tune G1 GC algorithm in general here.
G1 GC is designed not to require a lot of tuning. We can achieve optimal settings in most cases with adaptive garbage collection algorithm.
So please refer these advice only if you can believe it can improve performance. G1 GC might be able to do automatically.

## Make larger old area

This is the simplest way to avoid full GC in G1 as well as other algorithms like CMS. If the size of old area is increased, we may not
so many full GC. But there is a tread-off. In that case, the young area size is decreased. So we may have more minor garbage collection which
does small stop-the-world. On the contrary, if we decrease old area, it can cause many time full GC while achieving shorter time garbage collection.
The size of young area and old area can be changed with `-XX:NewRatio` or `-XX:G1NewSizePercent`.

|name|default value|
|-XX:NewRatio| 8(client VM), 2(server VM)|
|-XX:G1NewSizePercent	| 5 |

## Increase the background thread

If you have sufficient CPU cores, increasing the number of background thread can improve the performance. You can change the number of background thread
by setting `-XX:ParallelGCThreads`. The default value is same to the core of your machine. You can reduce the time of garbage collection by increasing
this setting.

## Run background thread frequently

Starting background thread as fast as possible can contribute for improving performance because background thread does not run frequently
and cannot finish marking before reaching limit of old area, it can cause full GC. We can let background thread starts time by setting
`-XX:InitiatingOccupancyPercent`. This is the ratio of heap usage against total heap size. Decreasing the value can be a pressure to start
background thread fast. The default value is 45. But one thing to note is that if the value is too small, minor garbage collection run too frequently.
It cost CPU cycle and can affects application performance itself. Please check CPU usage of your application.

## Let GC process more data

Once a concurrent cycle finishes, the next concurrent cycle will not start until marked regions in old area is empty. So increasing the data which is
processed by one garbage collection cycle of old are can contribute starting marking phase fast. There are two settings we can set publicly.
`-XX:G1MixedGCCountTarget` and `-XX:MaxGCPauseMillis`. Full garbage collection in G1 GC is called mixed GC because it does minor GC on young area
and full GC in old area at the same time. And it runs some times until almost all marked regions are free. `-XX:G1MixedGCCountTarget` specifies the maximum
number that mixed GC can try to make marked regions free. So decreasing this value can reduce the time of total time of mixed GC in one cycle. 	
`-XX:MaxGCPauseMillis` is the maximum time span that mixed GC stops the world. Mixed GC tries to free marked region at most the count specified by `-XX:G1MixedGCCountTarget`.
If it does not reach the maximum time specified by `-XX:MaxGCPauseMillis`, the mixed GC thread tries to free more memory and it can reduce the total time of
full GC cycle.

|name|default value|
|-XX:G1MixedGCCountTarget|8|
|-XX:MaxGCPauseMillis|200|

Though I listed the tuning settings here, it is important to profile your Java application in advance. G1 GC will work fine in the most case and it is designed so.
So please collect profiling metrics and try to these values to improve GC performance.

Thank you.

Reference: [Garbage First Garbage Collector Tuning](http://www.oracle.com/technetwork/articles/java/g1gc-1984535.html)
