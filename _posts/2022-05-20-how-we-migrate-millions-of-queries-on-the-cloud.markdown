---
title: "How We Migrate Millions of Queries on The Cloud"
layout: post
date: 2022-05-20 11:29:00 +0900
image: 'assets/img/posts/2022-05-20-how-we-migrate-millions-of-queries-on-the-cloud/catch.jpg'
description:
tag: ['SQL', 'Cloud']
blog: true
author: "Kai Sasaki"
---

As a software engineer maintaining running service on-site, you may have the experience of migrating something owned by users to another platform without breaking any visible functionality. It often happens when you introduce a new version of the software or apply security patches.

But when it comes to the scale of the cloud and web, this task turns into a colossal challenge. The number of resources we must migrate is massive. Luckily or unluckily, our users may hugely rely on these resources we manage. So we have to keep them available during any time of the migration. It takes unignorable time to complete all such demands, checking the compatibility and consistency of the new platform for such resources. It may seem a familiar situation to you regardless of the type of resources in the service.

We, [Treasure Data](https://www.treasuredata.com/), deal with millions of queries for the data analysis. They were written by marketers, analysts, and engineers in our customer's companies. So we have to keep them running without any problem every day.

Today, you may find our approach to this challenge in the following paper. We describe how to tackle this common problem in the research published in this year's [DBTest workshop](https://dbtest-workshop.github.io/).

[Taro L. Saito, et al., "Journey of Migrating Millions of Queries on The Cloud", 2022](https://arxiv.org/abs/2205.08664)

[![Architecture](/assets/img/posts/2022-05-20-how-we-migrate-millions-of-queries-on-the-cloud/architecture.png)](https://arxiv.org/abs/2205.08664)

I have contributed to initiating the framework to achieve the automatic query simulation. This framework proved helpful in the past five years and successfully lowered the hurdle to safely migrating running queries onto a new platform, an updated version of Trino.

We do not publish any code for the framework, but we contributed to finding several bugs during this simulation in [Trino](https://github.com/trinodb/trino/issues). In addition to that, there should be a lot of learnings generally applicable to various types of migration efforts you have encountered. I hope this paper is informative and insightful for every developer.

Thank you!


