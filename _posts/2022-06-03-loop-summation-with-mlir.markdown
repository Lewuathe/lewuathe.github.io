---
title: "Loop summation with MLIR"
layout: post
date: 2022-06-03 09:36:55 +0900
image: 'assets/img/posts/2022-06-03-loop-summation-with-mlir/catch.jpg'
description:
tag: ['MLIR', 'LLVM', 'Compiler']
blog: true
author: "Kai Sasaki"
---

[MLIR](https://mlir.llvm.org/) is not a programming language in a broad sense. As the name suggests, it's an intermediate representation to express the middle-level structure of the program. This framework is so versatile and flexible by employing the plugin architecture inside. It might be possible (and even natural) to write our program with MLIR by hand. MLIR is powerful in representing the high-level structure we recognize when writing algorithms. I tried to run a simple program adding up all values from 0 to 10 (inclusive).

## Affine Dialect

It is straightforward to use [Affine Dialect](https://mlir.llvm.org/docs/Dialects/Affine/) to implement the nested loop in MLIR. The syntax is very similar to what we see with the higher-level programming language like C/C++ and Java. [`affine.for`](https://mlir.llvm.org/docs/Dialects/Affine/#affinefor-mliraffineforop) is an operation representing a loop containing a region in its body. It gets three operands, lower bound, upper bound, and step value.

```mlir
affine.for $i = 0 to 11 step 1 {
  // Body
}
```

This code iterates the SSA value $i from 0 to 10. Step operand is optional. The block in `affine.for` should have one terminator operation [`affine.yield`](https://mlir.llvm.org/docs/Dialects/Affine/#affineyield-affineyieldop). This operation yields zero or more SSA values from an affine op region. In this case, we will use this operation to return the final summation value. `iter_args` is helpful to retain the loop-carryed variables, which are in the scope of the body region of `affine.for`. This value holds what is returned by the termination operation `affile.yield`. We will use `%sum_iter` to keep the current accumulated value.

In addition to the affine dialect, we need to use [Arith Dialect](https://mlir.llvm.org/docs/Dialects/ArithmeticOps/), which holds basic integer and floating-point mathematical operations. We utilize this dialect to initialize the constant and add operations.

As a whole, the program will look as follows.


```mlir
func.func @main() -> i32 {
  %sum_0 = arith.constant 0 : i32
  %sum = affine.for %i = 0 to 11 step 1 iter_args(%sum_iter = %sum_0) -> (i32) {
    %t = arith.index_cast %i : index to i32
    %sum_next = arith.addi %sum_iter, %t : i32
    affine.yield %sum_next : i32
  }
  return %sum : i32
}
```

## Lowering to LLVM

To run the program in MLIR, we need to lower it to the lowest level in the executable format. That means converting one dialect to another dialect in the MLIR sense. We will convert affine and arithmetic dialect to LLVM dialect first. `mlir-opt` is a handy tool to achieve that type of conversion.

```mlir
$ mlir-opt \
    --lower-affine \
    --convert-arith-to-llvm \
    --convert-scf-to-cf \
    --convert-func-to-llvm \
    --reconcile-unrealized-casts sum.mlir

module attributes {llvm.data_layout = ""} {
  llvm.func @main() -> i32 {
    %0 = llvm.mlir.constant(0 : i32) : i32
    %1 = llvm.mlir.constant(0 : index) : i64
    %2 = llvm.mlir.constant(11 : index) : i64
    %3 = llvm.mlir.constant(1 : index) : i64
    llvm.br ^bb1(%1, %0 : i64, i32)
  ^bb1(%4: i64, %5: i32):  // 2 preds: ^bb0, ^bb2
    %6 = llvm.icmp "slt" %4, %2 : i64
    llvm.cond_br %6, ^bb2, ^bb3
  ^bb2:  // pred: ^bb1
    %7 = llvm.trunc %4 : i64 to i32
    %8 = llvm.add %5, %7  : i32
    %9 = llvm.add %4, %3  : i64
    llvm.br ^bb1(%9, %8 : i64, i32)
  ^bb3:  // pred: ^bb1
    llvm.return %5 : i32
  }
}
```

As you can see, there are several options to complete this conversion.

* `--lower-affine` : Lowering affine dialect to standard dialect.
* `--convert-arith-to-llvm` : Convert arithmetic dialect to LLVM dialect.
* `--convert-scf-to-cf` : Convert structured control flow dialect to the primitive control flow dialect.
* `--convert-func-to-llvm` : Convert func dialect to LLVM dialect.

We do not talk about them in detail here, but the final code in MLIR only contains operations from the LLVM dialect. (Note that they start with the `llvm` prefix). Finally, it's ready to go down to LLVM IR!

## Translate MLIR to LLVM IR

`mlir-translate` is another handy tool to convert the MLIR program into LLVM IR format. For example, put `--mlir-to-llvmir` option as follows.

```
$ mlir-opt \
    --lower-affine \
    --convert-arith-to-llvm \
    --convert-scf-to-cf \
    --convert-func-to-llvm \
    --reconcile-unrealized-casts sum.mlir | \
    mlir-translate --mlir-to-llvmir

; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"

declare ptr @malloc(i64)

declare void @free(ptr)

define i32 @main() {
  br label %1

1:                                                ; preds = %5, %0
  %2 = phi i64 [ %8, %5 ], [ 0, %0 ]
  %3 = phi i32 [ %7, %5 ], [ 0, %0 ]
  %4 = icmp slt i64 %2, 11
  br i1 %4, label %5, label %9

5:                                                ; preds = %1
  %6 = trunc i64 %2 to i32
  %7 = add i32 %3, %6
  %8 = add i64 %2, 1
  br label %1

9:                                                ; preds = %1
  ret i32 %3
}
```

You may find several additional directives for debugging purposes. But the central part of the program should be identical. Now it should be able to execute.

```
$ mlir-opt \
    --lower-affine \
    --convert-arith-to-llvm \
    --convert-scf-to-cf \
    --convert-func-to-llvm \
    --reconcile-unrealized-casts sum.mlir | \
    mlir-translate --mlir-to-llvmir | lli

$ echo $?
55
```

The program returns the summation value as an exit code correctly! If you enjoy the writing program at MLIR, please visit the MLIR website for more detail. You may find excellent examples or hint to implementing the algorithm in MLIR directly.

## References
* [Affine Dialect](https://mlir.llvm.org/docs/Dialects/Affine/)
* [Arith Dialect](https://mlir.llvm.org/docs/Dialects/ArithmeticOps/)
* [Learn LLVM 12](https://amzn.to/3NOD9Ur)