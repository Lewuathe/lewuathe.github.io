---
title: "True Cause behind Additional Verification in ACM"
layout: post
date: 2021-07-21 20:36:01 +0900
image: 'assets/img/posts/2021-07-21-true-cause-behind-additional-verification-in-acm/catch.jpg'
description:
tag: ['AWS', 'SSL', 'Web']
blog: true
author: "Kai Sasaki"
---

[AWS Certificate Manager](https://docs.aws.amazon.com/acm/) (ACM) is a service allowing us to manage the complexity around SSL/TLS certificates such as creating, storing, and renewing. ACM handles almost all operational complexity on our behalf to concentrate on the essential application development. That is a massive benefit of using the service if you want to provide a safe web service using SSL/TLS. (Of course, all websites should use SSL/TLS as default)

The other day, I encountered a situation where ACM showed up the error message like:

> Request failed
> The status of this certificate request is "Failed". Additional verification is required to request certificates for one or more domain names in this request.

The certificate request failed. What's that? I usually pass the verification process without any trouble. So what do I need to do to deal with the *additional verification process*?

[The forum](https://forums.aws.amazon.com/thread.jspa?threadID=299418) gave me a clear answer.

> Usually, this error appears when an ACM certificate request contains a domain listed under the Alexa Top 1000 domains. This process is in place to prevent abuse.

Indeed, the target domain I have requested the certificate for is listed in the top 1000 in [the Alex ranking](https://www.alexa.com/siteinfo) at the time. :) Therefore, we rarely see such a situation unless you have an extensive popular domain in the world.

The only way to resolve the issue is to file a support ticket to ask AWS to put our domain in the whitelist. That seems to work as the *additional verification* in this case. AWS support team will promptly respond to your problem, and your certificate will be issued once the ticket is closed.

# Reference

- [Request failed while creating a certificate](https://forums.aws.amazon.com/thread.jspa?threadID=299418)
