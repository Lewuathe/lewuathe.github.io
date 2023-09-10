---
title: "Support Fast-Math Flag in MLIR"
layout: post
date: 2023-09-08 14:08:04 +0900
image: 'assets/img/posts/2023-09-08-support-fast-math-flag-in-mlir/catch.jpg'
description:
tag: ['MLIR', 'Compiler']
blog: true
author: "Kai Sasaki"
---

Needless to say, optimization is vital in the compiler pipeline to generate the code executable faster and compactly. The faster is better. One of the straightforward methods to make the code faster is eliminating unnecessary operations from the original instructions, such as redundant arithmetic operations or unused constants. These operations can hold some memory footprint and consume execution time despite its uselessness. Let's think about the case where we are going to add 0 to any numbers.

```c
int add(int a, int b)
{
  return a + b;
}
```

We can compile this code naively into RISC-V assembly.

```riscv
add(int, int):
  add a0,a0,a1
  ret
```

The compiler automatically eliminates unnecessary operations with the following code.
```c
int add0(int a, int b)
{
  return a + 0;
}
```

```
add0(int, int):
  ret
```

Note that the given argument is directly returned in `a0` register. When we want to add 0 to the second argument, the compiler needs to generate the `mv` instruction to load the data into `a0` 

See the real example [Compiler Explorer]([Compiler Explorer](https://godbolt.org/z/n58j9cM86))

However, this arithmetic optimization is only sometimes permitted. In the case we require more strict numerical precision in the floating-point operations, the instruction elimination for optimization can naturally cause an unsafe result. For instance, if the `a` would be +/- infinity in the above case, what binary representation should we return?

[Fast-Math Flags](https://llvm.org/docs/LangRef.html#fast-math-flags) is a compiler option to control floating-point optimization behavior by giving additional assumptions the code can take into account. If the compilation can premise the specific condition, it can safely eliminate or transform the instructions under such a condition. There are eight options in LLVM and each of them provides the specific assertion on the given numerical values.

- `nnan`
No NaNs - Allow optimizations to assume the arguments and result are not NaN. If an argument is a nan, or the result would be a nan, it produces a [poison value](https://llvm.org/docs/LangRef.html#poisonvalues) instead.
- `ninf`
No Infs - Allow optimizations to assume the arguments and result are not +/-Inf. If an argument is +/-Inf, or the result would be +/-Inf, it produces a [poison value](https://llvm.org/docs/LangRef.html#poisonvalues) instead.
- `nsz`
No Signed Zeros - Allow optimizations to treat the sign of a zero argument or zero result as insignificant. This does not imply that -0.0 is poison and/or guaranteed to not exist in the operation.
- `arcp`
Allow Reciprocal - Allow optimizations to use the reciprocal of an argument rather than perform division.
- `contract`
Allow floating-point contraction (e.g. fusing a multiply followed by an addition into a fused multiply-and-add). This does not enable reassociating to form arbitrary contractions. For example, `(a*b) + (c*d) + e` can not be transformed into `(a*b) + ((c*d) + e)` to create two fma operations.
- `afn`
Approximate functions - Allow substitution of approximate calculations for functions (sin, log, sqrt, etc). See floating-point intrinsic definitions for places where this can apply to LLVM’s intrinsic math functions.
- `reassoc`
Allow reassociation transformations for floating-point instructions. This may dramatically change results in floating-point.
- `fast`
This flag implies all of the others.

In MLIR world, however, these flags are not fully supported. [Arith](https://discourse.llvm.org/t/rfc-fastmath-flags-support-in-mlir-arith-dialect/6049) dialect supports these flags in the past. But higher level dialects (e.g. Math, Complex) lowering operation to Arith dialect do not fully recognize these options. That limits the opportunity for optimization in the dialect itself since they do not have complete information they can take it for granted. So I proposed the support of Fast-Math flags in complex dialect so that we can lower operations with full assumption about the floating-point premises and get more chance to optimize the code in the complex dialect itself. 

[[RFC] FastMath flags support in complex dialect - MLIR - LLVM Discussion Forums](https://discourse.llvm.org/t/rfc-fastmath-flags-support-in-complex-dialect/71981)

The initial change has been merged, and we are preparing progressive updates to support the flag for all complex ops lowering to Arith and LLVM. You can write the complex ops with the optional `fastmath` flag field like this.

```mlir
%add = complex.add %lhs, %rhs fastmath<nnan,contract> : complex<f32>
```

We can pass the fast math flag information by each operation.