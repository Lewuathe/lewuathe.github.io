---
title: "Embed docker image in CodeDeploy package"
layout: post
date: 2019-01-05 13:35:59 +0900
image: 'assets/img/posts/2019-01-05-embed-docker-image-in-codedeploy-package/catch.jpg'
description:
tag: ['Docker', 'CodeDeploy', 'AWS', 'Container', 'Cloud']
blog: true
author: "Kai Sasaki"
---

Deploying your application as docker image is not uncommon nowadays. You may usually use ECS or Kubernetes (EKS) to deploy the docker image to the environment in cloud service such as AWS. But do you know there is another simple way to run your Docker container in AWS environment? Yes, CodeDeploy.

# What is CodeDeploy?

AWS CodeDeploy is a service to provide us general deployment mechanism available for EC2 instances, on-premise instances, serverless lambda functions. The package used by CodeDeploy is a simple zip archive including all resources and binaries to run the application. Application lifecycle is managed by CodeDeploy. CodeDeploy system can start and stop the application on behalf of us. You can deploy any kind of applications with it, of course including docker container.

# How to include docker image in CodeDeploy package?

Docker image can be serialized by [`save`](https://docs.docker.com/engine/reference/commandline/save/) command as a tar archive format so that we can keep docker image as a simple archive file as follows.

```
$ docker save lewuathe/my-app | gzip -c > my-app-docker.tar.gz
```

Once it is converted into the tar archive format, we can easily let the CodeDeploy package contain it.

```
$    aws deploy push \
          --region us-east-1 \
          --output json \
          --application-name my-app \
          --description "My application running in docker contaienr in AWS CodeDeploy" \
          --s3-location "$(CODEDEPLOY_BUCKET)/my-app.zip" \
          --source "."
```

This command will create a CodeDeploy package based on the current directory specified by `--source` option. That contains `my-app-docker.tar.gz`. This command will also upload the package to the S3 bucket specified by `--s3-location`. 

It's necessary to load the docker image in the docker engine running in the EC2 instance where the package is deployed.
You can use [`load`](https://docs.docker.com/engine/reference/commandline/load/) command. It will be useful to write this command in a hook script triggered in [ApplicationStart lifecycle](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html). 

```
$ docker load -i /path/to/package/my-app-docker.tar.gz
```

You can see the image with `docker images`.

```
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
lewuathe/my-app     latest              6fc6e4e7a8ee        6 days ago          872MB
```

Since docker image can be easily converted into the portable format, deploying a docker image in CodeDeploy package probably the easiest way. The good news is that it is sufficiently stable as a way to deploy your docker application in AWS environment. We already run that kind of application in our production system because CodeDeploy is working not only EC2 instances but also our on-premise instances existing in other cloud services. So it's also portable in terms of cross-cloud environment. If you want to use another cloud service, it must not be so difficult to do so. Please try it.

Thanks.



The photo in the top is taken by <a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@frankiefoto?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from frank mckenna"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">frank mckenna</span></a>
