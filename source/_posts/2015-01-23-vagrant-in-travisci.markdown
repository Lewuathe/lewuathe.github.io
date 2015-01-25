---
layout: post
title: "Vagrant in TravisCI"
date: 2015-01-25 18:57:41 +0900
comments: true
categories: ["TravisCI", "Vagrant"]
author: Kai Sasaki
---

I received pull request from [Bill Warner](https://github.com/TD-4242). He writes unittest which used [test-kitchen](https://github.com/test-kitchen/test-kitchen) and
[RSpec](http://rspec.info/). This pull request is a great resource for me because I didn't know how to write test code for cookbook.
There are a lot of things I can obtain. I cannot say thank you enough. And I always glad to receive PR from anyone, anytime.

<!-- more -->

So after merging it, I want to run this test automatically. Continuous integration on [TravisCI](https://travis-ci.org/Lewuathe/storm-cookbook).
That's the way I always do after writing test code. But this time there is one obstacle to me. Vagrant.
test-kitchen uses Vagrant inside travis-ci instance. So you have to install Vagrant. Until v1.5.0, Vagrant is provided through
[gems](https://rubygems.org/gems/vagrant). But current Vagrant is distributed only as platform specific packages.
This means you have to install Vagrant through debian package in case of travis-ci. What have we to do?

I found one simple way. You can install debian package from [here](https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.2_x86_64.deb).
And Vagrant needs Oracle VirtualBox which is available with `apt-get`. So all you have to do is writing below script.

```
install:
  - sudo apt-get update -q
  - sudo apt-get install -q virtualbox --fix-missing
  - sudo wget -nv https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.2_x86_64.deb
  - sudo dpkg -i vagrant_1.7.2_x86_64.deb
  - bundle install
```

This is a part of `.travis.yml`. `install` directive is used for configuration of build environment.
The fact that we can use Vagrant virtual machine on travis-ci is very amazing to me. It reminds me of the powerful
ci platform which is always stands by me. I cannot help keeping using ci hostring services such as TravisCI!
