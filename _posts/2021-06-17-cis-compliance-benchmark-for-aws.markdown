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

Keeping the cloud infrastructure secure is an amazingly critical requirement these days to reassure users. But the process for that is complicated and time-consuming. Finding all vulnerable points is difficult at the first place. Although there are some benchmarks provided by security authorities, such as [CIS](https://www.cisecurity.org/cis-benchmarks/), it is not easy to apply them in our cloud infrastructure. I thought that until **TODAY**.

I discovered a mod for [steampipe](https://steampipe.io/) to run CIS compliance benchmark in public cloud infrastructure like AWS and found it helpful to reveal the vulnerability our service may suffer from.

[turbot/steampipe-mod-aws-compliance](https://github.com/turbot/steampipe-mod-aws-compliance)

# How To Use

We need to install the AWS plugin and mod in addition to `steampipe` itself.

```bash
# Install steampipe
$ brew tap turbot/tap
$ brew install steampipe

# Install aws plugin
$ steampipe plugin install aws
```

Get the mod for compliance benchmark.

```bash
$ git clone git@github.com:turbot/steampipe-mod-aws-compliance
$ cd steampipe-mod-aws-compliance

$ steampipe check all
```

That's it. It runs more than hundreds of benchmark suites in your service, and you definitely see a lot of **red** messages in the console :).