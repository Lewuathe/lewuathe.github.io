---
title: "Protect Your Application by AWS WAF"
layout: post
date: 2019-04-27 13:24:37 +0900
image: 'assets/img/posts/2019-04-27-protect-your-application-by-aws-waf/catch.jpg'
description:
tag: ['AWS', 'Application', 'Security', 'Application']
blog: true
author: "Kai Sasaki"
---

Have you ever heard about WAF before? You may but no, it's not web application **FRAMEWORK** I'm going to talk about today. It's web application **FIREWALL**. You may have a time when you struggle to deal with many accesses from scrapers or attackers to your web application. These requests look normal but a loaf of requests that keeps coming can behave like DoS attack. It can degrade the performance of your application and moreover, it can worsen user experience too. Actually, we had this sort of challenge to provide a web application [Buffett Code](https://www.buffett-code.com/) which provides valuable information for investment and corporate analysis. Due to the nature of the application providing numbers of investment information, the web application can receive many requests from bots or some machinery programs. We looked for several solutions to protect the application from this kind of scraping behavior. [AWS WAF](https://aws.amazon.com/waf/) may be a solution easily integrated into your application running in AWS resource.

# What is AWS WAF?

AWS WAF is a web application firewall to protect your application against scaping or DoS attacks. It can be easily integrated with your application running on AWS. WAF is provided with CloudFront (global) of regional application load balancers.

[![waf](assets/img/posts/2019-04-27-protect-your-application-by-aws-waf/waf.png)](https://aws.amazon.com/waf/)

You can configure WAF based on the following characteristics of the traffic.

* Geo Match
* IP Address
* Cross-Site Scripting
* Size Constraints
* SQL Injection
* String and Regex Matching

The benefit of using WAF is it can automatically detect the characteristics like SQL injection or cross-site scripting because it is troublesome if we need to protect our application against that sort of attacks manually. Let's see how we can set the blacklist of a user agent which should be blocked.

# User Agent Matching

You can put any user agent header to be blocked by using this feature. AWS WAF provides various kind of utilities to get things done easier. `Transformation` enables us to preprocess the header of an incoming request before applying the matching condition.

![User agent matching](assets/img/posts/2019-04-27-protect-your-application-by-aws-waf/user-agent.png)

By using the transformation of `Convert to lowercase`, we can simply put blocking user agent in the lower case without caring about the case sensitivity. Of course, you can configure not only HTTP header but also query string, HTTP method, URI.

# Dashboard

Another good thing of AWS WAF is dashboard to see how many requests are blocked at a glance.

![dashboard](assets/img/posts/2019-04-27-protect-your-application-by-aws-waf/dashboard.png)

As AWS WAF automatically keeps logs of blocked request including IP, header and query string so that we can check the configuration of WAF is effective or not. It's also helpful to detect the time when the abusive request tends to come to our application. We may be able to do auto scaling not to degrade the performance of the application around the time.

# Recap

So overall we can get a huge benefit by using AWS WAF. Since our application is running behind the application load balancer, it was so easy to integrate with our application. The easiness and flexibility of AWS WAF let us focus on developing the core value of our application.

Unfortunately there is not so many resources to learn AWS WAF technical details. As it is often the case, the official documentation (<a target="_blank" href="https://www.amazon.com/gp/product/B07641Q364/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B07641Q364&linkCode=as2&tag=lewuathe-20&linkId=e8faffc5200ffedd941c9958174207c6">AWS WAF, AWS Firewall Manager, and AWS Shield Advanced: Developer Guide</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=B07641Q364" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />) is the best one to get started this beneficial framework. It's free!

<p style='text-align: center'>
<a target="_blank"  href="https://www.amazon.com/gp/product/B07641Q364/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B07641Q364&linkCode=as2&tag=lewuathe-20&linkId=e4b9b61a71ae791ebcd144402f3cbbb8"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=B07641Q364&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=lewuathe-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=B07641Q364" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</p>

Thanks!