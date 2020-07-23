---
title: "Simple ETL running on Docker and ECS"
layout: post
date: 2019-01-21 14:42:46 +0900
image: 'assets/img/posts/2019-01-21-simple-etl-running-on-docker-and-ecs/catch.jpg'
description:
tag: ["ETL", "Docker", "ECS", "AWS", "Workflow", "Container"]
blog: true
author: "Kai Sasaki"
---

Running [**ETL**](https://en.wikipedia.org/wiki/Extract,_transform,_load) is often troublesome. We need to prepare the infrastructure to run the workflow which is scalable and extensible for the future use cases as we do when creating web applications or mobile applications.
As is often the case with the custom ETL workload, it's hard to simply decouple the ETL application and infrastructure where the workflow runs on. Even if we just want to run an amazingly simple shell script, 
we need to launch a server, install all dependencies and credentials on that and set up the configurations such as crontabs if you want to run the workflow regularly. It's possibly a huge overhead if you just want to run the small ETLs. Of course, we have a bunch of tools and frameworks to run the scalable and reliable ETLs but they are sometimes overkilling to me. 

I found **[ECS](https://aws.amazon.com/ecs/)** is a nice service to run such kind of micro ETL workflow as quickly as possible and sufficiently reliable for the simple use cases. This is the article introducing an example how to use ECS as simple ETL engine.

# What is ECS?

ECS is a container orchestration service provided by AWS. [Kubernetes](https://kubernetes.io/) is the most famous one as a container orchestration framework though. Actually, AWS also provides hosted Kubernetes called EKS. But ECS has a longer history and is basically provided in every region of AWS so that it can still be the platform to be considered to run your Docker container. In my experience, ECS is pretty straightforward to the people who does not have so much experience about Kubernetes. 

# Preparing Docker Image

ECS has its own image repository, [**ECR**](https://aws.amazon.com/ecr/). Of course, you can fetch the image from public Docker registry like [Docker Hub](https://hub.docker.com/) but using ECS may be better at the beginning because images
will be private as default. If you want to make the image public, you can do it later. 

The docker image you may want to run this time can look like this. 

```Dockerfile
#
# Docker image for running ETL container named lewuathe/myetl
#
FROM lewuathe/myetl-base
ENTRYPOINT ["/bin/bash", "/opt/myetl/bin/launch.sh"]
```

`myetl-base` is the base image including all prerequisites to run the ETL job and configuration. You can override the `ENTRYPOINT` in ECS so it is used to launch the container in your local machine. It's a minimum commands to run the ETL job.
`launch.sh` can take arguments from the docker command. `docker run` command passes these arguments to the script specified by `ENTRYPOINT`.

```bash
$ docker run lewuathe/myetl -v arg1 arg2
```

will be same as 

```bash
/bin/bash /opt/myetl/bin/launch.sh -v arg1 arg2
```

In order to upload the image to your ECS repository, it's necessary to log in with AWS account. `ecr get-login` command will do everything on behalf of you.

```bash
$ $(aws ecr get-login --no-include-email --region ap-northeast-1)
$ docker build -t lewuathe/myetl .
$ docker tag lewuathe/myetl:latest <Your Docker Registry>/myetl:latest
$ docker push <Your Docker Regitry>/:latest
```

You can check the actual command by referring `View push commands` displayed in the repository page in the AWS console.

![Push commands](/assets/img/posts/2019-01-21-simple-etl-running-on-docker-and-ecs/push-commands.png)

# Create Task Definition

A task is a unit of the job running on an ECS cluster. Task definition decides the structure and resources available for running the job. What we need to specify in the task definition are listed as follows.

- Name
- Task IAM Role
- Network Mode
- Task Size (Memory and CPU)
- Container Definitions

![Docker Image](/assets/img/posts/2019-01-21-simple-etl-running-on-docker-and-ecs/image.png)

Since we can attach any IAM role to the task definition, we can control what the task can do against the AWS resources. That indicates container running in ECS can easily access to the AWS resource just by attaching proper IAM role. 

We need to make sure the resources allocated for the task is lower than the available resource in the instance. For example, an instance with [1 CPU core has 1024 CPU units](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html). Tasks running in the instance cannot be allocated more than 1024 CPU units. Moreover, there is some resource that should be allocated to the system side. A task cannot use 1024 units anyway. In this case, we allocate 512 CPU unit to the task. You can run multiple Docker containers in one task. Such a case, you also need to specify the allocated resources respectively by image.

![Docker ENTRYPOINT](/assets/img/posts/2019-01-21-simple-etl-running-on-docker-and-ecs/entrypoint.png)

By rewriting `Entry point` configuration, you can change the command running in the container. It's also overridden at runtime which means you can change the running command when you run the task. For example, you can create a task definition without `Entry point`. At runtime, you will be able to pass the following `ENTRYPOINT` to the task definition. This task will process the data generated in 2018 specified from `2018-01-01` to `2019-01-01`.

```
/bin/bash,/opt/myetl/bin/launch.sh,2018-01-01,2019-01-01
```

If you want to process the data in 2019, just changing the entry point is sufficient so that we can reuse the same task definition. 

# Scheduled ETL

Scheduled ETL can be used as a regular batch job to process the while data generated in a day or month or year. In order to do that, we need to run the task regularly. 
How can we do that with ECS? 

We can set the scheduled job in each ECS cluster. By giving scheduled task settings to the cluster, the cluster will launch a container at a specific time and run the job. 

![Scheduled Job](/assets/img/posts/2019-01-21-simple-etl-running-on-docker-and-ecs/cron.png)

The good thing about it is ECS cluster automatically handles the required resource. If there are no instances belonging the cluster, the auto-scaling group of the cluster will launch instance sufficient to run the task. Although it takes some overhead time to start the task, it provides you with more efficiency and elasticity. 

# Benefit of using ECS as ETL engine

The main advantage of using ECS to run your ETL is flexibility in terms of resource management. Basically, you don't need to keep the instance in the specific state to run a task. ECS automatically launch the instance and whole codebase and configuration can be included in the container. Therefore ECS meets our requirement to run a simple ETL on a reliable infrastructure without manual configuration as much as possible. Of course, in terms of the scalability, there are many other suitable platforms to run the ETLs for Bigdata such as Hadoop. But I believe ECS is a sufficiently good platform to run our simple script as an ETL. 

If you want to learn more, <a target="_blank" href="https://www.amazon.com/gp/product/1492036730/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1492036730&linkCode=as2&tag=lewuathe-20&linkId=de2e8d0101f1d65b0ddadc0a568aa66b">Docker: Up &amp; Running: Shipping Reliable Containers in Production</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1492036730" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" /> is a good resource because it contains the practial guide to use Docker in production scale. Thus, it includes how to use Docker on ECS and Fargate. Please try to take a look.

<div style='text-align: center;'>
<a target="_blank"  href="https://www.amazon.com/gp/product/1492036730/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1492036730&linkCode=as2&tag=lewuathe-20&linkId=fecadb13ef6a7bf1a6387a5632c43fb4"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=1492036730&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=lewuathe-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1492036730" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</div>

I hope this guide would be helpful to you too. Thanks.