---
title: "How to install docker in Amazon Linux"
layout: post
date: 2019-09-01 15:11:55 +0900
image: 'assets/img/posts/2019-09-01-how-to-install-docker-in-amazon-linux/catch.png'
description:
tag: ["Linux", "AWS", "Docker"]
blog: true
author: "Kai Sasaki"
---

The usage of Docker is growing more and more. Our daily development tends to depend on the container platform highly. But I found AWS Linux I recently launched does not have Docker engine as default. It is a frustrating situation even I just want to use Docker in AWS environment. Here is the process to install Docker engine in your AWS Linux. That article is written mainly for avoiding my memory lost :)

FYI: The AMI I used in this experiment is `ami-0f9ae750e8274075b`. Amazon Linux 2.

# Install Docker Engine

```
$ sudo yum update -y

$ sudo yum install -y docker

$ sudo service docker start
Starting cgconfig service:                                 [  OK  ]
Starting Docker:                                           [  OK  ]
```

# Add User Group

But you need to prepend `sudo` every time you run docker command. Please don't forget to add `ec2-user` to `docker` group.

```
$ sudo usermod -a -G docker ec2-user
```

After you log in the instance again, you should be able to run docker command without any difficulty.

Thanks