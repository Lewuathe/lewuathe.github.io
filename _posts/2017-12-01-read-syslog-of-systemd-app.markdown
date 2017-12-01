---
title: "Read syslog of systemd app"
layout: post
date: 2017-12-01 22:37:12 +0900
image: 'images/'
description:
tag: ["syslog", "systemd", "Linux"]
blog: true
author: "lewuathe"
---

[Systemd](https://en.wikipedia.org/wiki/Systemd) enables you to bootstrap your service easily. The status of systemd service can be checked by using `systemctl` command.

```
$ systemctl status httpd.service
● httpd.service - The Apache HTTP Server
Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
Active: failed (Result: exit-code) since Tue 2016-03-01 11:53:07 UTC; 15s ago
Docs: man:httpd(8)
man:apachectl(8)
Process: 28473 ExecStop=/bin/kill -WINCH ${MAINPID} (code=exited, status=1/FAILURE)
Process: 28471 ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND (code=exited, status=1/FAILURE)
Main PID: 28471 (code=exited, status=1/FAILURE)
Mar 01 11:53:07 myclasslist systemd[1]: Starting The Apache HTTP Server...
Mar 01 11:53:07 myclasslist httpd[28471]: httpd: Syntax error on line 353 of /etc/httpd/conf/httpd.conf...nfig
Mar 01 11:53:07 myclasslist systemd[1]: httpd.service: main process exited, code=exited, status=1/FAILURE
Mar 01 11:53:07 myclasslist kill[28473]: kill: cannot find process ""
```

The bottom text is a log that the service generates. But it's just a part of whole log and also it won't be updated in realtime like `tail -f`. How can we look into the log more detail?

[`journalctl`](https://www.freedesktop.org/software/systemd/man/journalctl.html) is a utility to query the content of systemd journal. By using this you can check systemd log in the same way of `tail -f`.

```
$ journalctl -f -u <Unit Name>
```

