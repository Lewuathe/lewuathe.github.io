---
title: "Trimming zero values from Python list"
layout: post
date: 2017-11-04 10:07:24 +0900
image: 'images/'
description:
tag: ["Python", "Numpy"]
blog: true
author: "lewuathe"
---

I know how to trim white space characters from string in Python. You can use `strip` method in `str` type. (Python does not privde `trim` method :()

```python
>> ' I know how to write Python  \t'.strip()
'I know how to write Python'
```

But do you know how to trim zero values from Python list? What I wanted to do was:

```
>> l = [0, 0, 0, 1, 2, 3, 0, 0]
>> trim(l)
[1, 2, 3]
```

Numpy provided me an API to do exactly what I wanted to do. [`trim_zeros`](https://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.trim_zeros.html). 

```python
>>> import numpy as np
>>> l = [0, 0, 0, 1, 2, 3, 0, 0]
>>> np.trim_zeros(l)
[1, 2, 3]
```

Great!