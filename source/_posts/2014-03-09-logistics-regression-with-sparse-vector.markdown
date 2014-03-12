---
layout: post
title: "Logistics Regression with Sparse Vector"
date: 2014-03-09 19:54:25 +0900
comments: true
categories: ["Python", "Logistics Regression", "Machine Learning"]
author: Kai Sasaki
---

In my project I have to develop a model that is capable of predicting the count of page view
from sparse vector data such as

```
[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
```

However I found it was difficult to make a model which can be applied to practical use case. From sparse vector, my current model
doesn't look trained sufficiently. I used [scikit-learn](http://scikit-learn.org/stable/index.html) in python.

<!-- more -->

My current code is below.

```python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import random
from sklearn import svm


if __name__ == "__main__":
    rand = np.random.RandomState(1234)
    xs = []
    ys = []
    print "Train"
    for i in xrange(0, 30):
	    """
	     x is a sparse vector generated from binomial distribution
		 x has a 1 vector generally speaking
		"""
        x = rand.binomial(size=100, n=1, p=0.01)
        xs.append(x)

        """
		 y is obtained from gaussian distribution which has 0.7 as mean value
        """
        y = rand.normal(loc=0.7, scale=0.1)
        ys.append(y)

    clf = svm.SVR()
	# Train data
    clf.fit(xs, ys)

    print "Test"
    ts = []
    for i in xrange(0, 10):
        ts.append(rand.binomial(size=100, n=1, p=0.01))

    print clf.predict(ts)
```

Through this process I can only get these results.

```python
[ 0.7507838   0.7507838   0.75058871  0.7507838   0.75058871  0.75058871
  0.73136874  0.7507838   0.75058871  0.75058871]
```

I think this result doesn't have valid significance for predicting. All values look the same to me!
Simple support vector machine might not be suitable to predict with sparse vector data. But I have no idea
how to make alternate model that can be constructed with sparse vectors. Is there anyone who have a good idea or
a paper which has proper algorithm for this case? I want to know the algorithm which can construct better regression
model from sparse vector. Please let me know that.

Thank you.



