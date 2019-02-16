---
title: "Custom WebGL Operation in TensorFlow.js"
layout: post
date: 2019-02-16 11:12:03 +0900
image: 'assets/img/posts/2019-02-16-custome-webgl-operation-in-tensorflow/catch.jpg'
description:
tag: ['TensorFlow', 'DeepLearning', 'TypeScript', 'JavaScript', 'Web']
blog: true
author: "Kai Sasaki"
---

[TensorFlow.js](https://js.tensorflow.org/) is a framework that enables us to run deep learning model in the web browser easily and efficiently. As you may imagine, tensor manipulation requires huge amount of computation power. The defact standard way for that is currently using accelerator such as GPU. GPU provides us a large amount of parallelism so that we can distribute the tensor calculation in the multiple threads. TensorFlow.js make it possible even in the web browser by using [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API). WebGL is a standard API to use GPU from web browser mainly for graphical processing. Thanks to WebGL, we can see the rich web contents smoothly. [Chrome experiments](https://experiments.withgoogle.com/collection/chrome) shows bunch of fun experience realized by using WebGL. 

In this article, I'm going to briefly explain how to create a custom operator that is leveraged by WebGL acceleration in TensorFlow.js. This explanation based on the official documentation so please refer [*"Creating custom WebGL operations"*](https://js.tensorflow.org/tutorials/custom-webgl-op.html) more detail.

# Operator in TensorFlow.js

First, it's necessary to know the structure of kernel in TensorFlow.js. Each operator is implemented as the collection of multiple basic kernels. Kernels are the minimul unit of tensor manipulation. For example, [`tf.oneHot`](https://js.tensorflow.org/api/0.15.1/#oneHot) operator runs `oneHot` kernel implemented for CPU and WebGL repectively. If WebGL is available, TensorFlow.js chooses the WebGL backend transparently so that the application can be leverated by WebGL acceleration without rewriting applicaition code.

[![Backend Structure](assets/img/posts/2019-02-16-custome-webgl-operation-in-tensorflow/backend.png)](https://arxiv.org/pdf/1901.05350.pdf)

`backend` provides the interface to access the kernels. It has CPU and WebGL implementations. Once a kernel has WebGL implementation, it can be run on GPU without any modification to the above layer over `backend`. 

```ts
import * as tf from '@tensorflow/tfjs';
// oneHot operator is executed by the backend implementation.
tf.oneHot(tf.tensor1d([0, 1], 'int32'), 3).print();
```

Currently, TensorFlow.js supports three types backend officially. 

1. CPU
2. WebGL
3. [Node.js](https://github.com/tensorflow/tfjs-node)

CPU is just a JavaScript runtime running in the web browser so it's the slowest implementation. TensorFlow.js should fallback to this implementation if any other backend implementation is not available. WebGL will be described later. You can use TensorFlow core implementation via Node.js. TensorFlow provides [C API](https://www.tensorflow.org/install/lang_c) so that it can be binded by any other languages which supports C extension. Node.js backend delegates the computation to TensorFlow core. It indicates that we can use any kind of functionality of TensorFlow technically by using Node.js backend. If you are interested in Node.js backend, the detail is described [in the repository](https://github.com/tensorflow/tfjs-node). 

So how does WebGL look like?

# Using WebGL as GPGPU

Since WebGL was originally designed for acceleration of graphical processing, it requires some tricky technique to use WebGL for tensor computation. Input tensors are copied as texture to GPU memory. It can be regarded as the simple square and the computation is executed as fragment shader in WebGL pipeline. The following example shows how adding two tensors is done in WebGL. As you can see 

[![texture](assets/img/posts/2019-02-16-custome-webgl-operation-in-tensorflow/texture.png)](https://arxiv.org/pdf/1901.05350.pdf)


