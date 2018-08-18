---
title: "Changing the VOLUME within Dockerfile"
layout: post
date: 2018-03-08 09:21:56 +0900
image: 'mountains.jpg'
description:
tag: ['Docker', 'Container', 'Software']
blog: true
author: "lewuathe"
---

I had a trouble to use Docker `VOLUME` yesterday. This is my note to describe what the problem was and the way how to solve it. Volumes in Docker is a mechanism which enables us to generate data into host machine directory. [Volumes](https://docs.docker.com/storage/volumes/) are managed mainly by docker daemon, on the other hand [bind mounts](https://docs.docker.com/storage/bind-mounts/) is created on the user managed directory on the host machine. Official documentation says volumes have several advantages:

- Volumes are easier to back up or migrate than bind mounts.
- Volumes can be more safely shared among multiple containers.
- Volume drivers allow you to store volumes on remote hosts or cloud providers, to encrypt the contents of volumes, or to add other functionality.

[![docker volumes](https://docs.docker.com/storage/images/types-of-mounts-volume.png)](https://docs.docker.com/storage/volumes/)

But we need to pay attention to the writability when we use `VOLUME` directive in Dockerfile. Let's say we are using a Dockerfile that looks like this:

```
FROM ubuntu:16.04

VOLUME /myvol
RUN echo 'Hello World' >> /myvol/hello
```

```
$ docker build -t lewuathe/myvol .
$ docker run -it lewuathe/myvol bash
# ls /myvol
total 8
drwxr-xr-x 2 root root 4096 Mar  8 00:44 ./
drwxr-xr-x 1 root root 4096 Mar  8 00:44 ../
```

You won't be able to find the file `hello`. Why? [The official documentation](https://docs.docker.com/engine/reference/builder/#volume) says that:

> Changing the volume from within the Dockerfile: If any build steps change the data within the volume after it has been declared, those changes will be discarded.

So you cannot change the directory/file that is created by `VOLUME` from Dockerfile. Of course you can change the content from the process in runtime container after it launches. That must be the limitation of `VOLUME` in Dockerfile. 

This is one solution.

```
FROM ubuntu:16.04

RUN mkdir /myvol
RUN echo 'Hello World' >> /myvol/hello
VOLUME /myvol
```

You can write anything before creating volumes. Creating volumes at the last will enable you to do what you want. 


Thanks.

# Reference

- [Use volumes](https://docs.docker.com/storage/volumes/)
- [VOLUME in Dockerfile](https://docs.docker.com/engine/reference/builder/#volume)




