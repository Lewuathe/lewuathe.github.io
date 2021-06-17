---
title: "CIS Compliance Benchmark for AWS"
layout: post
date: 2021-06-17 10:14:17 +0900
image: 'assets/img/posts/2021-06-17-cis-compliance-benchmark-for-aws/catch.jpg'
description:
tag: ['AWS', 'CIS', 'Compliance', 'Security']
blog: true
author: "Kai Sasaki"
---

Keeping the cloud infrasturucture secure is an amazingly critical requrements these days to reassure users. But the process for that is complicated and time-consuming. Finding all vulnerable points is difficult at the first place. Although there are some benchmarks provided by security authorities such as [CIS](https://www.cisecurity.org/cis-benchmarks/), it is not easy to apply them in our cloud infrastructure. I thought that until **TODAY**.

I discovered a mod for [steampipe](https://steampipe.io/) to run CIS compliance benchmark in public cloud infrasturucture like AWS and found it useful to reveal the vulnerability our infrastructure may suffers from.

[turbot/steampipe-mod-aws-compliance](https://github.com/turbot/steampipe-mod-aws-compliance)




# How to use