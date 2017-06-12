---
title: "Machine Learning on ECS"
layout: post
date: 2017-06-06 12:42:14 +0900
image: 'images/'
description:
tag: ["docker", "ECS", "Python", "Machine Learning"]
blog: true
author: "lewuathe"
---

On the other day, I had a chance to try [ECS](https://aws.amazon.com/ecs/) (Amazon EC2 Container Service). ECS is a container management service
provides by AWS. Though I heard about it and thought it must be useful, there were some points to be cared as usual.
This is the note for the ECS users and of course for me.

## What we did

I tried to run machine learning algorithm on ECS.

* [Lewuathe/docker-td-xgboost](https://github.com/Lewuathe/docker-td-xgboost/)
* [takuti/docker-td-sklearn](https://github.com/takuti/docker-td-sklearn/)

They are the docker image containing machine learning libraries we used. We tried to run the container image on ECS through command line.

## ECR Register

ECS uses its own Docker registry called [ECR](https://aws.amazon.com/ecr/). You need to register your account from local machine in order to push Docker image to ECR.

```
$ aws ecr get-login --region $AWS_REGION
```

Run the docker login command that was returned in the previous step. Then build your first image.

```
$ docker build -t myimage:latest .
```

Tagging.

```
$ docker tag myimage:latest $YOUR_ECR_URI/myimage:latest
```

Then push to ECR.

```
$ docker push $YOUR_ECR_URI/myimage:latest
```

## ECS Cluster

Then we have to construct ECS cluster. The configuration is simple but there are some points to be noted.

| Config Name | Note |
|:----|:----|
|Cluster Name | As you like |
|EC2 Instance Type | As you like |
|Number of instances | As you like |
|Key pair| If you want to login to debug, need to specify|
|Networking| Basically no need to do manual configuration|
|Container instance IAM role|Create IAM role which has `AmazonEC2ContainerServiceforEC2Role` in advance. If you want to keep debug logs please also attach `CloudWatchLogsFullAccess`.|

## Create task definition

Containers are run as task on ECS. Tasks are created by task definition.

|Task Definition Config| Note |
|:----|:----|
|Task Definition Name| As you like|
|Task Role| Need to create role attached proper policy for doing your desired tasks. For example, if a container needs to access S3, it is necessary to give `AmazonS3FullAccess` policy.
|Network Mode|`Bridge` is enough|
|Container definition|As you like. But one thing to be noted is entry point definition. It should be written in *comma separated format*. (e.g. `python,script.py,arg1,arg2`). So we cannot use the arguments including **comma**!
|Log Configuration|If you created Log Group in CloudWatch, your task can send stdout to CloudWatch. Please set `awslogs` for log driver and corresponding configurations. (e.g. awslogs-group, awslogs-region are required)

## Run task

There are two ways to run task on ECS.

* Run task from AWS console.
* AWS CLI

### AWS Console

Click task definition -> Run Task

![Run Task](images/posts/2017-06-06-machine-learning-on-ecs/run-task.png)

You can override role, command arguments and environment variables etc.

### AWS CLI

```
$ aws ecs run-task \
    --cluster=$YOUR_CLUSTER_NAME \
    --task-definition=$TASK_NAME:$TASK_REVISION \
    --overrides '{"containerOverrides":[{"name":$CONTAINER_NAME,"command":["python","script.py","arg1","arg2"]}]}'
```

If you will integrate ECS with other system or workflow, AWS CLI is appropriate way.
