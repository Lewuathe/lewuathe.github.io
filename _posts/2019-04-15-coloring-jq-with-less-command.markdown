---
title: "Coloring jq with less command"
layout: post
date: 2019-04-15 11:17:27 +0900
image: 'assets/img/posts/2019-04-15-coloring-jq-with-less-command/catch.png'
description:
tag: ['JSON', 'jq', 'CLI']
blog: true
author: "Kai Sasaki"
---

[JQ](https://stedolan.github.io/jq/) is one of the best tools I frequently use. One good thing of jq is that it automatically print the JSON in pretty format with fine coloring. So I often use JQ command just for printing JSON in a pretty manner. 

But this coloring can be disappeared when using a pipe to other commands such as `less`. 

```
$ cat sample.json | jq . | less
```

This is the common case when we want to see the long length JSON file. How can we deal with it?

JQ has an option `-C` to keep the color even when the output goes to pipe or file. So if you want to ensure the coloring with less command, here is a helpful example.

```
$ cat sample.json | jq . -C | less -R
```