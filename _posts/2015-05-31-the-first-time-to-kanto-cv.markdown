---
layout: post
blog: true
title: "The first time to Kanto CV"
date: 2015-05-31 09:06:03 +0900
comments: true
categories: ["CV"]
author: Kai Sasaki
---

Yesterday, I went to my alma mater in order to attend a seminar, [Kanto CV seminar](http://kantocv.connpass.com/event/14485/). I always applied to this seminar but I failed because
it was too late. Therefore this is the first time for me.

<!-- more -->

Kanto CV is about computer vision as its name suggests. Recently computer vision technologies looks overwhelmed by deep learning. (In fact I don't think so) We could hear a lot of technologies
about deep learning in this seminar as far as hear in slide or ustream. This time we can read some famous papers about which CV researchers and engineers should know. Although these themes are not restricted in deep learning fields, I attended this seminar to obtain fundamental skills and technologies as an software engineer.

# P-N learning: Bootstrapping Binary

<div style="text-align:center;">
<iframe src="//www.slideshare.net/slideshow/embed_code/key/8zOOXPEnHXi51K" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/takmin/pn-learning-takmin" title="Pn learning takmin" target="_blank">Pn learning takmin</a> </strong> from <strong><a href="//www.slideshare.net/takmin" target="_blank">Takuya Minagawa</a></strong> </div>
</div>

This is a little diffucult for me because I'm not familiar with tracking technologies. There are a lot of unknown terminologies. I want to relearn this when I have time and also interests.

# Curriculum Learning

<div style="text-align:center;">
<iframe src="//www.slideshare.net/slideshow/embed_code/key/BgIaSW6hJM19F8" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/YoshitakaUshiku/20150530-kantocv-curriculumlearning" title="20150530 kantocv curriculum_learning" target="_blank">20150530 kantocv curriculum_learning</a> </strong> from <strong><a href="//www.slideshare.net/YoshitakaUshiku" target="_blank">Yoshitaka Ushiku</a></strong> </div>
</div>

This is the most interesting session and also easy to understand his talk. Curriculum learning looks a meta algorithm of matchine learning. This algorithm only decides what order model have to learn each samples. According to curriculum learning, only learning easy samples first and diffucult ones later contributes improving performance and convergence speed of model. This idea was inspired by human learning process. Almost all of us cannot master mathmatics at elementary school. There is a lot of fundamental knowledge to learn in advance before entering university math class. In the same way, machine learning model should learn easy samples first. And Deciding what order a model should learn samples can be done automatically with Self-paced learning. This is what I want to implement by myself.

# Selective Search for Object recognition

<div style="text-align:center">
<iframe src="//www.slideshare.net/slideshow/embed_code/key/pCGdsJ5uT5d4JR" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/belltailjp/kantocvselective-search-for-object-recoginition" title="KantoCV/Selective Search for Object Recoginition" target="_blank">KantoCV/Selective Search for Object Recoginition</a> </strong> from <strong><a href="//www.slideshare.net/belltailjp" target="_blank">belltailjp</a></strong> </div>
</div>

An object detection can be very slow process because a computer have to trace all windows included one image. This calculation can be done about 25000windows/image. The method provides a framework for paring down candidates and making an object detection process speed up. Each algorithms used in this framework was provided by previous researches. The contribution of this framework is reducing computational cost by combining these existing algorithms.

# Learning to forget: Continual prediction with LSTM

This session's slide have not seemed uploaded yet. This is the only session about deep learning in yesterday seminar. Although the contents of this session were a lot, I can grasp the fundamentals of LSTM. I want to implement this into my current project.

# Learning Bayesian network from data

This session's slide also have not been uploaded yet. Bayesian network does not always restricted computer vision technologies. This session introduced the diffuculty of making a huge general bayesian network in realistic time. 

# End

Although this is the first time to attend Kanto CV seminar, there were a lot of inspiring and interesting sessions. I could obtain some knowledges and ideas to make use of in my projects at home and office. At next time, of course I want to attend and also I want to make some contents to give a presentation at this seminar.

Thank you.
