---
title: "How store-to-load forwarding works in MLIR"
layout: post
date: 2022-12-27 10:59:26 +0900
image: 'assets/img/posts/2022-12-27-how-store-to-load-forwarding-works-in-mlir/catch.jpg'
description:
tag: ['MLIR', 'LLVM']
blog: true
author: "Kai Sasaki"
---

I don't know the origin of store-to-load forwarding terminology, but major processors and compilers widely employ this technique. According to [this blog](https://blog.stuffedcow.net/2014/01/x86-memory-disambiguation/), the store-to-load forwarding forwards the data which is assumed to be in the cache by the store operation in advance to the load operation, which depends on the previous store operation. Pipelined execution does not guarantee the last store execution puts the data in the cache and memory until the operation is committed. It can bring a problem when the dependent load operation tries to refer to the data stored by the store operation. We must fetch the original value itself (in the store queue by x86) instead of from the cache or memory. To the best of my knowledge, this is the original definition of store-to-load forwarding optimization. 

MLIR also has an optimization pass to implement store-to-load forwarding. But it seems slightly different from what I explained MLIR could execute store-to-load forwarding in the part of the scalar replacement.

[MLIR: Affine Scalar Replacement](https://mlir.llvm.org/docs/Passes/#-affine-scalrep-replace-affine-memref-acceses-by-scalars-by-forwarding-stores-to-loads-and-eliminating-redundant-loads)

> This pass performs a store to load forwarding and redundant load elimination for affine memref accesses and potentially eliminates the entire memref if all its accesses are forwarded.

This pass aims to eliminate redundant memref access of both store and load operations and can access the same element in the memref by replacing it with the scalar value. 

For instance, here is a code with the nested `affine.for` like this.

```mlir
func.func @store_load_affine_apply() -> memref<10x10xf32> {
  %cf7 = arith.constant 7.0 : f32
  %m = memref.alloc() : memref<10x10xf32>
  affine.for %i0 = 0 to 10 {
    affine.for %i1 = 0 to 10 {
      affine.store %cf7, %m[%i0, %i1] : memref<10x10xf32>
      %v0 = affine.load %m[%i0, %i1] : memref<10x10xf32>
      %v1 = arith.addf %v0, %v0 : f32
    }
  }
  return %m : memref<10x10xf32>
}
```

This turns into the function without unnecessary `store.load` operation by running the pass `-affine-scalrep`.

```
module {
  func.func @store_load_affine_apply() -> memref<10x10xf32> {
    %cst = arith.constant 7.000000e+00 : f32
    %0 = memref.alloc() : memref<10x10xf32>
    affine.for %arg0 = 0 to 10 {
      affine.for %arg1 = 0 to 10 {
        affine.store %cst, %0[%arg0, %arg1] : memref<10x10xf32>
        %1 = arith.addf %cst, %cst : f32
      }
    }
    return %0 : memref<10x10xf32>
  }
}
```

But why does this pass need store-to-load optimization inside? 

Look closer at the relationship between `affine.store` and `affine.load`. If we succeed in store-to-load forwarding, it indicates that 1) both operations access the same element in the memref and 2) store operation is dominant against the memref the load operation refers to. Satisfying these conditions suggests we can replace the element with the scalar value because no other operation can use the value in between. Hence, store-to-load forwarding gives us the precondition to run the scalar replacement successfully. Of course, more is needed to complete the scalar replacement. We also need to run the dependency analysis between the store and load, considering the depth of the nested structure. The scalar replacement in MLIR is more complicated by far than I expected. 