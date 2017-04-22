---
title: "Tag of ScalaTest"
layout: post
date: 2017-04-15 23:19:29 +0900
image: 'images/'
description:
tag: ["Scala", "Test"]
blog: true
jemoji:
author: "lewuathe"
---

We often want to exclude some test cases. [ScalaTest](http://www.scalatest.org/) has `@Ignore` annotation
to exclude that test case to be run as well as [JUnit](http://junit.sourceforge.net/javadoc/org/junit/Ignore.html). But how can we include or exclude test cases in more fine-grained way?

ScalaTest provides the feature called [Tagging](http://www.scalatest.org/user_guide/tagging_your_tests). By using tagging, you can specify which test cases to be run and which are not. You can use this feature in both `FlatSpec` and `WordSpec`.

For example, assuming you want to attach a tag to some test cases to specify them as slow test, you can create your own tag as follows.

```scala
import org.scalatest.Tag
object SlowTest extends Tag("com.lewuathe.SlowTest")
```

You can use the tag in each test cases.

```scala
class SomeTest extends WordSpec {
  "A Class" should {
    "do heavy task" taggedAs(SlowTest) in {
      // Doing some heavy test
    }
  }
}
```

There might be some cases when you don't want to run these heavy test because they take a lot of time. Of course it's the best we can improve test case performance to be done in reasonable time but just excluding can be a workaround. Once you tagged them as `SlowTest` both including and excluding are easy.

Excluding

```
$ sbt "test-only -- -l com.lewuathe.SlowTest"
```

Including (just running only test cases tagged as `SlowTest`)

```
$ sbt "test-only -- -n com.lewuathe.SlowTest"
```

You can which test case to be run arbitrary by using tagging of ScalaTest.

Thanks.

### Reference

- [Tagging your tests - ScalaTest](http://www.scalatest.org/user_guide/tagging_your_tests)
- [ScalaTest 109 - Mark your tests with tags to include or exclude them](http://alvinalexander.com/scala/scalatest-mark-tests-tags-to-include-exclude-sbt)
