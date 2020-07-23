---
title: "Building aarch64 image with Docker"
layout: post
date: 2020-01-27 09:48:13 +0900
image: 'assets/img/posts/2020-01-27-building-aarch64-image-with-docker/catch.jpg'
description:
tag: ['Docker', 'macOS', 'Arm']
blog: true
author: "Kai Sasaki"
---

Most of us may use x86 architecture to run your application usually. x86 machine is a dominant architecture in the data center and desktop application. Of course, this blog is also written in the MacBook Pro running on [Intel Core i7](https://en.wikipedia.org/wiki/List_of_Intel_Core_i7_microprocessors). But you may want to run your application on the machine running with different CPU architecture from time to time. Most mobile devices support Arm architecture. Additionally, cloud service providers such as [AWS](https://aws.amazon.com/about-aws/whats-new/2019/12/announcing-new-amazon-ec2-m6g-c6g-and-r6g-instances-powered-by-next-generation-arm-based-aws-graviton2-processors/) provide new generation machine running in Arm-based processor. It is not strange even if we want to run our application on a different platform seeking a chance of better performance or stability.

Nowadays, Docker is the first option to run our application quickly bundled with necessary prerequisites. Using Docker is a sound idea to apply the new platform to the existing app.

[To experiment Presto run Graviton processor](https://prestosql.io/blog/2019/12/23/Presto-Experiment-with-Graivton-Processor.html), I have tried to create a Docker image supporting Arm platform. Here is an article briefly describing how to create a Docker image supporting Arm.

# Docker Buildx

[Docker buildx](https://docs.docker.com/buildx/working-with-buildx/) is an experimental feature for the full support of [Moby BuildKit toolkit](https://github.com/moby/buildkit). It enables us to build a Docker image supporting multiple platforms, including Arm. The feature is so useful that we can quickly make the cross-platform Docker image with a one-line command. But the feature is not generally available in the typical installation of Docker. Enabling the experimental flag is necessary as follows in the case of macOS.

![experimental](/assets/img/posts/2020-01-27-building-aarch64-image-with-docker/docker-daemon.png)

And make sure to restart the Docker daemon.

# Command Line

We can build the Docker image for Presto supporting aarch64 architecture with buildx command. We can specify the target platform with `--platform` option as follows.

```
$ docker buildx build \
 --platform linux/arm64
 --push
 .
```

`--push` option lets us upload the image without issuing another command to do so.

![target platform](/assets/img/posts/2020-01-27-building-aarch64-image-with-docker/platform.png)

We will find the image supporting the target platform uploaded in the Docker Hub. The good thing is that the Docker engine automatically checks the target platform validity by using that information. It is helpful to search and run the image supporting our desired platform.

Thanks!

Image by <a href="https://pixabay.com/users/blickpixel-52945/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=447483">Michael Schwarzenberger</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=447483">Pixabay</a>
