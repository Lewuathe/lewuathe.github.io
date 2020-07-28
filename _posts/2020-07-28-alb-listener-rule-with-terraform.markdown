---
title: "ALB Listener Rule with Terraform"
layout: post
date: 2020-07-28 14:17:50 +0900
image: 'assets/img/posts/2020-07-28-alb-listener-rule-with-terraform/catch.png'
description:
tag: ['Terraform', 'LoadBalancer', 'AWS']
blog: true
author: "Kai Sasaki"
---

Terraform is once of the heavily-used infrastructure tool in my daily work recently. It allows us to write the wireframe of the cloud infrastructure we use by simple configuration language called [HCL](https://github.com/hashicorp/hcl). Thanks to that, we can safely modify the underlying infrastructure and quickly track the history of the change. Therefore, I'd like to collect some knowledge about the usage of Terraform based on the actual use cases.

Today, I'm going to show you how to construct the application load balancer in AWS with Terraform. That is what I did to prepare the load balancer running in front of our service.

## Create ALB

First, we need to create the ALB itself. [`aws_lb`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb) resource will form the ALB as follows.

```terraform
locals {
  this_alb_name = "myalb"
  redirect_to   = "redirect.to"
}

resource "aws_lb" "myalb" {
  name               = "${local.this_alb_name}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["${aws_security_group.lb_sg.id}"]
  subnets            = ["${aws_subnet.public.*.id}"]

  access_logs {
    bucket  = "${aws_s3_bucket.lb_logs.bucket}"
    prefix  = "${local.this_alb_name}"
    enabled = true
  }
}
```

## Create Listener

Next, we can attach a listener to the ALB we have created. It is necessary to get the ARN of the previous ALB for [`aws_lb_listener`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener) resource. Let's use the data source for retrieving the ARN this time.

```terraform
data "aws_lb" "myalb" {
  name = "${local.this_alb_name}"
}

resource "aws_lb_listener" "mylistener" {
  load_balancer_arn = "${data.aws_lb.myalb.arn}"
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      host        = "${local.redirect_to}"
      port        = "80"
      protocol    = "HTTP"
      status_code = "HTTP_301"
    }
  }
}
```

Note that this listener has a default action. This action returns a 301 response with the redirection to the specific location by `local.redirect_to`. If no other actions are matched, the default action will be taken.

## Add Listener Rule

Lastly, you can add your custom rules as you like with [`aws_lb_listener_rule`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener_rule). We can get the ARN of the listener without using the data source if the listener is created in the same Terraform configuration.

```terraform
resource "aws_lb_listener_rule" "redirect_to_cdp_bi" {
  listener_arn = "${aws_lb_listener.mylistener.arn}"
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = "${local.this_tg.arn}"
  }

  condition {
    path_pattern {
      values = ["/forward_to/*"]
    }
  }
}
```

The final diagram can look like this.

![ALB Listener Rules](/assets/img/posts/2020-07-28-alb-listener-rule-with-terraform/alb_listener_rules.png)

All requests matching with the path `/forward_to/*` are routed to the target group `this_tg`. The others go to the host `https://redirect.to`.

The best thing about using Terraform is that we can do that in a reproducible manner. Once the Terraform configuration is written, we can get the same resource by just applying it.


## Reference

* [Hashicorp Configuration Language](https://github.com/hashicorp/hcl)
* [aws_lb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb)
* [aws_lb_listener](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener)
* [aws_lb_listener_rule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener_rule)