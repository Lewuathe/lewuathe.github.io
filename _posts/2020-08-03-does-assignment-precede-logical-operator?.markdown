---
title: "Does assignment precede logical operator?"
layout: post
date: 2020-08-03 20:52:42 +0900
image: 'assets/img/posts/2020-08-03-does-assignment-precede-logical-operator?/catch.jpg'
description:
tag: ['Ruby', 'Programming']
blog: true
author: "Kai Sasaki"
---


I have encountered a weird situation while I'm writing a piece of code in Ruby. Here is the sample code extracting the essence of the problem I have faced. First, I tried to get the matching result with a line of code as follows.

```ruby
p1 = /hello/
p2 = /world/

s = "hello, world"

if m1 = s.match(p1) || m2 = s.match(p2)
    puts "m1=#{m1}"
    puts "m2=#{m2}"
end
`"

It shows:

`"
m1=hello
m2=
`"

Oops, I forgot that the logical operator `||` does the short-circuit evaluation. It makes `m2` nil. What I wanted to do was checking both regular expressions are matching with the given string. Here is the correct one.

```ruby
if m1 = s.match(p1) && m2 = s.match(p2)
    puts "m1=#{m1}"
    puts "m2=#{m2}"
end
```

But it shows:

```
m1=world
m2=world
```

Hmm, the result was unexpected. Why is `m1` assigned by the outcome of `p2` pattern? I expected that the result of the matching of `p1` pattern is assigned to `m1` and so forth for `m2`. Is the precedence of the operators correctly working?

According to [the Ruby operator precedence](https://www.oreilly.com/library/view/the-ruby-programming/9780596516178/ch04s06.html#:~:text=The%20associativity%20of%20an%20operator,appear%20sequentially%20in%20an%20expression.&text=The%20value%20%E2%80%9CL%E2%80%9D%20means%20that,evaluated%20from%20right%20to%20left.), the logical operator `&&` precedes the assignment operator `=`. Therefore, the evaluation order of the previous code should be same as:

```ruby
if (m1 = s.match(p1)) && (m2 = s.match(p2))
    puts "m1=#{m1}"
    puts "m2=#{m2}"
end
```

Obviously, its outcome is expected.

```
m1=hello
m2=world
```

In reality, the evaluation looks like:

```ruby
if m1 = (s.match(p1) && m2 = s.match(p2))
    puts "m1=#{m1}"
    puts "m2=#{m2}"
end
```

The logical operator follows the assignment to `m2`.

Since the result seems weird and I'm still not sure the mechanism behind this behavior, I posted one question in [StackOverflow](https://stackoverflow.com/questions/63228851/exception-of-operator-precedence-in-ruby)

I would very much appreciate it if you could find the answer to this problem. Thanks!

## Reference

- [Operators - The Ruby Programming Language](https://www.oreilly.com/library/view/the-ruby-programming/9780596516178/ch04s06.html#%3A~%3Atext%3DThe%20associativity%20of%20an%20operator%2Cappear%20sequentially%20in%20an%20expression.%26text%3DThe%20value%20%E2%80%9CL%E2%80%9D%20means%20that%2Cevaluated%20from%20right%20to%20left.)
- [Does assignment precede logical operator in Ruby?](https://stackoverflow.com/questions/63228851/exception-of-operator-precedence-in-ruby)