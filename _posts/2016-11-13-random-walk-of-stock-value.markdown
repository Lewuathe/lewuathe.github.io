---
title: "Random Walk of Stock Value"
layout: post
date: 2016-11-13 11:24:10 +0900
image: 'images/'
description:
tag: ['Stock Value', 'Finance']
blog: true
jemoji:
author: "lewuathe"
---

I've read a book about financial mathematical model used in Wall Street.
This book describes about the people who invented the financial models which become state-of-the-art technologies nowadays.

[![png](/images/posts/2016-11-13-random-walk-of-stock-value/book.png)](https://www.amazon.co.jp/%E3%82%A6%E3%82%A9%E3%83%BC%E3%83%AB%E8%A1%97%E3%81%AE%E7%89%A9%E7%90%86%E5%AD%A6%E8%80%85-%E3%83%8F%E3%83%A4%E3%82%AB%E3%83%AF%E3%83%BB%E3%83%8E%E3%83%B3%E3%83%95%E3%82%A3%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E6%96%87%E5%BA%AB-%E3%82%B8%E3%82%A7%E3%82%A4%E3%83%A0%E3%82%BA%E3%83%BB%E3%82%AA%E3%83%BC%E3%82%A6%E3%82%A7%E3%83%B3%E3%83%BB%E3%82%A6%E3%82%A7%E3%82%B6%E3%83%BC%E3%82%AA%E3%83%BC%E3%83%AB/dp/4150504334)

I'm not familiar with finance detail but the book was very interesting. The models introduced in this book was simple.
So I want to write a tiny program to confirm the detail of these models.

## Random Walk model of profit rate

In the second chapter of the book, random walk model of profit rate is described. It means profit rate can be transitioned
completely at random. We cannot predict the profit rate of next time because it rises at 50% and falls at 50% as well.
This is random walk. A mathematician, Osborne find a profit rate is transitioned at random. So profit rate of stock value
can be described below.

```python
%matplotlib inline
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
```


```python
def random_walk(n):
    ret = [0]
    for i in range(n):
        if np.random.random() > 0.5:
            # Rising profit rate
            ret.append(ret[-1] + 0.01)
        else:
            # Falling profit rate
            ret.append(ret[-1] - 0.01)
    return ret

# We compute 100 trials
for i in range(100):
    plt.plot(random_walk(1000))

plt.xlabel('Time')
plt.ylabel('Interest rate')
```


![png](/images/posts/2016-11-13-random-walk-of-stock-value/output_1_1.png)

Osborne also find the profit rate at the time is distributed according to [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution) whose mean is 0.
The mean of profit rate at the future is 0 unfortunately. We cannot expect any growth of profit rate in average.

```python
from scipy.stats import norm
last_values = [random_walk(1000)[-1] for n in range(2000)]
x = np.arange(-5,5,0.01)

plt.hist(last_values, bins=30)
```


![png](/images/posts/2016-11-13-random-walk-of-stock-value/output_2_1.png)

Surely, the profit rate after 1000 time unit seems to be obeyed to normal distribution.

# Stock value transition

How about stock value itself? According to Osborne, if profit rate is decided by random walk model,
the stock value distribution can be [log-normal distribution](https://en.wikipedia.org/wiki/Log-normal_distribution).
Let's plot the transition of stock value with above profit rate model.


```python
def random_walk_value(n, initial_value):
    # Collect profit rate transition
    interest_rates = random_walk(n)
    # Initial stock value
    ret = [initial_value]
    for i in range(n):
        # Calculate revenue with given profit rate
        revenue = ret[-1] * interest_rates[i]
        ret.append(ret[-1] + revenue)
    return ret

# Compute 500 trials
for i in range(500):
    plt.plot(random_walk_value(20, initial_value=10.0))
```


![png](/images/posts/2016-11-13-random-walk-of-stock-value/output_3_0.png)

Now we can confirm the stock value at the specific time unit is distributed according to log-normal distribution.

```python
last_values = [random_walk_value(20)[-1] for n in range(1000)]
x = np.arange(-5,5,0.01)

plt.hist(last_values, bins=10)
```

The histogram of the stock value at the 20 time unit is plotted. It looks like log-normal distribution.

![png](/images/posts/2016-11-13-random-walk-of-stock-value/output_4_1.png)
