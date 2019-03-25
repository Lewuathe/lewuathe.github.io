---
title: "Check ulimit by process"
layout: post
date: 2017-12-20 16:13:55 +0900
image: 'images/'
description:
tag: ["Unix", "ulimit"]
blog: true
author: "lewuathe"
---

`ulimit` is a utility tool to set some limitations of the user process. For example, you can set the maximum core file size by using `ulimit -c` command.

```
# It sets the max number of blocks used for the core file.
$ ulimit -c 100000
```

But `ulimit` does not show information about other processes. You may want to check the resource limitation put on the running processes. You can check the resource limitation of an arbitrary process by using `/proc` file system.

```
$ cat /proc/$PID/limits
Limit                     Soft Limit           Hard Limit           Units
Max cpu time              unlimited            unlimited            seconds
Max file size             unlimited            unlimited            bytes
Max data size             unlimited            unlimited            bytes
Max core file size        0                    unlimited            bytes
...
```
