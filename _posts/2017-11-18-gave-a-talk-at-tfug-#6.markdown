---
title: "Gave a talk at TFUG #6"
layout: post
date: 2017-11-18 10:19:10 +0900
image: 'images/'
description: 
tag: ["TensorFlow", "Conference", "DeepLearning"]
blog: true
author: "lewuathe"
---

In this week, I gave a talk at [TensorFlow User Group meetup](https://tfug-tokyo.connpass.com/event/69778/) in Tokyo. I have wanted to attend this meetup for a long time but kept falling in lottery to attend :(
So in this time, I decided to give a talk about deep learning and TensorFlow because a speaker can get a priority participation. 

<iframe src="//www.slideshare.net/slideshow/embed_code/key/EKHL1CDYWr8iJ8" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/lewuathe/deep-dive-into-deeplearnjs" title="Deep dive into deeplearn.js" target="_blank">Deep dive into deeplearn.js</a> </strong> from <strong><a href="//www.slideshare.net/lewuathe" target="_blank">Kai Sasaki</a></strong> </div>

This talk was about [deeplearn.js](https://deeplearnjs.org/) which some Google recently published as open source software recently. The most interesting thing about deeplearn.js is that it uses WebGL for accelerating numeric calculation of deep learning. Many deep learning frameworks like Torch, TensorFlow make use of GPU to achieve high performance computation. But it is often difficult and tough work to prepare GPU environment due to its cost. And also each vendor of GPU provides totally different API, which make things worse for GPU application engineers because our application on NVIDIA GPUs won't work on AMD GPUs. 

WebGL provides a standarized API to write GPU application code. This API is implemented in major web browsers such as Chrome, Firefox, Safari and Opera. You can highly expect your application user to install one of these browsers. It means your deep learning application that is hardware accelerated can be available a lot of users who are not familiar with GPU environment. 

deeplearn.js is now actively developed. It's [waiting for your contribution](https://github.com/PAIR-code/deeplearnjs/issues)!

