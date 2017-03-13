---
title: "About BlinkDB"
layout: post
date: 2016-11-08 22:15:07 +0900
image: 'images/'
description:
tag: ["BlinkDB", "Presto"]
blog: true
jemoji:
author: "lewuathe"
---

Today I found a interesting commit in Presto project.

[Remove support for approximate queries](https://github.com/prestodb/presto/commit/01718217269d9024ddb059f7190ad66744ee78d4)

What is approximate queries? Why do we use approximate queries?

The idea was originally developed in [BlinkDB](http://blinkdb.org/). According to the official website of BlinkDB,
it's called *approximate query engine*.

> BlinkDB is a massively parallel, approximate query engine for running interactive SQL queries on large volumes of data. It allows users to trade-off query accuracy for response time

Distributed processing engine on huge data often show bad performance. It can caused by various reasons such as data size, multi tenancy and network issues.
BlinkDB enables us to set constraint on SQL performance. We can do that SQL-style declarative queries. The sample is shown [here](http://blinkdb.org/).

![example](/images/posts/2016-11-08-about-blinkdb/example.png)

BlinkDB do sampling in order to satisfy constraint. Sampling is delegated to sampling module which solves combinational optimization problem.
So sampling module can choose samples while minimizing the statistical bias.

After a job is submitted, BlinkDB create a profile with running a query on small samples at runtime. So it can choose best samples for satisfying constraint.

![architecture](/images/posts/2016-11-08-about-blinkdb/architecture.png)

Finally it submit a job to actual distributed execution engine. One thing to note is that it can calculate approximate error of the result.
So we can decide the result can be accepted or not in reasonable time.

This is interesting idea and product. On the evidence BlinkDB received best paper award in ACM EuroSys 2013.

[BlinkDB: Queries with Bounded Errors and Bounded Response Times on Very Large Data](https://sameeragarwal.github.io/blinkdb_eurosys13.pdf)

Although Presto try this feature as experimental one, it removed as it is not used in production. Surely many users want to calculate accurate number
rather than approximate one in reasonable time in my experience. So it might not fit in production or enterprise usage.

But it was a good chance for me to look into some research in database. Though I'm a software engineer in a field of database or distributed system,
I'm not so familiar with the latest and cutting-edge research in the field. I'll keep reading papers and catch up the knowledge we should know at least.

Thank you.
