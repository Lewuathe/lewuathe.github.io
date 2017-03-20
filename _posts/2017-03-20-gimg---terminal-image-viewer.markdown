---
title: "gimg - Terminal Image Viewer"
layout: post
date: 2017-03-20 22:23:53 +0900
image: 'images/'
description:
tag: ["Go", "Image"]
blog: true
jemoji:
author: "lewuathe"
---

At the beginning of this year, I decided to learn some new programming languages.
For now, these are [Go](https://golang.org/) and [Haskell](https://www.haskell.org/).
Go is obtaining popularity among system programming and development tools like [Docker](http://docker.com/).
Haskell seems to be good for learning another programming paradigm, pure functional programming.

Anyway the best way to learn a new programming language is reading and writing. So I created a tool in Go lang.

- [Lewuathe/gimg - Terminal Image Viewer](https://github.com/Lewuathe/gimg)

This is a terminal image viewer. You can show image file in console without any specific softwares.

For example, you can show the original image

![twitter_icon](https://pbs.twimg.com/profile_images/653148539409698816/I0NJNSm7.jpg)

```
$ gimg some.jpg
```

in console.

![sample](https://github.com/Lewuathe/gimg/blob/master/gimg/sample.png?raw=true)

It shows one pixel in one character space as default. If the image size is larger than your terminal window size,
you can specify the width.

```
$ gimg -size 10 some.jpg
```

![resized](images/posts/2017-03-20-gimg/resized.png)

BTW, the frog image is my [Twitter icon](https://twitter.com/Lewuathe).
