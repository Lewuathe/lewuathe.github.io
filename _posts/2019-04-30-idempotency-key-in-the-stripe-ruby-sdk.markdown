---
title: "Idempotency key in the Stripe Ruby SDK"
layout: post
date: 2019-04-30 07:44:34 +0900
image: 'assets/img/posts/2019-04-30-idempotency-key-in-the-stripe-ruby-sdk/catch.png'
description:
tag: ['Ruby', 'Stripe', 'Idempotency', 'SDK', 'DistributedSystem']
blog: true
author: "Kai Sasaki"
---

A system may fail anytime even while doing something should not fail. The common pattern to recover that sort of failure is retrying. While retrying is simple, it's a powerful way to make a system reliable and worth considering. Actually, many operations across the network which can fail temporarily are able to be recovered by retrying. But here is the challenge.

If an operation has a side-effect, can we safely retry the same operation twice? For example, we have an operation to charge some amount of money to the user. Let's say the central transaction system is connected with the client through an unreliable network (e.g. Internet). There is the case when the operation itself succeeds but the client sees the failure due to network connection error or timeout of long-running request. Simple retrying can cause duplicated subscriptions. It's a huge problem that must not happen as a service providing online transaction. In theory, HTTP specification [does not require the semantics of idempotency ](https://stackoverflow.com/questions/45016234/what-is-idempotency-in-http-methods) in some HTTP request such as `POST`. [In RFC7231](https://tools.ietf.org/html/rfc7231#section-4.2.2), some requests including `PUT` and `DELETE` is defined as *idempotent*.

>  A request method is considered "idempotent" if the intended effect on
   the server of multiple identical requests with that method is the same as the effect for a single such request.  Of the request methods
   defined by this specification, PUT, DELETE, and safe request methods
   are idempotent.

But as you may imagine, implementing this kind of solution is easier said than done. Making every operation with side-effect is not cost effective especially in the transaction system in the small team. Here [Stripe](https://stripe.com/) comes.

# Idempotent Request in Stripe

One thing to make the system more reliable is the idea of **idempotent request** in Stripe. It's simple. Just adding a unique key in the request, Stripe ensures to return the same request without duplicating operation. Here is the simple diagram illustrating the flow of idempotent request.

![Idempotent Request](/assets/img/posts/2019-04-30-idempotency-key-in-the-stripe-ruby-sdk/idempotent-request.png)

The client sees an error due to timeout of `req1`. It retries with an idempotency key. Please be sure to use the same key as used in the first request `req1` so that Stripe can recognize them as identical. If an operation of `req1` succeeds, Stripe can return the response that should have been returned as the first response without any actual operation. You won't see any duplicated subscriptions in Stripe. By using idempotent request, you can retry the operation without worrying about the record duplication.

The key used for an idempotent request can be attached as a header, `Idempotency-Key`. The HTTP request with the header will be looking like this.

```bash
$ curl https://api.stripe.com/v1/subscription \
  -u ... \
  -H "Idempotency-Key: XXXXXXXXXXX" \
  ...
```

If you are using Ruby SDK, how can we pass the idempotency key? The methods in Ruby SDK provides a way to set headers from the second argument of the method as follows. Stripe SDK automatically set the options in the second argument in the headers of the HTTP request.

```ruby
charge = Stripe::Subscription.create({
  cusomer: 'Customer ID',
  items: [...]
}, {
  idempotency_key: "XXXXXXXXX"
})
```

Additionally, Stripe SDK automatically retry with the idempotent key in case of a timeout-related problem or 409 conflict. See [the code](onsole.treasuredata.com) for more detail. So basically Stripe and Stripe SDK enables us to achieve more robust transactional system even with the unreliable network environment.

Thanks!

> The Stripe name and logos are trademarks or service marks of Stripe, Inc. or its affiliates in the U.S. and other countries. Other names may be trademarks of their respective owners.
