---
title: "Simple side effect by forEach in Java 8"
layout: post
date: 2017-07-07 21:59:46 +0900
image: 'images/'
description:
tag: ["Java", "Stream"]
blog: true
author: "lewuathe"
---

As you know, Java 8 provides lambda expression and stream API. `forEach` is one of the them.

```java
List<String> a = ImmutableList.of("a", "b", "c");

a.forEach(s -> {
	System.out.println(s);
});
```

Having side-effect in lambda expression is not recommended because it can be a hinder against thread-safe. For example we sometimes want to add elements into external variable.

```java
List<String> a = ImmutableList.of("a", "b", "c");
List<String> b = new ArrayList<String>();

a.forEach(s -> {
		b.add(s);
});
```

But I found it can be simpler by using method reference like this.

```java
List<String> a = ImmutableList.of("a", "b", "c");

List<String> b = new ArrayList<String>();
a.forEach(b::add);

Assert.assertEquals(3, b.size());
```

So method reference is a good way to be used any situation in lambda expression.

Filter.

```java
public static boolean isEven(int x) {
  return x % 2 == 0;
}

@Test
public void testFilter() {
  List<Integer> a = ImmutableList.of(1,2,3,4,5);
  List<Integer> b = a.stream()
    .filter(TestForEach::isEven)
    .collect(Collectors.toList());

  Assert.assertEquals(2, b.size());
}
```

Map.

```java
private static Integer twoTimes(int x) {
  return x * x;
}

@Test
public void testMap() {
  List<Integer> a = ImmutableList.of(1,2,3,4,5);
  List<Integer> b = a.stream()
    .map(TestForEach::twoTimes)
    .collect(Collectors.toList());

  Assert.assertEquals(Integer.valueOf(4), b.get(1));
  Assert.assertEquals(Integer.valueOf(25), b.get(4));
}
```
