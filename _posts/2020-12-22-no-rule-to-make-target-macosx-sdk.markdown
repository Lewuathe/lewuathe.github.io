---
title: "No rule to make target for MacOSX SDK"
layout: post
date: 2020-12-22 15:01:22 +0900
image: 'assets/img/posts/2020-12-22-no-rule-to-make-target-macosx-sdk/catch.jpg'
description:
tag: ['macOS', 'C', 'C++', 'CMake']
blog: true
author: "Kai Sasaki"
---

I am usually conservative for upgrading the libraries my machine depends on. I do not click the update button even the OS installer urges me to do so because it is likely to temporarily slow down the productivity to deal with the problem that occurred just after the upgrade. That's not fun.

But this time, I was careless. I accidentally approved upgrading the Xcode in my mac. The target version is 12.3. I believed there should have been no problem in just upgrading one build toolchain. But I was wrong.

# No rule to make libcurses.

After I upgraded Xcode and install the toolchain alongside, my C++ project with CMake throws the following error.

```
No rule to make target `/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX11.0.sdk/usr/lib/libcurses.tbd'
```

Yes, `MacOSX11.0.sdk` is no more available, but my project still refers to the old SDKs unexpectedly. Some of the dependencies are correctly found under `MacOSX11.1.sdk`. Only the process to find libcurses failed.

I struggled to find the solution for hours and finally reached an unsophisticated answer.

# Create Symlink!

Since some tools keep referring to the old SDK, let's create a link to the new one with the old name!

```
sudo ln -s \
  /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk  \
  /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX11.0.sdk
```

It works. But that's a quite dirty way. I'm not sure how much impact it has on other software. If you have any ideas to resolve the situation better, please let me know. 