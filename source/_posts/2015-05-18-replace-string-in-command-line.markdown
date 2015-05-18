---
layout: post
title: "Replace string in command line"
date: 2015-05-18 20:28:49 +0900
comments: true
categories: ["Shell", "Command"]
author: Kai Sasaki
---

In daily development and operation, there are some times to replace string with command line. For example,

```
$ cat hostlist.txt
serviceA.foo.example.com
serviceB.foo.example.com
serviceC.foo.example.com
serviceD.foo.example.com
serviceE.foo.example.com
serviceF.foo.example.com
serviceG.foo.example.com
serviceH.foo.example.com
```

These hostlist files usually used by command line tools such as [fabric](http://www.fabfile.org/). When you want to deploy other service in example.com, how can we do that?
There are command line tools which is very useful and simple for replacing some string.

<!-- more -->

## tr

`tr` command translates characters. You can replace each one **character**.

```
$ cat hostlist.txt | tr "f" "b"
serviceA.boo.example.com
serviceB.boo.example.com
serviceC.boo.example.com
serviceD.boo.example.com
serviceE.boo.example.com
serviceF.boo.example.com
serviceG.boo.example.com
serviceH.boo.example.com
```

However it seems hard to replace one string not only one character. I think this is the case we usually face. So `sed` exists.

## sed

`sed` command replace one string, the sequence of character. You can replace foo service to bar service only one command.

```
$ cat hostlist.txt | sed s/foo/bar/
serviceA.bar.example.com
serviceB.bar.example.com
serviceC.bar.example.com
serviceD.bar.example.com
serviceE.bar.example.com
serviceF.bar.example.com
serviceG.bar.example.com
serviceH.bar.example.com
```

And also you can use regular expression with sed command. 


```
$ cat hostlist.txt | sed "s/^service[A-Z]/&-&/"
serviceA-serviceA.foo.example.com
serviceB-serviceB.foo.example.com
serviceC-serviceC.foo.example.com
serviceD-serviceD.foo.example.com
serviceE-serviceE.foo.example.com
serviceF-serviceF.foo.example.com
serviceG-serviceG.foo.example.com
serviceH-serviceH.foo.example.com
```

We can use matched string in later place as you like. This is powerful tool for daily operation. Thank you.


