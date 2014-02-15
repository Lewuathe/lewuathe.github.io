---
layout: post
title: "Stacked denoised autoencoder with nodejs"
date: 2014-01-29 21:38
comments: true
categories: ["nodejs", "autoencoder", "SdA"]
author : Kai Sasaki
---

I developed deep leanring module which enables you to use stacked denoised autoencoder in nodejs.
This is called n42. You can train with deep learning algorithm very easily.

https://npmjs.org/package/n42

<!-- more -->

## How to use

This is how to use it.

```js
    var n42 = require('n42');

    // input data
    // This is made of sylvester matrix
    var input = $M([
        [1.0, 1.0, 0.0, 0.0],
        [1.0, 1.0, 0.2, 0.0],
        [1.0, 0.9, 0.1, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.8, 1.0],
        [0.0, 0.0, 1.0, 1.0]
    ]);

    // label data
    // This is made of sylvester matrix
    var label = $M([
        [1.0, 0.0],
        [1.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 1.0],
        [0.0, 1.0]
    ]);

    var sda = new n42.SdA(input, label, 4, [3, 3], 2);

    // Training all hidden layers
    sda.pretrain(0.3, 0.01, 1000);

    // Tuning output layer which is composed of logistics regression
    sda.finetune(0.3, 50);

    // Test data
    var data = $M([
        [1.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 1.0]
    ]);

    console.log(sda.predict(data));

    /**
     *   Predict answers
     *   [0.9999998973561728, 1.0264382721184357e-7] ~ [1.0, 0.0]
     *   [4.672230837774381e-28, 1]                  ~ [0.0, 1.0]  
     */
```

If you want to know what stacked denoised autoencoder is, look this [page](http://deeplearning.net/tutorial/SdA.html)
Briefly, stacked denoised autoencoder is multi layer denoised autoencoder. 

First you should train denoised autoencoder by 
unsupervised learning. With this process, this network can extract characteristics of input data properly.

Second, you tune output logistics regression layer with gradient descent. 

And Last, only predict! It's easy, isn't it? 

Now the accuracy is depend on the parameters which you select considerably. Deep leanring algorithm might be the way it is, 
however, I want to develop end implement more general algorithms. In the next step, I'll develop restricted boltzmann machine, and
deep boltzmann machine. Thouhgh these algorithms are somewhat less accurate than stacked denoised autoencoder, n42 must have this algorithm
for own diversity, and the number of options.


## Last...

And the last but not least, if you find any bugs or any points to be fixed, patches are welcome!!
