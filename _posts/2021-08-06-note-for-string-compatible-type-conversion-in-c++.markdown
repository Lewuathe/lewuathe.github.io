---
title: "Note for string compatible type conversion in C++"
layout: post
date: 2021-08-06 15:51:15 +0900
image: 'assets/img/posts/2021-08-06-note-for-string-compatible-type-conversion-in-c++/catch.jpg'
description:
tag: ['C++', 'Programming']
blog: true
author: "Kai Sasaki"
---

Type conversion can be the most googled material in daily programming regardless of the kind of language. That is also the case when writing C++ code. For example, I often forget how to convert the `std::string` to `char *` and vice versa. [`llvm::StringRef`](https://llvm.org/doxygen/classllvm_1_1StringRef.html) brings additional complexity definitely into this conversion graph between string compatible types in C++.

This article is a brief note on how to move back and forward among these three data types so that we can later refer to them as necessary.

## `std::string` -> `char *`

It's pretty simple. `std::string` has a method to return the pointer to the underlying character entities. `c_str()` allows us to do so.

```c++
std::string str = "Hello, World";
const char *c = str.c_str();
```

## `char *` -> `std::string`

`std::string` has a constructor that takes the `const char*` type. Thus, it enables you to create `std::string` from the `char *` type.

```c++
const char *c = "Hello, World";
std::string str(c);
```

## `llvm::StringRef` -> `std::string`

`llvm::StringRef` has a method to return the string entity, `str()`.

```cpp
llvm::StringRef stringRef("Hello, World");
std::string str = stringRef.str();
```

## `llvm::StringRef` -> `char *`

`llvm::StringRef` has a method to return the underlying data pointer. `data()` method will do that.

```c++
llvm::StringRef stringRef("Hello, World");
const char *c = stringRef.data();
```

```cpp
llvm::StringRef stringRef("Hello, World");
std::string str = stringRef.str();
```

## `std::string`, `char *` -> `llvm::StringRef`

We can construct `llvm::StringRef` from both types of `std::string` and `char *` by its constructor.

```c++
std::string str = "Hello, String";
const char *c = "Hello, Char";
llvm::StringRef stringRef1(str);
llvm::StringRef stringRef2(c);
```

# Reference

- [std::string to char*](https://stackoverflow.com/questions/7352099/stdstring-to-char/7352131)
- [convert a char* to string](https://www.cplusplus.com/forum/general/41912/)
- [llvm::StringRef.str()](https://llvm.org/doxygen/classllvm_1_1StringRef.html#ae2338e6739b671ea853b6154db368292)
- [llvm::StringRef.data()](https://llvm.org/doxygen/classllvm_1_1StringRef.html#a3f9da404542bd67dea461bdda340d91d)


