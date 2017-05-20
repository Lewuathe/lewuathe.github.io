---
title: "functools for cache"
layout: post
date: 2017-05-20 11:33:29 +0900
image: 'images/'
description:
tag: ["Python", "functools"]
blog: true
author: "lewuathe"
---

functools was introduced from Python3. This library provides the utility for creating higher-order functions in Python. I didn't have any experience of using functools.

But today I read [the useful article](https://dev.to/rpalo/cache-me-outside-speed-boosts-in-python) and tried `lru_cache` functionality by myself. It was introduced in [Python 3.2](https://docs.python.org/3/library/functools.html#functools.lru_cache). So please upgrade your Python if 3.x is not installed. It must be worth doing.

## Run fibonacci

You may have many times to write a function which returns fibonacci number with given sequence index.

```python
def fib(n):
    if n in [1,2]:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
```

How long it takes to finish `fib(35)`?

```python
start = time.time()
fib(35)
print("elapsed time: {}".format(time.time() - start))

# elapsed time: 3.272068977355957
```

Around 3.3 seconds. The elapsed time of the function is growing exponentially by increasing `n`. You might not be able to wait to finish `fib(100)`!

You can easily make the speed up by using `functools.lru_cache`. Just adding annotation.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fib_cache(n):
    if n in [1,2]:
        return 1
    else:
        return fib_cache(n - 1) + fib_cache(n - 2)
```

`maxsize` specifies the number of saved recent calls. The LRU feature performs best when maxsize is a power-of-two. (e.g. 64, 128) So I set 128. If you specify `None`, the cache grow without bound.

Then try to run the program.

```python
start = time.time()
fib_cache(35)
print("elapsed time with cache: {}".format(time.time() - start))
print(fib_cache.cache_info())

# elapsed time with cache: 2.5987625122070312e-05
# CacheInfo(hits=32, misses=35, maxsize=128, currsize=35)

```

It finished in very short time. `cache_info()` returns the information for checking the usage of cache. Since it shows 32 cache hits, we found we could save 32 function calls in total.

In Python3, we can enable cache feature by just adding `lru_cache` annotation. Please try it.

## Reference

* [10.2. functools — Higher-order functions and operations on callable objects](https://docs.python.org/3/library/functools.html#functools.lru_cache)
* [Cache Me Outside: Speed Boosts in Python](https://dev.to/rpalo/cache-me-outside-speed-boosts-in-python)
