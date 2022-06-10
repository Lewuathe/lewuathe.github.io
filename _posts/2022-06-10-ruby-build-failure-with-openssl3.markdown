---
title: "Ruby Build Failure with OpenSSL3"
layout: post
date: 2022-06-10 09:42:44 +0900
image: 'assets/img/posts/2022-06-10-ruby-build-failure-with-openssl3/catch.jpg'
description:
tag: ['Rails', 'Ruby', 'OpenSSL']
blog: true
author: "Kai Sasaki"
---

There may be no developer who has not encountered installation errors when using Ruby and [rbenv](https://github.com/rbenv/rbenv). As a piece of evidence that Ruby and OpenSSL have bad chemistry with each other, you may be able to find a lot of questions line about the error like [this](https://github.com/rbenv/ruby-build/issues/1353).

This time, I tried to upgrade my Ruby environment to Ruby3 and encountered the following [issue](https://github.com/puma/puma/issues/2790).

```
OpenSSL 3 - symbol not found in flat namespace '_SSL_get1_peer_certificate'
```

This is because OpenSSL 3 has `SSL_get1_peer_certificate` but Open SSL 1.1 does not, which has `SSL_get_peer_certificate` instead. When you build Ruby with OpenSSL 1.1 but puma running for Rails using Open SSL 3, the problem shows up.

This solution targets the developer using macOS and Homebrew to manage their system packages.

# Short Answer

The quick answer to this problem is deleting OpenSSL 3 from your environment. If you use macOS and Homebrew, you will find which version is installed.

```bash
$ brew --prefix openssl
/usr/local/opt/openssl@3
```

It indicates that the system, including puma, can refer to OpenSSL 3. It might be better to uninstall this version completely. You may imagine changing the build option to compile puma with OpenSSL 1 can work.

```
$ bundle config build.puma \
    --with-opt-include=/usr/local/opt/openssl@1.1/include
```

But it did not work in my case. Eradicating the package from the system was the sole solution.






