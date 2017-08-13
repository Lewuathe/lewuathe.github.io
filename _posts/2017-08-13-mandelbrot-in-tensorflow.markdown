---
title: "Mandelbrot in Tensorflow"
layout: post
date: 2017-08-13 18:09:01 +0900
image: 'images/'
description:
tag: ["Tensorflow"]
blog: true
author: "lewuathe"
---


I found a interesting example in Tensorflow tutorials.

Tensorflow is famous as a deep learning framework. We can write various kind of deep learning algorithms in Tensorflow efficiently. But it is also sufficiently general machine learning and numerical computation library. We can write any kind of computation like [K-means](https://learningtensorflow.com/lesson6/). Tensorflow community provides [useful tutorials](https://www.tensorflow.org/tutorials/) for understanding Tensorflow potential. In this post, I will try to run [Mandelbrot simulation](https://en.wikipedia.org/wiki/Mandelbrot_set) by Tensorflow.

# Mandelbrot Set

Mandelbrot set is a set of complex number which satisfied a specific condition. The condition is this.

* $$c$$ is a complex number
* which does not diverge by several applications of below function

\begin{equation}
f_c (z) = z^2 + c
\end{equation}

The iteration is started from $$z=0$$. In short, the points in Mandelbrot set must not be diverged by $$...f_c(f_c(f_c(0)))...$$. The result set can be seen like this as you know.

![](https://upload.wikimedia.org/wikipedia/commons/2/21/Mandel_zoom_00_mandelbrot_set.jpg)

# Mandelbrot in Tensorflow

In Tensorflow, the flow can be like this.

1. Prepare whole data set in complex number space
2. Apply the function several times
3. Check the value is diverged

The code is this. I used Tensroboard to visualize Mandelbrot set instead of PIL image as in tutorial. Tensroboard provides good API and features to visualize metrics in such computation iterations.

```python
import tensorflow as tf
import numpy as np

# The size of complex number space
HEIGHT = 520
WIDTH = 600

Y, X = np.mgrid[-1.3:1.3:0.005, -2:1:0.005]
Z = X+1j*Y

# Initial value
xs = tf.constant(Z.astype(np.complex64))
# Complex number by each iteration
zs = tf.Variable(xs)

# The points which are not diverged
ns = tf.Variable(tf.zeros_like(xs, tf.float32))

# Compute the new values of z: z^2 + x
zs_ = zs*zs + xs

# Check whether the value is diverged or not
not_diverged = tf.abs(zs_) < 4

# tf.group just does computation without returning the result
# This operation suits for such numerical simulation
step = tf.group(zs.assign(zs_), ns.assign_add(tf.cast(not_diverged, tf.float32)))

# Ops for writing Mandelbrot image for Tensroboard
summary_image = tf.reshape(ns, [1, HEIGHT, WIDTH, -1])
tf.summary.image('Mandelbrot', summary_image)
merged = tf.summary.merge_all()

# Initialize all variables
init = tf.global_variables_initializer()

ret = []
with tf.Session() as sess:
    sess.run(init)
    writer = tf.summary.FileWriter('./mandelbrot', sess.graph)
    # Running iteration 200 times
    for i in range(200):
        _, summary = sess.run([step, merged])
        # Write image in each iteration
        writer.add_summary(summary, i)

    writer.close()

```

The result is this. After running 3 iterations, the whole Mandelbrot structure cannot be seen.

![iteration 3](images/posts/2017-08-13-mandelbrot-in-tensorflow/iter_3.png)

After running 170 iterations, we got clear Mandelbrot image as we know.

![iteration 170](images/posts/2017-08-13-mandelbrot-in-tensorflow/iter_170.png)

Good!

## Reference
* https://www.tensorflow.org/tutorials/mandelbrot
