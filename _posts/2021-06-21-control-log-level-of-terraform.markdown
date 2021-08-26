---
title: "Control Log Level of Terraform"
layout: post
date: 2021-06-26 09:50:45 +0900
image: 'assets/img/posts/2021-06-21-control-log-level-of-terraform/catch.jpg'
description:
tag: ['Terraform', 'Log', 'Cloud']
blog: true
author: "Kai Sasaki"
---

[Terraform in the cloud](https://app.terraform.io) writes the stderr log in the console so that we can quickly discover what resources are created, changed, and destroyed. However, it may sometimes be too lengthy to grasp the complete information quickly. As we do for the typical long-running application, it is necessary to control the log level to suppress the output of unessential descriptions.

[`TF_LOG`](https://www.terraform.io/docs/internals/debugging.html) environment variable is the way to control what type of information is written to the stderr.

![Variables](/assets/img/posts/2021-06-21-control-log-level-of-terraform/variables.png)

This variable is, of course, usable in the local Terraform. Additionally, we can make the environment variable effective by setting that in the *variables* pane in the dashboard of Terraform cloud.

It simplifies the process of looking into the log written by Terraform for you.


# Reference

- [Debugging in Terraform](https://www.terraform.io/docs/internals/debugging.html)
- [Variables](https://www.terraform.io/docs/cloud/workspaces/variables.html)