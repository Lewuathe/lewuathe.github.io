---
title: "Try deeplearn.js"
layout: post
date: 2017-09-06 21:06:12 +0900
image: 'images/'
description:
tag: ["DeepLearning", "JavaScript", "TypeScript"]
blog: true
author: "lewuathe"
---

New deeplearning framework was released from [Google PAIR project](https://pair-code.github.io/).

[deeplearn.js](https://pair-code.github.io/deeplearnjs/)

![deeplearn](images/posts/2017-09-06-try-deeplearn-js/deeplearnjs.png)

deeplearn.js is written in JavaScript(TypeScript) to work on web browser. JavaScript is not a programming
language for machine learning or numerical calculation which requires huge CPU power. But deeplearn.js can
work on hardware accelerator like GPU through WebGL API. So it's not so slow as you expected. [WebDNN(https://mil-tokyo.github.io/webdnn/) or [Keras.js](https://transcranial.github.io/keras-js/#/).

Why not using TensorFlow or other framework?

Yes, TensorFlow is the fast and scalable framework many researcher and engineers are using. But it is often
difficult to create a application using TensorFlow model on web application because there is no TensorFlow
runtime on there. We can say similar thing in other framework.

So one of the good thing about deeplearn.js is that it can import TensorFlow model and run it on web browser.

[![](images/posts/2017-09-06-try-deeplearn-js/tensorflow-import.png)](https://pair-code.github.io/deeplearnjs/demos/mnist/mnist.html)

Currently it does not support TensorFlow ops fully. But there seems to be [a roadmap](https://pair-code.github.io/deeplearnjs/docs/roadmap.html) to implement and extend them.

If you want to try this, [here](https://pair-code.github.io/deeplearnjs/index.html#demos) is the best place.
Especially model builder is good tutorial to know the potential of deeplearn.js.

## Reference

* [deeplearn.js](https://pair-code.github.io/deeplearnjs/)
* [WebDNN](https://mil-tokyo.github.io/webdnn/)
* [Keras.js](https://transcranial.github.io/keras-js/#/)
