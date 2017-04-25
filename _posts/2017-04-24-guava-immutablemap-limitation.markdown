---
title: "Guava ImmutableMap (implicit?) limitation"
layout: post
date: 2017-04-24 17:25:22 +0900
image: 'images/'
description:
tag: ["Java", "Guava"]
blog: true
author: "lewuathe"
---

Following the last time, I found a new trivial thing about Guava usage. [ImmutableList](https://google.github.io/guava/releases/snapshot/api/docs/com/google/common/collect/ImmutableList.html) creates the List which is immutable for you. You can create any length list by using [of](https://google.github.io/guava/releases/snapshot/api/docs/com/google/common/collect/ImmutableList.html#of-E-E-E-E-E-E-E-E-E-E-E-E-E...-) method. So I thought I can any length ImmutableMap with this analogy.

```java
import com.google.common.collect.ImmutableMap;

Map<String, String> l = ImmutableMap.of(
        "k1", "v1",
        "k2", "v2",
        "k3", "v3",
        "k4", "v4",
        "k5", "v5",
        "k6", "v6"
);
```

But this code cannot be compiled because [ImmutableMap.of](https://google.github.io/guava/releases/snapshot/api/docs/com/google/common/collect/ImmutableMap.html#of-K-V-K-V-K-V-K-V-K-V-) method receives at most 5 elements unlike `ImmutableList`.

```
[ERROR] /Users/sasakikai/dev/javaspike/src/test/java/com/lewuathe/TestGuava.java:[52,45] no suitable method found for of(java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String,java.lang.String)
    method com.google.common.collect.ImmutableMap.<K,V>of() is not applicable
      (cannot infer type-variable(s) K,V
        (actual and formal argument lists differ in length))
    method com.google.common.collect.ImmutableMap.<K,V>of(K,V) is not applicable
      (cannot infer type-variable(s) K,V
        (actual and formal argument lists differ in length))
    method com.google.common.collect.ImmutableMap.<K,V>of(K,V,K,V) is not applicable
      (cannot infer type-variable(s) K,V
        (actual and formal argument lists differ in length))
    method com.google.common.collect.ImmutableMap.<K,V>of(K,V,K,V,K,V) is not applicable
      (cannot infer type-variable(s) K,V
        (actual and formal argument lists differ in length))
    method com.google.common.collect.ImmutableMap.<K,V>of(K,V,K,V,K,V,K,V) is not applicable
      (cannot infer type-variable(s) K,V
        (actual and formal argument lists differ in length))
    method com.google.common.collect.ImmutableMap.<K,V>of(K,V,K,V,K,V,K,V,K,V) is not applicable
      (cannot infer type-variable(s) K,V
        (actual and formal argument lists differ in length))
```

Then how can we create arbitrary length ImmutableMap? You can use [ImmutableMap.Builder](https://google.github.io/guava/releases/snapshot/api/docs/com/google/common/collect/ImmutableMap.Builder.html).


```java
Map<String, String> l = ImmutableMap.<String, String>builder()
    .put("k1", "v1")
    .put("k2", "v2")
    .put("k3", "v3")
    .put("k4", "v4")
    .put("k5", "v5")
    .put("k6", "v6")
    .put("k7", "v7")
    .build();
```

You can the map which has more than 5 elements.
