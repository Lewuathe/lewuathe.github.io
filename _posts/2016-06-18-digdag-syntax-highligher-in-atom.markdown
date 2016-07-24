---
title: "Digdag syntax highlighter in Atom"
layout: post
date: 2016-06-18 10:06:48 +0900
image: 'images/'
description:
tags: ["Digdag", "Atom"]
blog: true
jemoji:
author: lewuathe
---

[Digdag](http://www.digdag.io) was released from [Treasure Data](http://www.treasuredata.com).
This is a highly scalable distributed workflow engine. It was developed for both analyst and engineers
in order to make their daily batch and adhoc jobs more easy. The important part I want to say here is
we can define workflow in one file called `*.dig`. So you can put the file under version control system like Git.
And all scripts and resources which is necessary to run each tasks are included in a digdag project.

The detail is described in [digdag.io](http://www.digdag.io).

<!-- more -->

What I want to tell here is that there is no syntax highlighter in Atom for `*.dig` file. So I wrote a package to do so.

[language-digdag](https://atom.io/packages/language-digdag)

You can install the package with this command.

```
$ apm install language-digdag
```

After you install this package your `*.dig` file can be seen like below.

![language-digdag](/images/posts/2016-06-18-language-digdag/language-digdag.png)

Since this is the first time I created syntax highlighter in Atom, I'm not sure what type of classes exists in Atom yet.
I searched which type of class is appropriate referring [language-ruby](https://atom.io/packages/language-ruby).
So if you find any other keyword or directive to be listed, please send me a Pull Request.

Thank you.
