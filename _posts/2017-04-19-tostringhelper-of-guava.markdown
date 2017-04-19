---
title: "ToStringHelper of Guava"
layout: post
date: 2017-04-19 18:57:38 +0900
image: 'images/'
description:
tag: ["Java", "Guava"]
blog: true
author: "lewuathe"
---

In Java, [`toString()`](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html#toString--) method is useful for debugging. It can print the object information in human readable format. Member variables and state can be returned. Only painful stuff of `toString()` is that
we need to implement by ourselves for custom class.

```java
class User {
  private final String name;
  private final int    age;

  public User(String name, int age) {
    this.name = name;
    this.age  = age;
  }

  @Override
  public String toString() {
    return "User{name=" + name + ",age=" + age + "}"
  }
}
```

Formatting the string returned by `toString()` is painful. So [`MoreObjects.ToStringHelper`](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/base/MoreObjects.ToStringHelper.html) is the one to be used.

It simply creates the readable formatted string given properties. It's easy to use.

```java
  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
      .add("name", name)
      .add("age", age)
      .toString();
  }
```

It just prints like this.

```
User{name=Kai, age=27}
```
