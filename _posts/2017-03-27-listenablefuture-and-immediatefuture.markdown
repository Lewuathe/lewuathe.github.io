---
title: "ListenableFuture and immediateFuture"
layout: post
date: 2017-03-27 21:48:26 +0900
image: 'images/'
description:
tag: ["Java", "Guava", "Future"]
blog: true
jemoji:
author: "lewuathe"
---

[ListenableFuture](https://github.com/google/guava/wiki/ListenableFutureExplained) is a `Future` interface implementation in [Google Guava](https://github.com/google/guava) library. Since it has compatibility with `Future`, you can replace `Future` with `ListenableFuture`. `ListenableFuture` provides a mechanism of lister callback in addition features of `Future`. The result of `Future` should be fetched by main thread later but `ListenableFuture` call the callback when it finishes the calculation.

```java
// ExecutorService especially for ListenableFuture
ListeningExecutorService service
  = MoreExecutors.listeningDecorator(Executors.newFixedThreadPool(10));

ListenableFuture<Explosion> explosion
  = service.submit(new Callable<Explosion>() {
      public Explosion call() {
        return pushBigRedButton();
      }
  });

Futures.addCallback(explosion, new FutureCallback<Explosion>() {
  // Called when succeeded
  public void onSuccess(Explosion explosion) {
    walkAwayFrom(explosion);
  }
  public void onFailure(Throwable thrown) {
    battleArchNemesis(); // escaped the explosion!
  }
});
```

Today I found a tip of migration from `CompletableFuture` to `ListenableFuture` checking [Presto commit](https://github.com/prestodb/presto/commit/681b6a970485f233c447d1f717540bb15600767b). `CompletableFuture` which returns the result immediately can be created with `java.util.concurrent.CompletableFuture.completableFuture`. On the other hand, the counterpart of `ListenableFuture` is `com.google.common.util.concurrent.Futures.immediateFuture`.

So if you want to create a `Future` which returns the result immediately (of course it is nonsense that alone), you must use corresponding static methods respectively.

```
// For CompletableFuture
completedFuture(null);

// For ListenableFuture
immediateFuture(null);
```
