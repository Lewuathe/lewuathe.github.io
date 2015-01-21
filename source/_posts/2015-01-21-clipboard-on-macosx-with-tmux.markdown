---
layout: post
title: "Clipboard on MacOSX with tmux"
date: 2015-01-21 20:50:37 +0900
comments: true
categories: ["Mac"]
author: Kai Sasaki
---

With default tmux, you may have some trouble copying text on clipboard. Drag with option key enables you to copy
selected text to clipboard. But the number of keys you have to touch when you select has been increased. This is completely
annoying. By using reattach-to-user-namespace, you can copy any text from copy mode of tmux to mac clipboard.
Below is the process.

```
# Use vim keybindings in copy mode
setw -g mode-keys vi

# Setup 'v' to begin selection as in Vim
bind-key -t vi-copy v begin-selection
bind-key -t vi-copy y copy-pipe "reattach-to-user-namespace pbcopy"

# Update default binding of `Enter` to also use copy-pipe
unbind -t vi-copy Enter
bind-key -t vi-copy Enter copy-pipe "reattach-to-user-namespace pbcopy"
```

My key binding is here. I use `Space` key as begin-selection`, and `Enter` key as `copy-pipe`.
Of course, if can change any keys as you like.

## Reference
[tmux Copy & Paste on OS X: A Better Future](http://robots.thoughtbot.com/tmux-copy-paste-on-os-x-a-better-future)
