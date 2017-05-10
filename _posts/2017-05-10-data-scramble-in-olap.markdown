---
title: "Data Scramble in OLAP"
layout: post
date: 2017-05-10 18:02:39 +0900
image: 'images/'
description:
tag: ["OLAP", "Data Scramble"]
blog: true
author: "lewuathe"
---

Data scrambling is the process to obfuscate or remove sensitive data like email address or password. This process is irreversible so that the original data cannot be derived from the scrambled data. Data scrambling can be utilized only during the cloning process. So there are two key points in data scrambling I think.

1. Unable to read original data
2. Not to lost the characteristics of original data

It is difficult to achieve point 2. without failing to do 1. Point 2 is important especially for OLAP tool. Since OLAP tool often extracts the statistics of original data such as sum, average, we don't want to change these type of information so much. For example assuming we have below table.

|name|email|age|
|:----|:----|:----|
|Kai Sasaki|kai@example.com|27|
|Takeshi Goda|takeshi@goda.ne.jp|12|
|Suneo Honekawa|sune@gmail.com|12|
|Nobita Nobi|nobi@nobinobi.com|12|
|Doraemon|dora@yaki.com|88|
|Doraemon|dora2@yahoo.co.jp|88|
|Shizuka Minamoto|oshizu@yahoo.co.jp|12|

How can we do data scrambling? The good example I thought is


|col1|col2|col3|
|:----|:----|:----|
|aa|aa@example.com|1|
|ab|ab@example.com|2|
|ac|ac@example.com|2|
|ad|ad@example.com|2|
|ae|ae@example.com|3|
|ae|be@example.com|3|
|af|af@example.com|2|

It keeps for example cardinality with original data. (But does not average or other statistics). How can we achieve this type of **good data scrambling**? I'm now investigating the algorithm and tools to be used.
