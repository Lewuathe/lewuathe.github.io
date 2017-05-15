---
title: "Always on SSL of GitHub Pages"
layout: post
date: 2017-05-15 14:19:00 +0900
image: 'images/'
description:
tag: ["SSL", "GitHub", "Jekyll"]
blog: true
author: "lewuathe"
---

Though I have longed for [Always on SSL](https://www.symantec.com/page.jsp?id=always-on-ssl) in this site, I hesitated to do that because it looks troublesome and cost me some money. Yesterday, I found a nice article about enabling Always on SSL on GitHub Pages.

["Move to GitHub Pages" by takuti](https://takuti.me/note/move-to-gh-pages/)

Thanks to [Cloudflare](https://www.cloudflare.com/), we can easily enable Always on SSL on our GitHub Pages for free.
The instruction was super very easy. Assuming we already have GitHub Pages repository with custom domain.

## Register you site in Cloudflare

After you created an account in Cloudflare, you should register your site.

![Add Website](images/posts/2017-05-15-always-on-ssl-of-github-pages/add-website.png)

Cloudflare automatically extract necessary information like DNS records. So please wait for a moment.

## Change name server on Route53

My registrar and name server is hosted by AWS Route53. So it was necessary to update name server configuration on Route53 next. We need to change two points in Route53.

- `NS` record of the hosted zone
- Name server of registrar

Please change the `NS` record of your hosted zone and don't forget the name server of registrar. I forgot that:).
Click the `Registered domains` and `Add or edit name servers`. You can update the name servers with given cloudflare name servers.


![Change here](images/posts/2017-05-15-always-on-ssl-of-github-pages/change-here.png)

## Set configuration on Cloudflare

We need to wait for up to several hours. In my case only several minutes.

* `SSL`: Set `Flexible` because between GitHub and Cloudflare cannot communicate in SSL
* Confirm `Edge Certificates` has universal SSL certificates.
* `Page Rules`: Add rule to redirect `http://<Your Domain>` to `Always to Use HTTPS`

Please wait for a while, you can see your connection to the site is through SSL.

![security on chrome](images/posts/2017-05-15-always-on-ssl-of-github-pages/security-on-chrome.png)

Thanks
