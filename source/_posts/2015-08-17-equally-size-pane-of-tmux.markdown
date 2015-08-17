---
layout: post
title: "Equally size pane of tmux"
date: 2015-08-17 20:29:50 +0900
comments: true
categories: ["tmux"]
author: Kai Sasaki
---

You can split your terminal with [tmux](https://tmux.github.io/). But these pane sizes are not same when you split more than 3 panes.
This is not good to see and even might be obstacle for development. You can split equally size panes with only below two lines.

```sh
# split -v S
unbind S
## bind S split-window <- this is an original line.
bind S split-window \; select-layout even-vertical

# split vertically
unbind |
## bind | split-window <- this is an original line.
bind | split-window -h \; select-layout even-horizontal
```

![splits](/images/posts/2015-08-17-equally-size-pane-of-tmux/split.png)

This is easy way! 
