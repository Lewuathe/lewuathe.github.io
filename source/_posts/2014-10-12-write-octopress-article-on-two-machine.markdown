---
layout: post
title: "Write Octopress article on Two machine"
date: 2014-10-12 20:38:47 +0900
comments: true
categories: ["Blog", "MacPro"]
author: Kai Sasaki
---

By accident, I got [MacPro](https://www.apple.com/jp/mac-pro/). This is my first desktop machine in my life. I usually use notebook or laptop machine because
there were a lot of time to bring my machine outside. But now I found it is very confortable to use it, large size display, high spec for processing and sufficient amount of capacity.

![MacPro](/images/posts/2014-10-12-macpro/macpro.jpg)

<!-- more -->

I want to write Octopress article on MacPro. I wrote this on MacBookPro previously. So this time, I'd like to record how to achieve this goal.

# Clone source

First clone your octopress original source.

    $ git clone -b source git@github.com:username/username.github.com.git octopress

Then octopress has a built site under `_deploy` directory. You have to pull master branch into this directory.

    $ git clone  git@github.com:username/username.github.com.git _deploy

# Setup

Before setting up, you have to install [bundler](http://bundler.io/). 

    $ gem install bundler
    $ rbenv rehash
    $ bundle install

And setup your github pages url.

    $ bundle exec rake setup_github_pages

Last but not least, update all sources and built files.

    $ git pull origin source
    $ cd _deploy
	$ git pull origin master

OK this time you can deploy from this new machine. So I wrote this article on my new MacPro. Through this process, I want to say thank you to [Robert Anderson](http://blog.zerosharp.com/clone-your-octopress-to-blog-from-two-places/).
From now I will keep update my blog on super MacPro. 




