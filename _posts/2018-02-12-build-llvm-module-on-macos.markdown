---
title: "Build LLVM module on macOS"
layout: post
date: 2018-02-12 10:00:14 +0900
image: 'images/'
description:
tag: ['LLVM', 'macOS']
blog: true
author: "lewuathe"
---

Have you ever tried to build LLVM module on macOS? It may common to build LLVM module on Linux (e.g. Ubuntu). 
But I have macOS as my main machine. So this is the article to explain how to build LLVM module on macOS with minimal steps. 

# Homebrew

Fortunately, all LLVM package and dependencies can be installed via [Homebrew](https://brew.sh/). It includes headers and libraries needed to build your own LLVM module.

```
$ brew install llvm
```

Your LLVM will be installed in `/usr/local/opt/llvm`. 

# CMake

CMake is a cross-platform build tool. CMake is often used to build C/C++ project but you can use CMake more generally. From LLVM 3.5, using CMake to embed LLVM into your project is recommended.

> From LLVM 3.5 onwards both the CMake and autoconf/Makefile build systems export LLVM libraries as importable CMake targets. This means that clients of LLVM can now reliably use CMake to develop their own LLVM-based projects against an installed version of LLVM regardless of how it was built.

See [LLVM document](https://llvm.org/docs/CMake.html#embedding-llvm-in-your-project) more detail.

LLVM package in CMake provides useful command to link libraries from LLVM. This is the minimum list of command needed to build LLVM module.

```
cmake_minimum_required (VERSION 3.5)
project (myproject)
set (CMAKE_CXX_STANDARD 11)

find_package(LLVM REQUIRED CONFIG)

include_directories(/usr/local/opt/llvm/include)

llvm_map_components_to_libnames(llvm_libs core)

add_executable(main main.cc)
target_link_libraries(main ${llvm_libs})
```

I'm going to explain one by one.

```
cmake_minimum_required (VERSION 3.5)
project (mybf)
set (CMAKE_CXX_STANDARD 11)
```

This is the general setting which most projects require. `project(PROJECT_NAME)` is used to set the name of your project. `CMAME_CXX_STANDARD` is a variable to compile with C++11 standard.

```
find_package(LLVM REQUIRED CONFIG)
```

LLVM CMake package provides useful commands to embed LLVM into your project. I'll use `llvm_map_components_to_libnames` later. 

```
include_directories(/usr/local/opt/llvm/include)
```

Since header files of LLVM are stored in `/usr/local/opt/llvm/include`, we need to let CMake know where to search for. `include_directories` is similar to `-I` option in `clang`.

```
llvm_map_components_to_libnames(llvm_libs core)
```

This command is similar to `add_library` command. `core` library is linked to the target with the name of `llvm_libs`. You can specify multiple target libraries as you like. For example, 

```
llvm_map_components_to_libnames(llvm_libs support core irreader)
```

After that, you can link all necessary libraries by just specifying the name, `llvm_libs`.

```
target_link_libraries(main ${llvm_libs})
```

LLVM `core` is linked to `main` target. So your `main` program can use LLVM `core` library now.

# Build 

We often our-of-source build by CMake, which is nice way to build your project because it does not affect on your original source code at all.

```
$ mkdir build
$ cd build
$ cmake ..
$ make
```

That's all!




