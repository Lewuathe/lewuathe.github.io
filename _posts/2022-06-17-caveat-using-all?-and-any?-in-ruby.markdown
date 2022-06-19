---
title: "Caveat using all? and any? in Ruby"
layout: post
date: 2022-06-17 11:09:10 +0900
image: 'assets/img/posts/2022-06-17-caveat-using-all?-and-any?-in-ruby/catch.jpg'
description:
tag: ['Ruby']
blog: true
author: "Kai Sasaki"
---

There are always several pitfalls in writing a code, regardless of its difficulty. Developers are likely to get into trouble for several hours or more. This time I will briefly describe the situation where I've got stuck due to a lack of recognition of the short-circuit evaluation semantics provided by [all?](https://apidock.com/ruby/Enumerable/all%3F) and [any?](https://apidock.com/ruby/Enumerable/any%3F) in Ruby.

## What is short-circuit evaluation?

The short answer is [here](https://en.wikipedia.org/wiki/Short-circuit_evaluation). It is semantic for a kind of optimization. We only evaluate the second argument of the boolean expression only if the first argument does not enough to provide the total value of the expression. For example, let's say we have the following boolean expression.

```ruby
a && b
```

We do not need to evaluate the variable `b` if `a' is false because we can know the overall final value is false without `b`.

But what if `a` and `b` have side effects, respectively? We want to make sure to execute the result of side effects. That happened when I used the `all?` method in Ruby.

```ruby
my_models = [...]

if my_models.all?(&:valid?)
  puts "All okay."
else
  puts "Someone is not okay."
end
```

I wanted to collect all models' errors in `my_models` so that users can see all possible errors at once. `valid?` allows us to accumulate validation errors in the model. But `all?` stops executing `valid?` if some models are already invalid. So we need to rewrite the code like this.

```ruby
my_models = [...]
all_validity = my_models.map(&:valid?)

if all_validity.all?
  puts "All okay."
else
  puts "Someone is not okay."
end
```

This is a simple problem, and well experienced Ruby developer may not have made such a mistake. I hope this caveat may help someone who accidentally forgets the short-circuit semantics when writing the code.




