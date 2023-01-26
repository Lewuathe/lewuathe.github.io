---
title: "Caching HTTPS GitHub credentials"
layout: post
date: 2023-01-24 13:34:05 +0900
image: 'assets/img/posts/2023-01-24-caching-https-github-credentials/catch.jpg'
description:
tag: ['Git', 'HTTP', 'Security']
blog: true
author: "Kai Sasaki"
---

When you try to clone the repository with HTTPS protocol, you must see the following message at least once.

```
$ git clone https://github.com/foo/bar.git
Cloning into 'bar'...
Username for 'https://github.com': xxx
```

It's easy to resolve this issue. We just put the username and the token issued in [the personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) page in the GitHub settings.

But what if you do not have any option to set the token by yourself? In a situation like using [Homebrew](https://brew.sh/) to clone the repository with HTTPS protocol?

We can cache the credentials of GitHub in Git so that we can use these credentials even if we do not have any way to control the external script execution. 

1. Please make sure to [install GitHub CLI](https://github.com/cli/cli#installation)
2. Run `gh auth login` and select HTTPS as your preferred procotol.

Now, you should be able to clone the repository with HTTPS protocol without specifying the username and personal access token explicitly. Git automatically takes care of that. 

See [the official document](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git) for more detail.