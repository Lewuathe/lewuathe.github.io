---
title: "How to init Memref in MLIR"
layout: post
date: 2021-04-23 11:22:14 +0900
image: 'assets/img/posts/2021-04-23-how-to-init-memref-in-mlir/catch.jpg'
description:
tag: ['MLIR', 'Compiler', 'C++', 'LLVM']
blog: true
author: "Kai Sasaki"
---

Reading the tutorial of one software always brings me to the gateway leading to the other eternal journey. It's an exciting experience if you are a technology enthusiast. Walking the path to be the software expert on your foot can be an irreplaceable event in your career.

But it's also true that a guidebook written by the pioneer on the field gives you a distinct viewpoint on the path, and it can make your experience more exciting and profound.

I have walked through [the Toy tutorial](https://mlir.llvm.org/docs/Tutorials/) to learn the [MLIR](https://mlir.llvm.org/) and have found many things to know through the journey. This article aims to clarify the point I struggled to grasp the concept and usage of MLIR based on my experience.

This time I'm going to focus on creating the Memref in a pass in a custom MLIR Dialect.

# What is Memref in MLIR?

In the first place, what is a Memref at all? [FAQ](https://mlir.llvm.org/getting_started/Faq/) part of the official documentation gives us a brief introduction of the Memref type.

> You can have a memref (a buffer in memory) containing Vectors, but you can't have a memref of a tensor type.

Looking at this description, Memref is a low-level concept more directly associated with the underlying hardware. It's just a pointer to the memory location where the tensor data (or vector) is stored. [Memref](https://mlir.llvm.org/docs/Dialects/MemRef/) dialect provides the way to manipulate the allocation or layout of the field pointed by the memref type. For instance, [`memref.alloc`](https://mlir.llvm.org/docs/Dialects/MemRef/#memrefalloc-mlirmemrefallocop) enables us to allocate memory space enough for the given data type. The following code allocates the contiguous memory field for 2x3x64 bits.

```mlir
%0 = memref.alloc() : memref<2x3xf64>
```

As we use `malloc` in C, it is practically vital to call the memory resource's deallocation explicitly. We can free the space by calling [`memref.dealloc`](https://mlir.llvm.org/docs/Dialects/MemRef/#memrefdealloc-mlirmemrefdeallocop).

```mlir
memref.dealloc %0 : memref<2x3xf64>
```

Of course, we need to embed the values into the memref. That can be done by `memref.store` or `affine.store`, which can recognize memref type.

```mlir
affine.store %cst_3, %0[%c1, %c1] : memref<2x3xf64>
```

How can we create these IRs by using MLIR API?


# Intialization Procedure

To make sure to call allocation and deallocation in a block, we get the block where the allocation is created. `Block.front()` and `Block.back()` provide us the correct location where allocation/deallocation pair should exist.

```cpp
mlir::Location loc = ...
mlir::MemRefType type = ...
mlir::PatternRewriter rewriter = ...

auto alloc = rewriter.create<mlir::memref::AllocOp>(loc, type);
auto *parentBlock = alloc->getBlock();
alloc->moveBefore(&parentBlock->front());
auto dealloc = rewriter.create<mlir::memref::DeallocOp>(loc, alloc);
dealloc->moveBefore(&parentBlock->back());
```

Store operation can be created as follows.

```cpp
rewriter.create<mlir::AffineStoreOp>(
    loc,
    rewriter.create<mlir::ConstantOp>(loc, 1.0),
    alloc,
    llvm::makeArrayRef([0, 0]));
```

`loc` is a location where this `affine.store` is created. `alloc` is a target memref type. The last argument specifies the index within the memref type where the value is assumed to be stored.

Finally, we will get the following MLIR code.

```mlir
module  {
  func @main() {
    %0 = memref.alloc() : memref<2x3xf64>
    %c0 = constant 0 : index
    %cst = constant 1.000000e+00 : f64
    affine.store %cst, %0[%c0, %c0] : memref<2x3xf64>
    memref.dealloc %0 : memref<2x3xf64>
    return
  }
}
```

We can construct any procedure to initialize memref type by obeying this convention overall. Please visit my toy project named [mlir-hello](https://github.com/Lewuathe/mlir-hello) for more detail.

# Reference

- [Lewuathe/mlir-hello](https://github.com/Lewuathe/mlir-hello)
- [Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/)