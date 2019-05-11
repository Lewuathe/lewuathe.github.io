---
title: "Bitshift to 64 bit in Java"
layout: post
date: 2019-05-11 09:03:15 +0900
image: 'assets/img/posts/2019-05-11-bitshift-to-64-bit-in-java/catch.png'
description: 
tag: ['Java', 'Programming', 'Algorithm']
blog: true
author: "Kai Sasaki"
---

Bitwise operation sometimes looks like magic. There is a bunch of sophisticated techniques to manipulate the value at the bit level.
Bit shift operation is one of these operations. You can shift the bit sequence of the given value by using shift operators which are commonly described as `>>` or `<<` in many programming languages. But do you know what happens if you shift the value beyond the length the type of the value in Java?

Let's say we want to shift the given long value with 64 bit.

```java
long num = 1;
long shift = 63;

System.out.println(Long.toBinaryString(num));
System.out.println(Long.toBinaryString(num << shift));

// 1
// 1000000000000000000000000000000000000000000000000000000000000000
```

Yes, it's working fine. The shifted area is padded with zero value. How about shifting 64 bit?

```java
long num = 1;
long shift = 64;

System.out.println(Long.toBinaryString(num));
System.out.println(Long.toBinaryString(num << shift));

// 1
// 1
```

Umm, it's a different result from what I expected. I thought we will get zero by shifting 64 bit because all shifted are padded with zero and only one bit will be thrown away. What's happening?

I found an answer [StackOverflow](https://stackoverflow.com/questions/43763619/bitshift-to-64th-bit-in-java) as usual.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 140px; padding-bottom: 0;"><a href="https://stackoverflow.com/questions/43763619/bitshift-to-64th-bit-in-java" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F43763619%2Fbitshift-to-64th-bit-in-java&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

> Java will shift by num % sizeof(datatype) only, i.e. if you shift an int by 32 it will effectively be no shift at all. If you shift by 33 the effective shift will be 33 % 32 = 1.

The size of the long type is 64 bits so that it does not have any effect on the result by shifting 64 bit. Actually, the specific error message is shown by my IDE. We should shift the long value over 64 bit in general.

![error](assets/img/posts/2019-05-11-bitshift-to-64-bit-in-java/error.png)

So please make sure to shift the value within the size of the data type in Java.