---
layout: post
blog: true
title: "Security Group on VPC"
date: 2015-01-28 23:04:17 +0900
comments: true
categories: ["EC2", "VPC"]
author: Kai Sasaki
---

When you create SecurityGroup on AWS, there is a point you have to care. Security group can control access list
listed as IP addresses. These values are retained as `Inbound` and `Outbound` format. Inbound shows that this security group
can receive package from described IP addresses. Outbound is the contrary.

<div style="text-align:center">
<img src="/images/posts/2015-01-28-ec2-security-group/dashboard.png" />
</div>

<!-- more -->

So if you missed the configuration of security groups, you cannot access your instances from the internet. And I found that this fact can be also applied to VPC environment.
If your instances are launched inside VPC, you have to permit these internal IP addresses with security group. I misunderstood
that. VPC access are always permitted because these instances are in the same network. So I wrote down today this fact for reminding myself whenever I launch EC2 instances with my own security groups.
