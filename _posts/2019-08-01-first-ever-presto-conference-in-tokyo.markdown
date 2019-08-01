---
title: "First Ever Presto Conference in Tokyo"
layout: post
date: 2019-08-01 12:07:34 +0900
image: 'assets/img/posts/2019-08-01-first-ever-presto-conference-in-tokyo/overall-view.jpg'
description:
tag: ['Presto', 'Conference']
blog: true
author: "Kai Sasaki"
---

In the last month, we have held a Presto conference in Tokyo at our office. That is the first-ever Presto conference gathering Presto developers in the Japanese community. While I've written a report in the official blog of [prestosql.io](https://prestosql.io/blog/2019/07/11/report-for-presto-conference-tokyo.html), I neglected to write down my thought on this blog.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 140px; padding-bottom: 0;"><a href="https://prestosql.io/blog/2019/07/11/report-for-presto-conference-tokyo.html" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fprestosql.io%2Fblog%2F2019%2F07%2F11%2Freport-for-presto-conference-tokyo.html&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

This is the article to describe the impression I had at the conference.

## Usability of Presto

One of the biggest surprises I had at the conference was the enthusiasm maintainers have to keep the usability of Presto. As the user may already know, the error message Presto throws is comprehensive and straightforward so that users can quickly detect the cause of the error. Presto maintainers keep the quality of codebase by intensively reviewing the pull requests from the viewpoint of the usability. Their experience gave them a lesson about the importance of the usability of the database system. Thanks to their effort and design decision, we can benefit from it.

## Effort of Migration from Hive

Hive and Presto are an entirely different system. Their SQL syntax is different, which often causes the challenge in terms of the compatibility between two systems. Our Treasure Data uses Hive and Presto as our data processing engine. Thus, the experience of Star from Yahoo Japan was exciting to me.

<div style='text-align: center;'>
<iframe src="//www.slideshare.net/slideshow/embed_code/key/ld3tI0uIzAQe1" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/techblogyahoo/large-scale-migration-fromhive-to-presto-at-yahoo-japan" title="Large scale migration fromHive to Presto at Yahoo! JAPAN" target="_blank">Large scale migration fromHive to Presto at Yahoo! JAPAN</a> </strong> from <strong><a href="https://www.slideshare.net/techblogyahoo" target="_blank">Yahoo!デベロッパーネットワーク</a></strong> </div>
</div>

We can imagine the trouble to convert the existing queries into the format compatible with Presto. One of the best things I could know was they had a plan to make the tool for converting the query open. It enables us to migrate existing Hive queries to Presto more quickly and easily.

## Presto is Fast

AS there are many developers and users in the Presto community, there are also many use cases, and requirements turned toward Presto. But maintainers rarely hear the dissatisfaction of Presto performance. Most users are satisfied with the performance. Considering my experience, Presto can provide the best performance in any query processing engines, which is open-sourced. That is indeed a great thing. A few years ago, quite many people tried to find a high-performance query engine system. Presto was just a candidate of them. Now using Presto as a productionized query processing engine is considered promising. We can say it is the best choice without any doubt.

# Wrap Up

Presto software foundation is now actively working on creating a chance to gather developers and have a conversation with the community. You can check the detail in [the community blog](https://prestosql.io/blog/).

Thanks!