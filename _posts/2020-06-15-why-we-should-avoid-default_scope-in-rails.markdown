---
title: "Why we should avoid default_scope in Rails"
layout: post
date: 2020-06-15 22:18:05 +0900
image: 'assets/img/posts/2020-06-15-why-we-should-avoid-default_scope-in-rails/catch.png'
description:
tag: ['Rails', 'Practice']
blog: true
author: "Kai Sasaki"
---

ActiveRecord in Rails provides a way called [`scope`](https://guides.rubyonrails.org/active_record_querying.html#scopes) to keep the readability along with encapsulating the detail of the business logic in the model class. It enables us to add a more intuitive interface to the model so that we can quickly call the scoped method without caring about the complicated underlying implementation. This also contributes to achieving the well-known good practice in the MVC model, [**"Fat Model, Skinny Controller"**](https://riptutorial.com/ruby-on-rails/example/9609/fat-model--skinny-controller). It shows us the clear guidance saying, "We should not write non-response related logic in the controller". If you are writing a complicated logic that is not directly related to the HTTP response construction response, that should go to the model, not controller. `scope` methods are helpful to materialize this goal.

## What is `default_scope`?

As part of the scope feature, ActiveModel has a `default_scope` which defines the scope method applied to all queries on the model. Let's say we have a `User` model as follows.

```ruby
class User < ActiveRecord::Base
end
```

`User.all` returns all users as it states. But what if you want to get the users excluding all hidden users. The following code will return the results as you expected.

```ruby
User.where(hidden: false)
```

But `default_scope` will provide a more convincing manner.

```ruby
class User < ActiveRecord::Base
  default_scope { where(hidden: false) }
end
```

This `default_scope` is always applied to the model query. In other words, you do not need to specify the query explicitly anymore.

```ruby
User.all # It will return the visible users, excluding hidden ones.
```

That is good. You do not need to specify the same where conditions many times. `default_scope` automatically creates the basis of all queries.

Practically, `default_scope` is often not recommended in Rails.

## Implicit Behavior Change

Based on my experience, the biggest problem of the `default_scope` is applied implicitly. If the writer of the `default_scope` is different from the model user, the behavior must look weird. Model users will see a query they do not write unexpectedly. Implicit behavior change is generally anti-pattern. (In Scala, [even the compiler shows the warning for the `implicit` type conversion.](https://docs.scala-lang.org/tour/implicit-conversions.html)).

In my case, I have developed one API using the model class, which is derived from the original web application. Since the data source is shared with them, it is useful to share the model class too. But it brings unexpected pitfall caused by `default_scope`. At some time, another developer introduced the following `default_scope`.

```ruby
class OriginalClass < ActiveRecord::Base
  default_scope { select(all_columns) }
end
```

An application I have developed is using the class. What I want here are only `c1`, `c2`, and `c3`. Returning all columns can cause the problem.

```ruby
OrignalClass.where("c1 = xxx").select("c1, c2, c3")
```

As you imagine, introducing the `default_scope` here makes it happen. Without any notice, all columns are returned because I do not know the change around the default behavior of the `OriginalClass`.

Implicit behavior change is always requiring intensive care. All developers touching the codebase and related repository need to be careful of the transformation of the behavior. But we must not expect all members to do so. It's unrealistic.

## Use `scope`, not `default_scope`

Here is a simple answer. Use `scope`, not `default_scope`. What we want to do was completely achieved by `scope`. There was no special reason to use `default_scope`.

```ruby
class OriginalClass < ActiveRecord::Base
  scope, get_all_columns -> { select(all_columns) }
end
```

Using `scope` does not break any user codebase implicitly. If a user wants to make use of this new scope, call it explicitly. Of course, `default_scope` can reduce the amount of code you need to write in terms of the number of characters. But the damage and maintenance cost will surpass the benefit obtained by the `default_scope`. Simply obeying the following guidance will lead you to keep the Rails code clean and more maintainable.

> Use scope, not default_scope

Thanks for reading!

## References

* [Don’t use default_scope. Ever.](https://andycroll.com/ruby/dont-use-default-scope/)
* [Why is using the rails default_scope often recommend against?](https://stackoverflow.com/questions/25087336/why-is-using-the-rails-default-scope-often-recommend-against)