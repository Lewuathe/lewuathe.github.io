---
title: "exec format error in Docker container"
layout: post
date: 2017-08-26 09:44:36 +0900
image: 'images/'
description:
tag: ["Docker", "bash"]
blog: true
author: "lewuathe"
---

You may see such error when you launched your docker container.

```
$ docker run lewuathe/test
standard_init_linux.go:187: exec user process caused "exec format error"
```

My `Dockerfile` is this.

```
FROM ubuntu

ADD test.sh /tmp
WORKDIR /tmp

ENTRYPOINT ["./test.sh"]
```

The shell script of entry point is here.

```

#!/bin/bash

echo "This is a script"
```

Umm, there is no weird point to me. Actually the `test.sh` works as expected in host OS (macOS).

```
$ ./test.sh
This is a script
```

I tried to replace ENTRYPOINT with `/bin/bash` and execute the test script.

```
FROM ubuntu

ADD test.sh /tmp
WORKDIR /tmp

# ENTRYPOINT ["./test.sh"]
ENTRYPOINT ["/bin/bash"]
```

```
$ docker run -it lewuathe/test
root:/tmp# ls
test.sh
root:/tmp# ./test.sh
This is a script
```

Hmm, after all it works. Why cannot I launch test script from ENTRYPOINT directly.

# shebang

The root cause was shebang. Shebang (`#!/bin/bash`) should be put on **the first line** because first bytes was [checked by kernel](https://stackoverflow.com/questions/12910744/why-should-the-shebang-line-always-be-the-first-line).

So after I rewrote `test.sh` to remove first empty line, the image worked as expected.

```
#!/bin/bash

echo "This is a script"
```

But I'm still not sure why `test.sh` works in host OS or through bash in Docker container. 
