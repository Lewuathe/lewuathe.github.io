---
layout: post
title: "Unity crashes on Yosemite"
date: 2014-11-08 10:59:44 +0900
comments: true
categories: ["yosemite", "unity"]
author: Kai Sasaki
---

Yesterday, I found that iOS app exported by [Unity](http://unity3d.com/) with [Vuforia](https://developer.vuforia.com/) crashed as soon as launched.
This is critical problem because I cannot see the result totally! And I found [this page](http://qiita.com/JunSuzukiJapan@github/items/4e230f4a448f2db486f6)
This page described the simple process how to solve it. 

<!-- more -->

## Setting orientation

In exported project, `Info.plist` should be rewritten. You add new item named `UIInterfaceOrientation` and set as you like.

![setting](/images/posts/2014-11-08-unity-crash/setting.png)

That's all your Xcode project might not crash. Try it.
![setting](/images/posts/2014-11-08-unity-crash/result.png)




