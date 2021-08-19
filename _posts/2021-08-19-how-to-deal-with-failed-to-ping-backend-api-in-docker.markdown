---
title: "How to deal with 'Failed to ping backend API' in Docker"
layout: post
date: 2021-08-19 09:24:25 +0900
image: 'assets/img/posts/2021-08-19-how-to-deal-with-failed-to-ping-backend-api-in-docker/catch.jpg'
description:
tag: ['Docker', '']
blog: true
author: "Kai Sasaki"
---

After I upgraded the docker to the latest version, I constantly face the following error.

![error](/assets/img/posts/2021-08-19-how-to-deal-with-failed-to-ping-backend-api-in-docker/error.png)

According to the instruction, I clicked some buttons, but it turns out to be in vain. The dialog did not display any response at all. There is no way to fix the problem and make it disappear other than restarting the machine. It is so stressful to see the error keeps showing up every time I launched the laptop.

Although the issue is already discussed [here](https://github.com/docker/for-mac/issues/5037), it's not resolved yet. It seems to be the bug of the Docker engine installed in the macOS machine.

How can we deal with the situation?



# Restarting Docker

The easiest and most effective way I have found was restarting the docker process by force. For example, just running the following command will remove the dialog and relaunch the process without any trouble.

```bash
$ killall Docker && cd /Applications;open -a Docker;cd ~
```

Every time I see the error message, I quickly run the command and continue to start on my work :)

For your reference, my docker engine version is v20.10.7. macOS is 10.15.17.


# Reference

- [Updated Docker, Now Doesn't Work #5037](https://github.com/docker/for-mac/issues/5037)

