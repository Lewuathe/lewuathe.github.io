---
layout: post
title: "Optimization for neural network"
date: 2016-04-11 20:39:59 +0900
comments: true
categories: ["Neural Network"]
author: Kai Sasaki
---
The other day I read [this article](http://sebastianruder.com/optimizing-gradient-descent/). This post was written about
the variation of gradient descent algorithm. Gradient descent is an de facto standard algorithm for optimizing deep learning.
Iterative optimization algorithm such as gradient descent plays an important role in deep learning because there is no way
to find the global solution analytically.

<!-- more -->

A lot of research has been done to find efficient type of gradient descent for training large scale deep neural network.
I heard about some of them, but I didn't understand the detail of each algorithm. So I decided to implement small samples
to run these gradient descent algorithms. This project was [uploaded on GitHub](https://github.com/Lewuathe/nn-optimization).
I implemented some of the algorithms actively researched and I could figure out why recent developed algorithms optimize faster
and reach global minimum. I wrote the program in Python and numpy. The problem to learn was mimicking sine wave with neural network.

[![SGD Training](http://img.youtube.com/vi/-mmMzCEmFI8/0.jpg)](https://www.youtube.com/watch?v=-mmMzCEmFI8)

So the program is very simple to read. I could grasps the structure of optimization algorithm and each gradient descent algorithm. I hope the program can also help you understand the variation of gradient descent algorithms recently developed.

Thank you.
