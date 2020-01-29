---
title: "How to install docker in Amazon Linux"
layout: post
date: 2019-09-01 15:11:55 +0900
image: 'assets/img/posts/2019-09-01-how-to-install-docker-in-amazon-linux/catch.png'
description:
tag: ["Linux", "AWS", "Docker"]
blog: true
author: "Kai Sasaki"
---

The usage of Docker is growing more and more. Our daily development tends to depend on the container platform highly. But I found AWS Linux I recently launched does not have Docker engine as default. It is a frustrating situation even I just want to use Docker in AWS environment. Here is the process to install Docker engine in your AWS Linux. That article is written mainly for avoiding my memory lost :)

FYI: The AMI I used in this experiment is `ami-0f9ae750e8274075b`. Amazon Linux 2.

# Install Docker Engine

```
$ sudo yum update -y

$ sudo yum install -y docker

$ sudo service docker start
Starting cgconfig service:                                 [  OK  ]
Starting Docker:                                           [  OK  ]
```

# Add User Group

But you need to prepend `sudo` every time you run docker command. Please don't forget to add `ec2-user` to `docker` group.

```
$ sudo usermod -a -G docker ec2-user
```

After you log in the instance again, you should be able to run docker command without any difficulty.

Thanks

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1521822808&asins=1521822808&linkId=72a88d2b077145c841575b87262a936f&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>
<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1617294764&asins=1617294764&linkId=f877edf94a3e3c61a630172ef0872d24&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>