---
title: "When to use var in Java 10"
layout: post
date: 2020-08-01 06:44:02 +0900
image: 'assets/img/posts/2020-08-01-when-to-use-var-in-java-10/catch.jpg'
description:
tag: ['Java', 'Programming']
blog: true
author: "Kai Sasaki"
---

Java 10 officially introduced the `var` keyword to declare the local variable without typing the type information. Java developers have needed to keep typing the class name explicitly for a long time.

`var` keyword allows us to declare the local variable without type information supported by the power of type inference of Java compiler. We can simplify the following code.

```java
String str = "Hello, Java!"
```

like this

```java
var str = "Hello, Java!"
```

But is it beneficial for practical use? Does it make the code better from the viewpoint of the readability and maintainability?

I have found an interesting discussion in the [Presto community](https://prestosql.slack.com/archives/CP1MUNEUX/p1596193971338400) about the `var` usage. Let me summarize the point here.

## Pros

- Speeding the type typing
  - We do not need to write the code as follows anymore.
```java
AnOverlyLengthyClassName instance = new AnOverlyLengthyClassName();
```
- Since it's just an implicit typing, we already use it in the lambda expression.
- We can avoid the trouble caused by forgetting the `L` in the long literal.
- It can have a use when we want to simplify the expression.
```java
abc = doSomething(somethingElse());
// ↓ Extracting variables
List<Map<SomeLongNameHere, List<BlahBlahBlah>>> foo = somethingElse();
abc = doSomething(foo);
```
- It encourages developers to use a more descriptive variable name like Kotlin, Scala.

## Cons
- It makes the readability worse by imposing the burden to infer the type by ourselves.
- The primary purpose of the code is readability, not the speed of typing.
- Even if we use the `var` declaration, we can save only a few characters in most cases.
- Although we can check the actual type by jumping the code with IDE, we cannot do that in GitHub.

Overall, the Presto community does not prefer using the `var` for now. That's pretty reasonable. From my experience, the `var` usage did not improve the readability even though it could worsen it. Thanks to the power of IDE (e.g. [IntelliJ IDEA](https://www.jetbrains.com/idea/)), it would not be much trouble to type lengthy class name in Java anymore.

Therefore, we may need to be careful to use the `var` declaration in general. If we are sure to simplify the expression by eliminating the tiring generic type declaration (See 4th item in Pros), there might be room to use it.

I am also interested in how the other Java community treats the `var` usage in their project.

## Reference

- [Finally, Java 10 Has var to Declare Local Variables](https://dzone.com/articles/finally-java-10-has-var-to-declare-local-variables)
- [Presto Slack](https://prestosql.slack.com/archives/CP1MUNEUX/p1596193971338400)
