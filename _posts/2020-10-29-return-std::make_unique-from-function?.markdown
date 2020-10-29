---
title: "Return std::make_unique from function?"
layout: post
date: 2020-10-29 17:16:13 +0900
image: 'assets/img/posts/2020-10-29-return-std::make_unique-from-function?/catch.jpg'
description:
tag: ['cpp', 'c++', 'copy', 'programming']
blog: true
author: "Kai Sasaki"
---

If you are an expert in modern C++, you must be familiar with the move semantics of C++. Move semantics provides us a chance to improve the performance by eliminating the unnecessary copy of the object, introduced in [C++11](https://www.cprogramming.com/c++11/rvalue-references-and-move-semantics-in-c++11.html). If your code contains a large object and sees the time when it's copied often, it's worth considering it.

Additionally, you may also be familiar with the smart pointer of C++. `std::unique_ptr` is a type of smart pointer. It prohibits the programmer from copying the pointer so that we can keep the ownership semantics clear. If we change the ownership of the object, move semantics will come into your scope. Generally, you can write the following code.

```cpp
class A {}

std::unique_ptr<A> a1 = std::make_unique<A>();

std::unique_ptr<A> a2 = a1; // Compilation error

std::unique_ptr<A> a3 = std::move(a1); // OK
```

It clarifies **we are never able to copy the `std::unique_ptr`**.

# Returning unique pointer from a function?

But I have found the following code passed the compile.

```cpp
class A {}

std::unique_ptr<A> f() {
  return std::make_unique<A>();
}

std::unique_ptr<A> a = f();
```

Hmm, if I remember correctly, a function in C++ returns a copy of the returned object. A function `f` returns a copy of `std::unique_ptr` constructed by `std::make_unique`. How is it possible?

# Copy Elision

[This stackoverflow](https://stackoverflow.com/questions/4316727/returning-unique-ptr-from-functions) answers my question.

C++ seems to have a specification to define the case where we can omit the copy operation. According to that,

> When certain criteria are met, an implementation is allowed to omit the copy/move construction of a class object [...] This elision of copy/move operations, called copy elision, is permitted [...] in a return statement in a function with a class return type, when the expression is the name of a non-volatile automatic object with the same cv-unqualified type as the function return type [...]
>
> When the criteria for elision of a copy operation are met and the object to be copied is designated by an lvalue, overload resolution to select the constructor for the copy is first performed as if the object were designated by an rvalue.

So the compiler is allowed to omit the copy operation for this particular case. In short, **if the returned value is non-volatile (which is expected to have no side-effect) and local variable**, a compiler can safely omit the copy operation. This rule seems to be applied to the case returning `std::unique_ptr`.

To fully understand the detail of the rule, we need to dig deeper into the specification of C++. But I'll stop around here. The lesson I've got so far is **there is an official rule to allow us to return `std::unique_ptr` from function**. That's enough for a typical developer like me :)


# Reference

- [Copy Elision](https://en.cppreference.com/w/cpp/language/copy_elision)
- [Returning unique_ptr from functions](https://stackoverflow.com/questions/4316727/returning-unique-ptr-from-functions)
- [How does returning std::make_unique\<SubClass\> work?](https://stackoverflow.com/questions/39478956/how-does-returning-stdmake-uniquesubclass-work/39479117#:~:text=The%20reason%20you%20can%20return,from%20one%20to%20the%20other.&text=Since%20the%20value%20returned%20from,return%20value%20is%20move%2Dconstructed.)
