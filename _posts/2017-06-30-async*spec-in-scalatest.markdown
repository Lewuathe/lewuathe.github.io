---
title: "Async*Spec in Scalatest"
layout: post
date: 2017-06-30 20:58:58 +0900
image: 'images/'
description:
tag: ["Scala", "Future"]
blog: true
author: "lewuathe"
---

When I wrote a test for Finagle, I found it didn't work as expected. Scalatest didn't check assertion properly asynchronously like `Future`.

From Scalatest 3.0, we can test in async style. It means we can assert the result returned from `Future`. There are some abstract classes for the purpose. [AsyncWordSpec](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncWordSpec), [AsyncFunSuite](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFunSuite), [AsyncFunSpec](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFunSpec),
[AsyncFlatSpec](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFlatSpec),
[AsyncFreeSpec](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFreeSpec),
[AsyncFeatureSpec](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFeatureSpec).

Suites in these spec classes must return `Future[Assertion]`. Trait versions are also provides.
[AsyncWordSpecLike](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncWordSpecLike), [AsyncFunSuiteLike](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFunSuiteLike), [AsyncFunSpecLike](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFunSpecLike),
[AsyncFlatSpecLike](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFlatSpecLike),
[AsyncFreeSpecLike](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFreeSpecLike),
[AsyncFeatureSpecLike](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.AsyncFeatureSpecLike).

The usage can be like this. This is the example of `AsyncWordSpec`.

```scala
import scala.concurrent.{Future, Promise}

import org.scalatest.AsyncWordSpec

import com.twitter.finagle.Service
import com.twitter.finagle.http.{Request, Response, Status}
import com.twitter.util.{Future => TwitterFuture, Return, Throw}

class MyAsyncTest extends AsyncWordSpec {
  // Async*Spec is not work with Twitter util Future
  implicit def fromTwitter[A](twitterFuture: TwitterFuture[A]): Future[A] = {
    val promise = Promise[A]()
    twitterFuture respond {
      case Return(a) => promise success a
      case Throw(e) => promise failure e
    }
    promise.future
  }

  "A Server" should {
    "return 404" in {
      val req = Request("http://example.com")
      val res = client(req) // res is Future[Response]
      res.map { r => assert(r.status == Status.NotFound) }
    }
  }
}
```

There are two points to be noted. One is about assertion. We need to write assertion inside the code after result is obtained.

The next one is `Future` type. Finable is using its own `Future` utility, `com.twitter.util.Future`. Scalatest Async*Spec cannot recognize that class. So we need to convert them into `scala.concurrent.Future`. In this case, I implemented a implicit method for implicit conversion.

```scala
implicit def fromTwitter[A](twitterFuture: TwitterFuture[A]): Future[A] = {
  val promise = Promise[A]()
  twitterFuture respond {
    case Return(a) => promise success a
    case Throw(e) => promise failure e
  }
  promise.future
}
```

So Scala compiler convert `TwitterFuture` into `Future` if necessary.

## Reference

* [Scalatest 3 Scaladoc](http://doc.scalatest.org/3.0.0/index.html#package)
* [What's new in Scalatest 3](http://tudorzgureanu.com/whats-new-in-scalatest-3/)
