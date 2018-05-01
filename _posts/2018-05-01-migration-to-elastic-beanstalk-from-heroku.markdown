---
title: "Migration to Elastic Beanstalk from Heroku"
layout: post
date: 2018-05-01 21:22:19 +0900
image: 'images/'
description:
tag: ["Rails", "AWS", "Heroku"]
blog: true
author: "lewuathe"
---

Though I had to migrate [our Rails application](https://www.buffett-code.com/) infrastructure, it took time to migrate my Rails application to Elastic Beanstalk from Heroku than expected. [Amazon Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) and [Heroku](http://heroku.com/) are very similar PaaS service. Initially, I thought I could launch my Rails application without rewriting any code because Elastic Beanstalk supports Puma application server. But that's not true. there is one thing we need to take care of for migrating to Elastic Beanstalk.

Elastic Beanstalk uses Nginx as a web server that back-forwarding request to following application server on Puma. This Nginx uses Unix domain socket as default to connect to backend application server. So we cannot use HTTPS in this case. 

On the other hand, our Rails application running with HTTPS request was enabled `force_ssl` configuration. It tries to redirect the request to HTTPS protocol if possible. But Nginx always tries to connect to a backend server with Unix domain socket. Then redirect loop happens. 

So even if you want to enable HTTPS for your Rails application, you should disable `force_ssl`. Instead, you can make sure HTTPS by changing Nginx configuration to redirect normal HTTP request to HTTPS protocol. That is a natural way to launch Rails application with Elastic Beanstalk, I think. 

