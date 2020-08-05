---
title: "Implicit left-padding of the binary literal in Java"
layout: post
date: 2020-08-05 14:20:42 +0900
image: 'assets/img/posts/2020-08-05-implicit-sign-interpretation-of-binary-literal-in-java/catch.jpg'
description:
tag: ['Java', 'Binary', 'Programming']
blog: true
author: "Kai Sasaki"
---

Hey, this is a part of [the series](/does-assignment-precede-logical-operator.html) describing the situation where I encountered weird behavior in the programming :) Today is about Java.
When I wrote a code to do bit manipulation in Java, the unexpected outcome shows up. Unfortunately, I could not find the official specification behind this behavior. Thus this aims to get a chance to find the answer from someone who read this article.

## Masking the most significant bit

What we wanted to do was getting the most significant bit in the 2's complement format. For instance, `1111_1111` is -1 in the signed 8-bit format. To get the most significant bit in the number, we can use the mask of the signed bit.

```java
byte value = -1;
long byteSignMask = 0b1000_0000;;
assertEquals(0b1000_0000, value & byteSignMask);
```

Yes, it properly works to get only the bit representing the sign of the number. Using binary literal and shift operation, constructing the mask gives us an identical result.

```java
long byteSign1 = 1L << 7;
long byteSign2 = 0b1000_0000;

// byteSign1 = 10000000
System.out.println("byteSign1 = " + Long.toBinaryString(byteSign1));
// byteSign2 = 10000000
System.out.println("byteSign2 = " + Long.toBinaryString(byteSign2));

// OK
assertEquals(byteSign1, byteSign2);
```

But when I do the same thing for integer, it does not work.

## Implicit padding

The following code works correctly as well as the previous example.

```java
long value = -1;
long intSignMask = 0b1000_0000_0000_0000_0000_0000_0000_0000;
assertEquals(0b1000_0000_0000_0000_0000_0000_0000_0000, value & intSignMask);
```

Okay, let me check the mask is the same with `1L << 31`.

```java
long intSign1 = 1L << 31;
long intSign2 = 0b1000_0000_0000_0000_0000_0000_0000_0000;

// intSign1 = 10000000000000000000000000000000
System.out.println("intSign1 = " + Long.toBinaryString(intSign1));
// intSign2 = 1111111111111111111111111111111110000000000000000000000000000000
System.out.println("intSign2 = " + Long.toBinaryString(intSign2));

// Fail: expected:<2147483648> but was:<-2147483648>
assertEquals(intSign1, intSign2);
```

It's interesting. Why is the mask constructed by the shift operation `1L << 31` results in a different outcome from the binary literal? Why is the binary literal automatically left-padded with 1?
I asked in the [StackOverflow](https://stackoverflow.com/questions/63259242/implicit-left-padding-of-the-binary-literal-in-java) as before to get the answer. Please let me know if you an explanation for it.

Thanks.

## Reference
- [Implicit left-padding of the binary literal in Java](https://stackoverflow.com/questions/63259242/implicit-left-padding-of-the-binary-literal-in-java)
- [Java Binary Literals](https://docs.oracle.com/javase/8/docs/technotes/guides/language/binary-literals.html)

