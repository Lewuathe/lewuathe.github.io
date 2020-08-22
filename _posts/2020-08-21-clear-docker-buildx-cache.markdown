---
title: "Clear Docker Buildx Cache"
layout: post
date: 2020-08-21 13:11:31 +0900
image: 'assets/img/posts/2020-08-21-clear-docker-buildkit-cache/catch.jpg'
description:
tag: ['Docker', 'Presto', 'Java']
blog: true
author: "Kai Sasaki"
---

You might have encountered a situation where you cannot build the latest Docker image when using the [Buildx](https://docs.docker.com/buildx/working-with-buildx/). If so, you may find this article helpful to give you a little insight into your question, *"Why I keep seeing the stale image in the list!"*.

What I tried was building [the Docker image supporting ARM64 architecture](https://github.com/Lewuathe/docker-presto-cluster/commit/bcdaf191829754d93876c1e4d44cb33019bd75ad). To achieve my goal, it requires me to enable Buildx experimental feature of Docker. It allows us to build a Docker image supporting multiple architectures. When I have found a problem in the image, I wanted to change the Dockerfile to reflect the fix I applied. But it failed. As shown in the following output, the `CREATED` time of the images keeps the past time even I have created just a few seconds before.

```
$ docker images
REPOSITORY                                                    TAG                      IMAGE ID            CREATED             SIZE
presto                                                        341-SNAPSHOT             c15822305160        5 hours ago         1.05GB
lewuathe/presto-worker                                        341-SNAPSHOT             eb1d11521b04        5 hours ago         1.38GB
lewuathe/presto-coordinator                                   341-SNAPSHOT             8e0085374165        5 hours ago         1.38GB
```

That's was so annoying that I could not test my fix was adequately resolving the issue. Here are two options to overcome this stressful situation.

## Build without any cache

As well as normal build command, `buildx` also provides [`--no-cache`](https://thenewstack.io/understanding-the-docker-cache-for-faster-builds/#:~:text=When%20the%20'%E2%80%93no%2Dcache,the%20maximum%20amount%20of%20time.) option. It enables us to build an image from scratch. The latest image will be created for sure.

```sh
$ docker buildx build \
    --no-cache \ # Without using cache
    --platform linux/arm64/v8 \
    -f Dockerfile-arm64v8 \
    -t lewuathe/prestobase:340-SNAPSHOT-arm64v8
```

## Clearing the cache completely

Another option is clearing the cache. However, it has a side-effect affecting other image build time. Since removing all layer caches, it can make the build time for other images longer. But if the images you are holding is not so many, deleting the cache can be a reasonable option.

The builder instance holds the cache. The following command will clear the cache hold by all builders.

```sh
$ docker builder prune --all
```

Afterward, you can build the image as usual. We can see the build time is refreshed as follows.


```
$ docker images
REPOSITORY                                                    TAG                      IMAGE ID            CREATED             SIZE
presto                                                        341-SNAPSHOT             c15822305160        a second ago        1.05GB
lewuathe/presto-worker                                        341-SNAPSHOT             eb1d11521b04        a second ago        1.38GB
lewuathe/presto-coordinator                                   341-SNAPSHOT             8e0085374165        a second ago        1.38GB
```

To learn the practical techniques of Docker, you may find [the following guide from Manning](https://www.amazon.com/gp/product/1617294802/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=lewuathe-20&creative=9325&linkCode=as2&creativeASIN=1617294802&linkId=9e74c652a72e58e3287c30b704effbde) useful. Docker has many options or configurations. If you know these details, Docker will be more attentive tool for you.

<div style='text-align: center;'>
<a target="_blank"  href="https://www.amazon.com/gp/product/1617294802/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1617294802&linkCode=as2&tag=lewuathe-20&linkId=4e8ef0281e7a4fb958f91ce8f10e706c"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=1617294802&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=lewuathe-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1617294802" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</div>

Thanks for reading as usual!

## References
- [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
- [Docker In Practice](https://www.amazon.com/gp/product/1617294802/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=lewuathe-20&creative=9325&linkCode=as2&creativeASIN=1617294802&linkId=9e74c652a72e58e3287c30b704effbde)