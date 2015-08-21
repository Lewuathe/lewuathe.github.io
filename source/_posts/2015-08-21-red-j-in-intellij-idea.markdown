---
layout: post
title: "Red J in IntelliJ IDEA"
date: 2015-08-21 21:47:20 +0900
comments: true
categories: ["IntelliJ IDEA"]
author: Kai Sasaki
---

In some cases when I use IntelliJ IDEA for Java projects, I faced this red J mark.

![J](http://i.stack.imgur.com/4hWdR.png)

This mark means these files are not included current project. So indexes of these files are not generated and search functionality
does not work. How can we solve this problem?

The answer is [here](http://stackoverflow.com/questions/4904052/what-does-this-symbol-mean-in-intellij).


> You need to specify the source dir
> File> Project Structure > Modules click the directory and click the Sources button

So in this wizard, only you have to do is `+` and add a missing module into your projects. That's all.


# Ref
* [What does this symbol mean in IntelliJ?](http://stackoverflow.com/questions/4904052/what-does-this-symbol-mean-in-intellij)
* [Image](http://stackoverflow.com/questions/18961951/intellij-idea-doesnt-compile-my-project-after-switch-from-jdk-1-6-to-1-7)
