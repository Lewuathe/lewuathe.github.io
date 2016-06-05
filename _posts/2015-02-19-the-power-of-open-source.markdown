---
layout: post
blog: true
title: "The Power of Open Source for a Learner"
date: 2015-02-19 22:17:15 +0900
comments: true
categories: ["OSS", "Storm"]
author: Kai Sasaki
---

Recently I often receive patches into my own latest open source software, [storm-cookbook](https://github.com/Lewuathe/storm-cookbook).
This is a simple chef cookbook which creates apache storm cluster. I wrote just for myself, my needs, my other projects.

Until now, there were some times I received patches and merged pull requests into other projects. Almost all patches were small but not trivial ones. I was so glad to receive these patches. These all experiences were great and gave me a great deal motivation for tomorrow development. With these contributions my project grow one by one and the quality is improved. It must be nice thing for users.

<div style="text-align:center">
<img src="/images/posts/2015-02-19-oss-power/review.png" alt="review"/>
</div>


<!-- more -->

However this time there were a little difference from previous experiences for me.
I was so impressed that I cannot help writing about this amazing chance to learn for me. Look these pull requests first.

[Pull Requests](https://github.com/Lewuathe/storm-cookbook/pulls?q=is%3Apr+is%3Aclosed)

These patches(but they are all big changes!) include major changes to this cookbook especially unit test and continuous integration. Test and tools for enhancement of development usually done later because these are troublesome and moreover boring.
But I am sure that these enhancements of development environment are very important when you maintain an open source software made by only a software engineer like me. In spite of this fact, I'm not willing to do this!

This time. I could receive these type of patches from [TD-4242](https://github.com/TD-4242). I have not met with him/her.
I am not familiar with him. But I can see his patches, review them and merge into my repository. Above all, he send me test codes that exactly I wanted and had to write to maintain this cookbook myself otherwise. This was very helpful to me and of course the users of
this cookbook.

In honest I had no idea how to write unit test of chef cookbooks. I am a newbie of [chef](https://www.chef.io/chef/) architecture. I could not count the times when I referred the documentation about resources, recipes and attributes.
But this time I was able to learn how to write test with his patches. What gem package do I need? How can I run unit test with Rakefile? Without these patches, it will take a lot of time to start writing unit test codes and tools. And also it might be buggy :(

**It was the first time I just realized patches were
good learning resources for even receivers of these patches.** I thought that patch reviewers should be always knowledgable than submitters. But I found that's not true. I received not only patches but also knowledges which is necessary to grade up my software skills. These are worth things I might not receive even if I pay a lot of money, but I can got for free!! That was fantastic, wasn't it?

Receiving pull requests are always fantastic things themselves because of the fact a people who are not familiar to me, who
may live in the other side of the earth tries to improve my software. This is no other than miracle not only in technology industry but also all industries we all human made.

So you have no choice not to submit patches into some libraries you always use. You have no choice not to write some libraries
which you think cool. And you have no choice not to review great patches you received just now because these are treasures which include a lot of learning resources you cannot obtain only from reading books. That's must be fun. I think this is the world our technology people want to create.

Viva learning!!
