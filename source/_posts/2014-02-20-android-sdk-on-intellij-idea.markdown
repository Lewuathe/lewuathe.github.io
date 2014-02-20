---
layout: post
title: "Android SDK on IntelliJ IDEA"
date: 2014-02-20 21:24:56 +0900
comments: true
categories: ["IntelliJ IDEA", "Android"]
author: Kai Sasaki

---

Eventually, I finished android lecture that is introduced on [previous post](http://lewuathe.com/blog/2014/02/18/useful-shortcuts-for-intellij-idea/)
In this lecture, I learned how to use [Eclipse](https://www.eclipse.org/), [Java](http://java.com/ja/) and of course [Android SDK](http://developer.android.com/sdk/index.html)

After coming home, I tried to creating a environent for android application development. However only installing Eclipse and creating same environment to lectures one 
makes me tired. So I create this environment with [IntelliJ IDEA](http://www.jetbrains.com/idea/).


<!-- more -->

I use IntelliJ IDEA community edition because it is free. Until now I don't think there is any lack of function with community edition

## Install IntelliJ IDEA

From [this page](http://www.jetbrains.com/idea/), download IntelliJ IDEA community edition. Follow the instructions of wizard. Done!

![android project](/images/posts/2014-02-20-androidsdk-with-intellijidea/intellijidea-ce.png)



## Install Android SDK

From [here](http://dl.google.com/android/android-sdk_r22.2.1-macosx.zip), download android SDK. But there is one thing to pay attention. You don't have to install ADT bundler version, bacause this package includes Eclipse and its plugins. With IntelliJ IDEA, these are not necessary to install.

And then, unzip this package. Put `android-sdk-macosx` on any directory. For example, I put on my home directory.

```
~/android-sdk-macosx
```

Run android package manager, and install requires packages.

```
$ cd ~/android-sdk-macosx
$ ./android-sdk-macosx/tools/android
```

## Create project

Select android application module project.

![android project](/images/posts/2014-02-20-androidsdk-with-intellijidea/android-project.png)

And select android SDK version that you installed previously. In this capture, I selected API version 19.

![android project](/images/posts/2014-02-20-androidsdk-with-intellijidea/android-sdk.png)

It is very easy, isn't it?

But unfortunately, android simulator is no more faster :(

I pray for the faster android emulator to Google. 

Thank you :)



