---
title: "Sign your Git commit with SSH key"
layout: post
date: 2023-01-22 13:34:31 +0900
image: 'assets/img/posts/2023-01-22-sign-your-git-commit-with-ssh-key/catch.jpg'
description:
tag: ['Git', 'Security']
blog: true
author: "Kai Sasaki"
---

I used the [GPG](https://gnupg.org/) key to sign my Git commit. This is because it's beneficial to show my commit's identity and authenticity publicly. The signed commit, appropriately associated with the email registered in GitHub, will get the verified mark in the UI.

![verified](assets/img/posts/2023-01-22-sign-your-git-commit-with-ssh-key/verified.png)

But you can use the SSH key to sign the commit alternatively. It's a better and easier way because most GitHub users already should register their SSH keys to push the code to GitHub. Therefore, we do not need to prepare another key only for signing the Git commit.

First, you tell Git to use the SSH key to sign commits and tags as a default way.

```
$ git config --global commit.gpgsign true
$ git config --global gpg.format ssh
```

Second, tet the location of the public key you are using.

```
$ git config --global user.signingkey /PATH/TO/.SSH/KEY.PUB
```

At last, please make sure to register this key as a `Signing keys` found in [the settings](https://github.com/settings/keys). I thought registering the key in `Authentication keys` would be enough, but it did not work. Check the `Signing keys` section in your GitHub account's SSH and GPG keys setting.

That's it. You will see your commit is appropriately verified when you submit some patches into GitHub next time.


See [the official document](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key) for more detail. 

To learn more about the general mechanism and usage of Git, [this book](https://amzn.to/3QYZTUt) will be helpful.
<a href="https://www.amazon.com/Version-Control-Git-Collaborative-Development/dp/1492091197?crid=34WJ3LBQPE7MF&keywords=Git&qid=1674362960&sprefix=gi%2Caps%2C246&sr=8-1&linkCode=li3&tag=lewuathe-20&linkId=2ada1985367ab6e2ad7ba531a1f1d01b&language=en_US&ref_=as_li_ss_il" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=1492091197&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=lewuathe-20&language=en_US" ></a><img src="https://ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&language=en_US&l=li3&o=1&a=1492091197" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />