---
layout: post
blog: true
title: "Split string in Java"
date: 2015-06-01 21:56:35 +0900
comments: true
categories: ["Java"]
author: Kai Sasaki
---

There are a lot of time to split string type when you are writing program. Of course in Java. Although I already know `split` method in `String` can be applied to this case, I misunderstood how to use it. My initial code is below.

<!-- more -->

```java
public class Split {
    public static void main(String[] args) {
        String s = "foo.bar";
        System.out.println(s.split(".")[0]);
        System.out.println(s.split(".")[1]);
    }
}
```

And running this threw such exception.

```
$ java Split
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: 0
    at Split.main(Split.java:4)
```

It looks split method does not work properly. What happend? The answer is in javadoc about String.

[String#split](http://docs.oracle.com/javase/7/docs/api/java/lang/String.html#split(java.lang.String))

`String#split` must receive **regex** type as String. So in this case "." interpreted as "Match any one character" in regular expression context. I had to write argument as "Only dot character" when passes to split method. I rewritten it.

```java
public class Split {
    public static void main(String[] args) {
        String s = "foo.bar";
        System.out.println(s.split("\\.")[0]);
        System.out.println(s.split("\\.")[1]);
    }
}
```

```
$ java Split
foo
bar
```

Yes. It's working now. I learned javadoc is one of the most useful resource to all java developers. I want to be not reluctant to look into official documents such as javadoc of JDK from now.

Thank you.





