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

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1449355730&asins=1449355730&linkId=821d014eded5702990704ba84efa3acc&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>