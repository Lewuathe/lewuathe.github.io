---
layout: post
title: "cgit cookbook"
date: 2015-06-22 21:06:19 +0900
comments: true
categories: ["cgit", "chef"]
author: Kai Sasaki
---

I created cgit server on EC2 before in order to check commit log and source code. (However, running EC2 constantly costs me not a few money. I terminated it. ) This process was a little troublesome for me. So I write the first cgit cookbook [here](https://supermarket.chef.io/cookbooks/cgit).

[cgit cookbook](https://github.com/Lewuathe/cgit-cookbook)

This cookbook will do

* Configuration of cgit service
* Launch cgit server with apache2

<!-- more -->

Repositories should be listed in `node['cgit']['project_list']` file. This file must be readable from cgit service. This project list file looks like this.

```
repo1
repo2
repo3
```

These are repository names. And then these repositories are stored in `node['cgit']['scan_path']` directory. This must be also readable from cgit service. The rest you have to do is git clone your desired repository under `scan_path`. cgit runs fast and easy to read because almost all features are based on the features of git itself. If you are familiar with git, you can see cgit dashboard quickly.

If you have any questions or advice for improvement, patches are always welcome!

Thank you.
