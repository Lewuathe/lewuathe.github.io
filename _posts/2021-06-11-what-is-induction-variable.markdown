---
title: "What is Induction Variable?"
layout: post
date: 2021-06-11 15:15:22 +0900
image: 'assets/img/posts/2021-06-11-what-is-induction-variable/catch.jpg'
description:
tag: ['LLVM', 'Compiler']
blog: true
author: "Kai Sasaki"
---

I found an unfamiliar method when I looked into the LLVM documentation, [`getInductionVariable`](https://llvm.org/doxygen/classllvm_1_1Loop.html#ab05e97728516fbeeaa9426496257c800). I could see a similar name in [MLIR scf (Static Control Flow)](https://mlir.llvm.org/docs/Dialects/SCFDialect/#scffor-mlirscfforop) dialect as well.

> The operation defines an SSA value for its induction variable.

What is an **induction variable**?

[Wikipedia](https://en.wikipedia.org/wiki/Induction_variable) gave me a clear description of what the induction variable is.

> In computer science, an induction variable is a variable that gets increased or decreased by a fixed amount on every iteration of a loop or is a linear function of another induction variable

That's not limited to the value written in the `for` loop incrementally updated. All variables updated iteratively in the loop can be seen as induction variables.

```c
for (i = 0; i < 10; ++i) {
    j = 17 * i;
}
```

`i` and `j` are both induction variables in the previous case.

Induction variables are represented as region argument in MLIR `mlir::scf::ForOp`. Hence they are assumed to be passed from the outside of the region.

