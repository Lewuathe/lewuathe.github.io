---
title: "Don't forget export"
layout: post
date: 2017-05-11 13:38:02 +0900
image: 'images/'
description:
tag: ["zshrc"]
blog: true
author: "lewuathe"
---

I made a mistake to set environment variable in `zshrc`.

```
ENV_VARIABLE1=var1
ENV_VARIABLE2=var2
```

But as you know it doesn't work. Please don't forget `export`.

```
export ENV_VARIABLE1=var1
export ENV_VARIABLE2=var2
```
