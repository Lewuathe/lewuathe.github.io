---
layout: post
blog: true
title: "How to use cgit"
date: 2015-06-04 20:53:25 +0900
comments: true
categories: ["cgit", "git"]
author: Kai Sasaki
---

When I want to browse a git repository, I usually use [GitHub](https://github.com) if the desired repository is there. Of couse GitHub always provides great experience whenever looking into source code of a famous open source software.
But I found there are three cases when I want an alternative.

<!-- more -->

* GitHub is slow for just browsing source code.
* GitHub does not host official repositories managed by Apache.
* Internal cases such as enterprise.

So I searched alternate software to just only browsing my private codes. Then I found what I want when I read linux [kernel source code](https://git.kernel.org/cgit/).

That is called [cgit](http://git.zx2c4.com/cgit/). This is a hypertext web frontend for git repositories written in C. This is written in C! Can you believe it? I was used to LL and Java when develop web services and middlewares. This is the first time to meet a web frontend written in C. Although I don't know the reason why this tool is written in C, this cgi server works with amazing speed. Browsing experience was very good. So I'd like to introduce you how to host cgit server here. These descriptions are valid on CentOS/RHEL environment.

## Prerequisites

```bash
$ sudo yum install httpd openssl-dev gcc git
```

# Install cgit

```bash
$ git clone git://git.zx2c4.com/cgit
$ cd cgit
$ make get-git
$ vim cgit.conf   # Create configuration file
```

This is the `cgit.conf`.

```yaml
CGIT_SCRIPT_PATH = /var/www/cgit
```

```bash
$ make
$ sudo make install
```

In this way, cgit will be installed under `/var/www/cgit`.

# Writing configurations

You should write configuration file `/etc/cgitrc`.

```bash
$ cat /etc/cgitrc
logo=/cgit/cgit.png
css=/cgit/cgit.css
favicon=/cgit/favicon.ico
project-list=/home/yourname/projects.list
scan-path=/home/yourname/repositories
```

`project-list` is the file which lists all repository names. This is written like

```bash
$ cat /home/yourname/projects.list
repo1
repo2
repo3
```

And scan-path is the directory where all repositories you want to see through cgit. At last httpd has to know about this cgi service.

```bash
cat /etc/httpd/conf.d/cgit.conf
Alias /cgit /var/www/cgit
<Directory /var/www/cgit>
  Options +ExecCGI
  AddHandler cgi-script cgi
</Directory>
```

# Start cgit

Start httpd server.

```bash
$ sudo service httpd start
```

You will see http://yourhost.com/cgit/cgit.cgi. It runs very high speed, isn't it?
I hope you will be the person who investigate some source code through cgit. I will!

Thank you.
