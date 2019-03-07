---
title: "Annoucements in TensorFlow Dev Summit 2019"
layout: post
date: 2019-03-06 21:30:15 +0900
image: 'assets/img/posts/2019-03-06-annoucements-in-tensorflow-dev-summit-2019/catch.png'
description:
tag: ['TensorFlow', 'MachineLearning', 'DeepLearning', 'Google']
blog: true
author: "Kai Sasaki"
---

[TensorFlow Dev Summit](https://www.tensorflow.org/dev-summit/) is an annual conference held by Google collecting a bunch of topics around TensorFlow framework. I usually watch the conference via live stream on YouTube. But fortunately, I got a chance to attend the conference this time. There is a sear number of exciting announcements in the conference so I list up the interesting items in this article. 

# Table Of Contents

```
- TensorFlow 2.0
- TensorFlow Lite
- TensorFlow.js 1.0
- Others
```

# TensorFlow 2.0

TensorFlow 2.0 alpha has just been released today. The biggest change introduced by the version is the simplified API by Keras and default eager mode. It was a little hard to write the complicated control flow as a TensorFlow graph in the past. You need to be familiar with `tf.where` or `tf.select` in order to write the conditions. That makes programmers have a difficult time to write a code executing what they want to. 

From 2.0, you can use `tf.function` to write a complex control flow as TensorFlow graph. `tf.function` is just an annotation to be attached to the Python function. TensorFlow compiler automatically resolves the dependency on the Tensor and create a graph.

```python
@tf.function
def f(x):
  while tf.reduce_sum(x) > 1:
    x = tf.tanh(x)
  return x

f(tf.ranfom.uniform([10]))
```

In the above example, function `f` will be a TensorFlow graph because it depends on the given tensors, `a` and `b` even we don't define the ops for `while` control flow. That makes the development far easier because we can write the control flow of TensorFlow graph as we write the Python code. It is achieved by overloading some method like `__if__` or `__while__` under the hood. 
It also the necessity of `tf.control_dependencies` which was needed to update multiple variables properly. It contributes to reducing the complexity of graph construction too.

So overall you do not need to write the following things anymore.

- tf.session.run
- tf.control_dependencies
- tf.global_variables_initializer
- tf.cond, tf.while_loop

Please the here to look into more detail about TensorFlow 2.0 and Autograph feature. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/Up9CvRLIIIw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Improvements of TensorFlow Lite

One amazing thing I found in the conference was the TensorFlow project puts a significant amount of resource to the edge computing which is happening on the mobile device, wearable, browsers, and smart speakers. TensorFlow Lite is a symbolic product to accelerate the ML in Edge device. The ML in edge device is thought to be required by the following reasons.

- Fast Interactive Application
- Data Privacy

By running the ML application on the client side, we can eliminate the overhead of sending the data between server and client. It is beneficial especially in the environment where we have a limited amount of network resource or bandwidth. It also protects data privacy by avoiding to send data to the server. So the demand for the ML in edge device is growing more and more. 

TensorFlow Lite is a project to create a lightweight TensorFlow model running in the edge device. By delegating the processing to [**Edge TPU**](https://cloud.google.com/edge-tpu/), they achieve 62x faster inference time at maximum combining with quantization.

![Edge TPU](assets/img/posts/2019-03-06-annoucements-in-tensorflow-dev-summit-2019/edge-tpu.png)

They have also a super tiny model that is only tens of kilobytes so that we can put it into the microcontrollers. [Sparkfun](https://www.sparkfun.com/products/15170) is an edge demo board powered by TensorFlow. Exciting thing is that we could get the board as a gift of attending the conference. 
![Sparkfun](assets/img/posts/2019-03-06-annoucements-in-tensorflow-dev-summit-2019/sparkfun.png)

This kind of gift always makes me fun because we can try to use what we've learned. So I'm going to try the tiny model running on the microcontroller later. In my opinion, the evolution of the ML in the edge device is the most interesting field. Please take look into the video for more detail around TensorFlow Lite. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/DKosV_-4pdQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# TensorFlow.js 1.0

The reason why I'm involving with TensorFlow project is this. I keep contributing to TensorFlow.js since it has been published. (It was named deeplearn.js initially) It gave me an opportunity to write a book, "<a target="_blank" href="https://www.amazon.com/gp/product/B07GNZPP2P/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B07GNZPP2P&linkCode=as2&tag=lewuathe-20&linkId=6cb5cedc94d3351778f5e13948bd0e7e">Deep Learning in the Browser</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=B07GNZPP2P" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />". Evolving the project I'm involved game me a great joy. 

Now it has been released as 1.0 reaching a kind of milestone. In addition to core components, there are multiple supporting libraries around TensorFlow.js.

- **[tfjs-layers](https://github.com/tensorflow/tfjs-layers)**
- **[tfjs-data](https://github.com/tensorflow/tfjs-data)**
- **[tfjs-vis](https://github.com/tensorflow/tfjs-vis)**

Those libraries enable us to have a similar experience using TensorFlow core libraries. It must accelerate the application development in the client side supporting JavaScript runtime. Actually, TensorFlow.js project will support various kind of platform such as [Electron](https://electronjs.org/) and [React Native](https://facebook.github.io/react-native/) so that we can use the same application code in many platforms. 

Here is another interesting slide. The performance of TensorFlow.js in Chrome browser is becoming faster since its initial release. Therefore, TensorFlow.js can be said to be a production-ready platform that supports client-side ML application sufficiently. 

![Performance](assets/img/posts/2019-03-06-annoucements-in-tensorflow-dev-summit-2019/performance.png)

I also had a chance to talk with TensorFlow.js team members about the enhancements and development plan happening in near future. At the same time, I'm looking forward to these kinds of things, I want to contribute these things to make TensorFlow.js more powerful. Here is the video about the announcement of TensorFlow.js 1.0.

<iframe width="560" height="315" src="https://www.youtube.com/embed/x35pOvZBJk8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Others

Last but not least, I'm going to introduce some other changes I found at the conference.

- Released [tf-agents](https://github.com/tensorflow/agents) to accelerate reinforcement learning by using TensorFlow
- Tensorboard can be embedded in **[Google Colab](https://colab.research.google.com/)** and **[Jupyter notebook](https://jupyter.org/)**
- The new conference **[TensorFlow World](https://conferences.oreilly.com/tensorflow/tf-ca)** will be held Oct 28-31
- Two new online courses are available to learn TensorFlow at [Cousera](https://www.coursera.org/learn/introduction-tensorflow) and [Udacity](https://www.udacity.com/course/intro-to-tensorflow-for-deep-learning--ud187)

The full videos of presentation introduced in the conference are available on YouTube. Please take a look if you want to know further.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://www.youtube.com/channel/UC0rqucBdTuFTjJiefW5t-IQ" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fwww.youtube.com%2Fchannel%2FUC0rqucBdTuFTjJiefW5t-IQ%2Fvideos&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

Thanks!