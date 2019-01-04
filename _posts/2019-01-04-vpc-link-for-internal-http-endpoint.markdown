---
title: "VPC Link for internal HTTP endpoint"
layout: post
date: 2019-01-04 19:31:00 +0900
image: 'assets/img/posts/2019-01-04-vpc-link-for-internal-http-endpoint/catch.png'
description:
tag: ["AWS", "VPC", "API Gateway", "HTTP", "Network"]
blog: true
author: "Kai Sasaki"
---

API Gateway in AWS initially only supports HTTP endpoint exposed to the public internet. We had to use AWS Lambda to access the endpoint behind the private VPC. 

[Since the end of 2017, we can connect API Gateway and internal HTTP endpoint by using VPC Link directly](https://aws.amazon.com/about-aws/whats-new/2017/11/amazon-api-gateway-supports-endpoint-integrations-with-private-vpcs/). 
We tried to use VPC link to make sure our HTTP endpoint hosted by Elastic Beanstalk only accessible via API Gateway. 

1. Create Elastic Beanstalk with NLB
2. Specify VPC type in request integration
3. Deploy API Gateway to the target stage
4. Specify stage variables

# Create Elastic Beanstalk with NLB

First, we need to create our Elastic Beanstalk application with the network load balancer. As VPC link only supports routing to the network load balancer, an application load balancer (ALB) and classic load balancer cannot be used. You can create NLB via AWS console without any difficulties. [Here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-nlb.html) is the instruction.

# Specify VPC type integration

In the configuration of integration request, it is necessary to specify **VPC Link** type. You can do that in AWS console as follows.

![VPC Link type](assets/img/posts/2019-01-04-vpc-link-for-internal-http-endpoint/vpclink.png)

It's also necessary to specify VPC link ID and endpoint as stage variables if you want to use different upstream endpoint by stages. All stage variables are stored in the parent object `stageVariables`. So your variable should be referred here such as `${stageVariables.vpcLinkId}`.

# Deploy API Gateway to the target stage

Then we can deploy the API Gateway implementation so that it can be visible from the public internet. 

![deploy](assets/img/posts/2019-01-04-vpc-link-for-internal-http-endpoint/deploy.png)

The root path of the deployed endpoint will be the stage name. For example, if you deploy an API to the stage `development`, the URL visible from the public internet will be `https://<API Gateway ID>.execute-api.<Region>.amazonaws.com/development/path/to/resource`.

# Set stage variable

We need to specify the stage variables that are defined in step 2. This console is shown when you click the stage name in the `Stages` tab.

![variable](assets/img/posts/2019-01-04-vpc-link-for-internal-http-endpoint/variable.png)

In this case, we need to define both `vpcLinkId` and `url` variables. 

Then your internal endpoint will be accessible from the public internet. One big advantage is that it enables us to limit the all possible connection through API Gateway. We can have access control and resource quota in API Gateway without modifying the application code. It makes life significantly easy. 

