---
layout: post
blog: true
title: "Parse API migration test tool"
date: 2016-02-15 19:10:57 +0900
comments: true
categories: ["parse", "migration"]
author: Kai Sasaki
---

I participated into [HackDay 2016](http://hackday.jp/) that is held by Yahoo Japan Corporation with my friend.
Every time I attended, we develop a tool for ourselves not for users. Because I'm sure it can make the world better.
In addition, it provides us new skill as a software engineer. That was fun time.

<!-- more -->

We wrote a tool and patch for migration from [Parse.com](http://parse.com/) that has just announced to be closed.
A lot of mobile developers seems to use Parse.com for their services. What we have done in the hackathon were here.

* Write spec tool for API and data migration from Parse.com. We published it as [parse-spec](https://www.npmjs.com/package/parse-spec).
* Write a patch for implementing missing features, Cloud code job execution. [#PR398](https://github.com/ParsePlatform/parse-server/pull/398).
* Fix [a compatibility issue](https://github.com/ParsePlatform/parse-server/pull/397) for default configuration between parse-server and Parse.com.

We hope these patches will be merged into master because it will make our migration easier and of course your migration too.
So please send a feedback about the PRs or [parse-spec](https://www.npmjs.com/package/parse-spec) if you have some interest.
We are sure to these simple tools can make our migration simple and easier.

Thanks!
