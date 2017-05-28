---
title: "Generator comprehension"
layout: post
date: 2017-05-28 12:06:11 +0900
image: 'images/'
description:
tag: ["Python"]
blog: true
author: "lewuathe"
---

As you may know, Python has list comprehension syntax.

```python
>>> [i for i in range(1, 10)]
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

The expression is not only applied to `list` but also dictionary and even generator!

In case of dictionary, we can use like this.

```python
>>> {str(v): v * v  for v in range(1, 4)}
{'2': 4, '1': 1, '3': 9}
```

We get the map from the str of number to squaring of the one.

Generator is used in `for` syntax look as `range` function.

```python
>>> for i in range(1, 3):
...     print(i)
...
1
2
```

The same thing can be done by using list or dictionary. But if that data structure has a lot of data, it can have memory pressure. Generator does not keep whole sequence on memory.

```python
>>> for i in (v * v for v in range(1, 5)):
...     print(i)
...
1
4
9
16
```

```python
>>> g = (v * v for v in range(1, 5))
>>> type(g)
<class 'generator'>
```

So you find that it's not list. 
