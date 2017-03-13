---
layout: post
blog: true
title: "Easy template rendering with Python"
date: 2015-08-16 22:32:00 +0900
comments: true
categories: ["Python"]
author: Kai Sasaki
---

There were some cases I want to render some template file easily without any rendering engine(such as ERB, jade).
So far I wrote some script which uses `sed` command to replace an arbitrary placeholder written by myself. This is a little tough work and
not maintainable. I have found a easy way to render an template file with only Python.

<!-- more -->

Python has already original format print method. You might see it.

```python
>>> vars = {"yourname":"Nobita", "myname":"Kai"}
>>> print("Hello, %(yourname)s" % d)
Hello, Nobita
```

We can use this method for rendering template file. Your `template.txt` file can be like this.

```
Hello, %(yourname)s, my name is %(myname)s. Nice to meet you!
```

In python script, your can write below code to replace all placeholders.

```python
#!/usr/bin/env python

# This is given from other place.
vars = {
  "yourname": "Takeshi", "myname": "Kai"
}

with open("./template.txt") as f:
    data = f.read()
    print(data % vars)
```

OK. We can obtain desired output from this script.

```
Hello, Takeshi, my name is Kai. Nice to meet you!
```

When you put template file with rendering such as configuration files, you can use this way. Thank you.
