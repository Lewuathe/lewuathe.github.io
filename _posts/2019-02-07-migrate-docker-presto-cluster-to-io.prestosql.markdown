---
title: "Migrate docker-presto-cluster to io.prestosql"
layout: post
date: 2019-02-07 19:14:26 +0900
image: 'assets/img/posts/2019-02-07-migrate-docker-presto-cluster-to-io/catch.png'
description:
tag: ['Presto', 'Docker']
blog: true
author: "Kai Sasaki"
---

At the beginning of this month, new **Presto Software Foundation** was launched. This foundation was created for ensuring the openness of Presto as open source software.

<div style='text-align: center;'>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">We are pleased to announce the launch of the Presto Software Foundation, a not-for-profit organization dedicated to the advancement of the Presto open source distributed SQL engine. We&#39;ll be announcing soon about the first community meeting.<a href="https://t.co/QnOldnXlT5">https://t.co/QnOldnXlT5</a></p>&mdash; Presto (@prestosql) <a href="https://twitter.com/prestosql/status/1091016345800658945?ref_src=twsrc%5Etfw">January 31, 2019</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>


Since the source code was forked from the original repository [prestodb/prestodb](https://github.com/prestodb/presto) to **[prestosql/presto](https://github.com/prestosql/presto)**. And there are already several released published after the fork. The latest version is [302](https://twitter.com/prestosql/status/1093368972576092160).

I decided to migrate [docker-presto-cluster](https://github.com/Lewuathe/docker-presto-cluster) to new Presto. The latest version published in [DockerHub](https://hub.docker.com/).

|image|url|
|:---|:---|
|presto-coordinator|[lewuathe/presto-coordinator](https://cloud.docker.com/u/lewuathe/repository/docker/lewuathe/presto-coordinator)|
|presto-worker|[lewuathe/presto-worker](https://cloud.docker.com/u/lewuathe/repository/docker/lewuathe/presto-worker)|

The easiest way to use these images are [docker-compose](https://docs.docker.com/compose/). Please take a look into the previous post for more detail.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://www.lewuathe.com/launch-distributed-system-with-docker-compose.html" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fwww.lewuathe.com%2Flaunch-distributed-system-with-docker-compose.html&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

This is the example of [`docker-compose.yml`](https://github.com/Lewuathe/docker-presto-cluster/blob/master/docker-compose.yml) file.

```
version: '3'

services:
  coordinator:
    build: 
      context: ./presto-coordinator
      args:
        node_id: coordinator
    ports:
      - "8080:8080"
    container_name: "coordinator"

  worker0:
    build: 
      context: ./presto-worker
      args:
        node_id: worker0
    container_name: "worker0"
    ports:
      - "8081:8081"
  worker1:
    build: 
      context: ./presto-worker
      args:
        node_id: worker1
    container_name: "worker1"
    ports:
      - "8082:8081"
```

Of course, you may want to submit queries to the cluster. I hope this article would be helpful for that purpose. This describes how to use client tool to run queries in Presto cluster running by docker-compose.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://www.lewuathe.com/accessing-presto-cluster-on-docker.html" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fwww.lewuathe.com%2Faccessing-presto-cluster-on-docker.html&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>


Please let me know anytime if you find anything wrong with the framework. Thanks!
