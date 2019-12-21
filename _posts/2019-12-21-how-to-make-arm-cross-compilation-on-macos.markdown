---
title: "How to make ARM cross compilation on macOS"
layout: post
date: 2019-12-21 21:55:12 +0900
image: 'assets/img/posts/2019-12-21-how-to-make-arm-cross-compilation-on-macos/catch.jpg'
description:
tag: ['macOS', 'ARM']
blog: true
author: "Kai Sasaki"
---

Cross-compilation is occasionally troublesome. It often requires us to install additional toolchain to get it done.

Now, I found I needed to compile my source code for the Arm architecture machine for [Mbed application](https://github.com/Lewuathe/mbed-sample). I do not have any idea how to install the toolchain for Arm compilation. Thus this is the post to describe the fastest way to prepare the toolchain for the cross-compilation for Arm.

# Xcode Compiler

Please ensure to install Xcode first. Xcode contains the first compiler sets, such as clang.

```
$ xcode-select --install
```

# Arm Toolchains from Homebrew

You can install Arm GCC toolchains by using Homebrew. There are two options.

- [osx-cross/homebrew-arm](https://github.com/osx-cross/homebrew-arm)
- [ARMmbed/homebrew-formulae](https://github.com/ARMmbed/homebrew-formulae)

There is no difference between these two distributions. They use precisely the same package internally. You can use whichever you want.
For my Mbed application, I choose the second one.

```
$ brew tap ArmMbed/homebrew-formulae
$ brew install arm-none-eabi-gcc
```

You should be able to find the compiler eventually. The following tools are installed in the local machine.

```
$ arm-none-eabi-gcc
$ arm-none-eabi-g++
...
```

It looks like they are GCC for Arm architecture. I believe it is the easiest way to prepare the Arm build toolchains in macOS platform.

Thanks

Photo by [Chris Ried](https://unsplash.com/photos/bN5XdU-bap4) on Unsplash