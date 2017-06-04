---
title: "Tensorflow Ops"
layout: post
date: 2017-05-28 15:00:11 +0900
image: 'images/'
description:
tag:
blog: true
author: "lewuathe"
---

[Tensorflow](http://tensorflow.org/) is a famous library for creating deep learning models. We can run efficient deep learning algorithms
in Google scale. But it's more **GENERAL** library than you thought. I have found that in this [lessons](http://web.stanford.edu/class/cs20si/syllabus.html).
So I want to write several useful tips about Tensorflow Ops.

## Visualize you graph on Tensorboard

Tensorboard visualize your graph in fine way easily.

```python
import tensorflow as tf

# Add some operations here...

with tf.Session() as sess:
	writer = tf.summary.FileWriter('./graphs', sess.graph)
	sess.run()

writer.close()
```

The graph information is written under `./graphs` directory. You can launch your tensorboard.

```
$ tensorboard --logdir="./graphs"
```

![tensorboard](images/posts/2017-05-21-tensorflow-ops/tensorboard.png)

## Constant

You can add the name shown in tensorboard.

```python
a = tf.constant([2.0, 3.0], name='a')
```

Some ops has syntax sugar.

```python
a = tf.constant(2.0, name='a')
b = tf.constant(3.0, name='b')

# Same result
c = tf.add(a, b)
c = a + b
```

Filled with specific values.

```python
tf.zeros([2, 3], tf.int32) # ==> [[0, 0, 0], [0, 0, 0]]
tf.ones([2, 3], tf.int32)  # ==> [[1, 1, 1], [1, 1, 1]]

t = tf.constant([[1, 2], [3, 4]])
tf.zeros_like(t) # ==> [[0, 0], [0, 0]]
tf.ones_like(t)  # ==> [[1, 1], [1, 1]]

tf.fill([2, 3], 8) # ==> [[8, 8, 8], [8, 8, 8]]
```

Sequences of constant values.

```python
tf.linspace(10.0, 20.0, 4) # ==> [10., 13.33333302, 16.66666603,20.]

tf.range(1.0, 4.0, 1.2) # ==> [1., 2.20000005, 3.4000001]
```

Randomly generated constants.

```python
tf.random_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
tf.truncated_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None,
name=None)
tf.random_uniform(shape, minval=0, maxval=None, dtype=tf.float32, seed=None,
name=None)
tf.random_shuffle(value, seed=None, name=None)
tf.random_crop(value, size, seed=None, name=None)
tf.multinomial(logits, num_samples, seed=None, name=None)
tf.random_gamma(shape, alpha, beta=None, dtype=tf.float32, seed=None, name=None)
```

One thing to be noted here is that constant are stored in the graph definition itself. If you add a huge
constant which consumes a lot of memory, it is recommended to be added as `Variable`. Otherwise loading time
of model definition can be longer.

## Data Types

Tensorflow ops can receive Python native types as well.

```python
t_0 = 42
tf.zeros_like(t_0) # ==> 0

t_1 = ["apple", "peach", "banana"]
tf.zeros_like(t_1) # ==> ['', '', '']
tf.ones_like(t_1) # ==> TypeError is thrown

t_2 = [[True, True], [False, False]]
tf.zeros_like(t_2) # ==> All False matrix
tf_ones_like(t_2)  # ==> All True matrix
```

`ones` is not defined in string value in Tensorflow. Tensorflow can receive numpy data types as well.

```python
import tensorflow as tf
import numpy as np
tf.int32 == np.int32 # True
```

But basically, it's not recommended because the compatibility between TensorFlow and numpy can be broken in future release.

## Variable

`Variable` is in-memory buffer to hold variables of the model.

```python
v = tf.Variable([1,2], name='v')
```

Variable is a class, on the other hand constant is a TensorFlow op. So please note `Variable`'s first latter is upper case.
Actually v has several ops internally.

```python
v.initializer
v.value()
v.assign(...)
v.assign_add(...)
```

You have to initialize all variables in advance.

```python
init = tf.global_variables_initializer()
with tf.Session() as sess:
	sess.run(init)
```

You can see the actual value of `Variable` by using `eval` method.

```python
W = tf.Variable(tf.truncated_normal([700, 10]))
with tf.Session() as sess:
	sess.run(W.initializer)
	print W.eval()
>> [[-0.76781619 -0.67020458 1.15333688 ..., -0.98434633 -1.25692499
 -0.90904623]
 [-0.36763489 -0.65037876 -1.52936983 ..., 0.19320194 -0.38379928
 0.44387451]
 [ 0.12510735 -0.82649058 0.4321366 ..., -0.3816964 0.70466036
 1.33211911]
 ...,
 [ 0.9203397 -0.99590844 0.76853162 ..., -0.74290705 0.37568584
 0.64072722]
 [-0.12753558 0.52571583 1.03265858 ..., 0.59978199 -0.91293705
 -0.02646019]
 [ 0.19076447 -0.62968266 -1.97970271 ..., -1.48389161 0.68170643
 1.46369624]]
```

When you initialize the Variable with another Variable, please use `initialized_value`.

```python
W = tf.Variable(tf.truncated_normal([10, 10]))
U = tf.Variable(W.initialized_value())
```

It ensures `U` is initialized with the value of `W`.

## Session

Usually you have to specify the session to be used explicitly.

```python
with tf.Session() as sess:
	sess.run(a + b)
```

You can set default session by using `InteractiveSession`.

```python
sess = tf.InteractiveSession()

a = tf.constant(1, name='a')
b = tf.constant(2, name='b')
c = a + b

print(c.eval()) # Use InteractiveSession
sess.close()
```

## Placeholder

Placeholder enables us to pass some values to graph at runtime.

```python
a = tf.placeholder(tf.float32, shape=[3])
b = tf.constant([5,5,5], name='b', dtype=tf.float32)

c = a + b

with tf.Session() as sess:
	sess.run(c, {a: [1,2,3]}) # [6,7,8]
```

If you specify `None`, placeholder can accept any shape in the field.


```python
x = tf.placeholder(tf.float32, shape=[None, 3])
W = tf.Variable(tf.truncated_normal([3, 2]), name='W')
b = tf.Variable(tf.truncated_normal([2]), name='b')

y = tf.matmul(x, W) + b
with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	sess.run(y, {x: [[0.1, 0.2, 0.3], [0.3, 0.3, 0.3], [0.1, 0.1, 0.1]]})

#	array([[ 1.08204758,  0.64428711],
#	       [ 0.99868155,  0.86420214],
#	       [ 0.76671058,  0.50330997]], dtype=float32)
```

But placeholder is just a way to indicate the actual value must be provided. So you can provide any value at runtime.


```python
a = tf.constant(1, name='a')
b = tf.constant(2, name='b')
c = a + b
with tf.Session() as sess:
	sess.run(c, {a: 10}) # 12
```

## Reference

* http://web.stanford.edu/class/cs20si/lectures/slides_02.pdf
