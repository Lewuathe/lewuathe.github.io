---
title: "exec format error in Docker container"
layout: post
date: 2017-08-26 09:44:36 +0900
image: 'assets/img/posts/2017-08-26-exec-format-error-in-docker-container/catch.png'
description:
tag: ["Docker", "bash", "script", "Error", "Linux"]
blog: true
author: "lewuathe"
---

When you use docker, you may see such error when you launched your docker container like me.

```
$ docker run lewuathe/test
standard_init_linux.go:187: exec user process caused "exec format error"
```

I found a workaround for this now. In this post, I'll try to explain how to resolve the issue.

# Table of Contents
- Dockerfile
- shebang


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

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1521822808&asins=1521822808&linkId=72a88d2b077145c841575b87262a936f&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>
<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1617294764&asins=1617294764&linkId=f877edf94a3e3c61a630172ef0872d24&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>

A catch image came from [docker.com](https://www.docker.com/legal).
