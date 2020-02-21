---
title: "Launch Your Own Presto Cluster with Terraform"
layout: post
date: 2020-02-19 16:22:06 +0900
image: 'assets/img/posts/2020-02-19-launch-your-own-presto-cluster-with-terraform/catch.png'
description:
tag: ['Presto', 'Terraform', 'AWS']
blog: true
author: "Kai Sasaki"
---

Launching a distributed system is not an easy task, unlike the simple command-line tools or desktop application. It takes time to install software and prepare the server instances. There are many automation tools to make it easy to launch a complicated system in public cloud services like AWS. [Terraform](https://www.terraform.io/) is a tool to enable us to achieve infrastructure as a code on the major cloud services. It accelerates not only the process to provision production servers but also the validation of new features or bug fixes you have created.

I have used [docker-presto-cluster](https://github.com/Lewuathe/docker-presto-cluster) for testing purposes. But it is necessary to launch multiple node cluster under the environment close to more real cases. I have found Terraform is capable of provisioning the Presto cluster in AWS quickly. This post will introduce [new module](https://github.com/Lewuathe/terraform-aws-presto) I have created to provision out-of-the-box Presto cluster in AWS environment.

# [terraform-aws-presto](https://github.com/Lewuathe/terraform-aws-presto)

terraform-aws-presto is a module to create all resources to launch a Presto cluster in the AWS environment. It uses Docker images to build and distributed by myself and [AWS Fargate](https://aws.amazon.com/fargate/) to start a cluster in the ECS environment.

All resources created by the module are illustrated as follows.

![overview](https://raw.githubusercontent.com/Lewuathe/terraform-aws-presto/master/overview.png)

* VPC
  * Public Subnet
  * Private Subnet
  * Application Load Balancer (ALB)
* ECS Cluster
  * Task Definition
  * ECS Service

It creates a public subnet and private subnet inside the specific VPC. The default CIDR block of VPS is `10.0.0.0/16`.  ALB connecting to the coordinator is located in public subnet so that anyone can submit a query to the cluster. All services of Presto (coordinator and worker) are running inside the private subnet. No one can access Presto instances directly.

There are two task definitions in ECS service. One is for the coordinator, and the other is for workers. You can control the number of worker instances by using the [Terraform variable](https://registry.terraform.io/modules/Lewuathe/presto/aws/0.0.2?tab=inputs).

# Usage

For example, this is the minimum code to launch a Presto cluster with two worker instances in the default VPC.

```terraform
module "presto" {
  source           = "github.com/Lewuathe/terraform-aws-presto"
  cluster_capacity = 2
}

output "alb_dns_name" {
  value = module.presto.alb_dns_name
}
```

As the module returns the coordinator DNS name, you can get access to the coordinator through ALB.

```bash
$ ./presto-cli --server http://presto-XXXX.us-east-1.elb.amazonaws.com \
    --catalog tpch \
    --schema tiny
```

The module downloads the Docker images distributed in [lewuathe/presto-coordinator](https://hub.docker.com/repository/docker/lewuathe/presto-coordinator) and [lewuathe/presto-worker](https://hub.docker.com/repository/docker/lewuathe/presto-worker). You can control the version of Presto installed in the cluster by changing the `presto_version` input variable.

To create the module, **"<a target="_blank" href="https://www.amazon.com/gp/product/1491977086/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1491977086&linkCode=as2&tag=lewuathe-20&linkId=48dee172fed864b958f90ba209d790a1">Terraform: Up and Running: Writing Infrastructure as Code</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1491977086" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"** was a good reference to learn how Terraform works in general. Take a look if you are interested in Terraform module.

<p style='text-align: center;'>
<a target="_blank"  href="https://www.amazon.com/gp/product/1491977086/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1491977086&linkCode=as2&tag=lewuathe-20&linkId=cbdf4d30c6108c9e8a0b06cd11e6bd68"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=1491977086&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=lewuathe-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1491977086" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</p>

As far as I tried, the module will launch a Presto cluster in a few minutes because it's minimal and straightforward. You may find something insufficient or not useful. Please give me any feedback or pull requests if you have any requests.

Thanks as usual.

# Reference

* [Lewuathe/terraform-aws-presto](https://github.com/Lewuathe/terraform-aws-presto)
* [Terraform Registry: Lewuathe/aws/presto](https://registry.terraform.io/modules/Lewuathe/presto/aws)