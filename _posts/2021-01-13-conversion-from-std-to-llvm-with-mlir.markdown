---
title: "Conversion from std to llvm with MLIR"
layout: post
date: 2021-01-13 10:35:12 +0900
image: 'assets/img/posts/2021-01-13-conversion-from-std-to-llvm-with-mlir/catch.jpg'
description:
tag: ['MLIR', 'Compiler', 'LLVM']
blog: true
author: "Kai Sasaki"
---

Continuing from the latest article, I'm going to cover another topic of MLIR as well.

[`mlir-opt`](https://mlir.llvm.org/docs/Tutorials/Toy/Ch-2/#interfacing-with-mlir) is a tool working as a utility to manipulate the MLIR code by applying various kinds of passes and optimizations legally. It enables us to convert a dialect of MLIR to another dialect easily. There is a tremendous amount of functionality and options in `mlir-opt`. Hence I'm afraid I cannot cover the whole topic of `mlir-opt` on this small page. (`mlir-opt --help` emits 372 lines for options!)

The main takeaway of this article will be the primary usage of `mlir-opt` for the dialect conversion by demonstrating the example from [std](https://mlir.llvm.org/docs/Dialects/Standard/) dialect to [llvm](https://mlir.llvm.org/docs/Dialects/LLVM/) dialect. At last, we will see the result returned by the code lowered by `mlir-opt`. I hope this article will work as a little tutorial of `mlir-opt` to let you get used to the tools provided by MLIR.

# MLIR Code

First, let's write a tiny MLIR code returning an `i32` value from the main function. It should work as a hello world program in our case.

```
func @main() -> (i32) {
  %0 = constant 42 : i32
  return %0 : i32
}
```

We define a function named `@main` receiving no argument and returning a single `i32` value. `constant` is [an operation provided by `std` dialect](https://mlir.llvm.org/docs/Dialects/Standard/#stdconstant-constantop) generating an SSA value with the specified attribute. Finally, it returns the SSA value (`%0`) with [`std.return` operation](https://mlir.llvm.org/docs/Dialects/Standard/#stdreturn-returnop) working as a termination of the function.

You may expect mlir-opt will convert it to the function returning 42 intuitively. That's right! We'll confirm `mlir-opt` and tools provided by MLIR works as you expected. `mlir-opt` legalizes std to dialect as follows.

```bash
$ mlir-opt --convert-std-to-llvm mytest.mlir
module attributes {llvm.data_layout = ""}  {
  llvm.func @main() -> i32 {
    %0 = llvm.mlir.constant(42 : i32) : i32
    llvm.return %0 : i32
  }
}
```

The converted code is printed in stdout. But note that we are still in the world of MLIR, which is not executable directly. It is also necessary to generate LLVM IR from the LLVM dialect code.

# mlir-cpu-runner

Here comes `mlir-CPU-runner`. This tool provides a JIT environment for MLIR code. It is capable of executing any LLVM dialect code as it is.

```bash
$ mlir-opt --convert-std-to-llvm mytest.mlir  | mlir-cpu-runner --entry-point-result=i32
42
```

But it also has an option to print the LLVM IR from the given LLVM dialect. `--print-module` will dump the LLVM IR of the corresponding LLVM module constructed in the JIT environment of `mlir-CPU-runner`. That allows us to fly away from the world of MLIR and obtain the portable format of the code.

```bash
$ mlir-opt --convert-std-to-llvm mytest.mlir  | mlir-cpu-runner \
    --print-module --entry-point-result=i32 > /dev/null
```


```llvm
; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-darwin19.6.0"

declare i8* @malloc(i64)

declare void @free(i8*)

define i32 @main() !dbg !3 {
  ret i32 42, !dbg !7
}

define void @_mlir_main(i8** %0) {
  %2 = call i32 @main()
  %3 = getelementptr i8*, i8** %0, i64 0
  %4 = load i8*, i8** %3, align 8
  %5 = bitcast i8* %4 to i32*
  store i32 %2, i32* %5, align 4
  ret void
}

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2}

!0 = distinct !DICompileUnit(language: DW_LANG_C, file: !1, producer: "mlir", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug)
!1 = !DIFile(filename: "LLVMDialectModule", directory: "/")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = distinct !DISubprogram(name: "main", linkageName: "main", scope: null, file: !4, line: 2, type: !5, scopeLine: 2, spFlags: DISPFlagDefinition | DISPFlagOptimized, unit: !0, retainedNodes: !6)
!4 = !DIFile(filename: "<stdin>", directory: "/path/to/llvm-project/build")
!5 = !DISubroutineType(types: !6)
!6 = !{}
!7 = !DILocation(line: 4, column: 5, scope: !8)
!8 = !DILexicalBlockFile(scope: !3, file: !4, discriminator: 0)
```

Since `mlir-CPU-runner` outputs the code in stderr, I discarded the stdout, which shows the output from the program itself (42 in this case).

# Execute the Program on the Host Machine

Okay, now it's executable on any machine included in the scope of the LLVM target. I'm going to use [lli](https://llvm.org/docs/CommandGuide/lli.html), a tool to execute the program from LLVM assembly.

```bash
$ mlir-opt --convert-std-to-llvm mytest.mlir  | \
    mlir-cpu-runner --print-module --entry-point-result=i32 > /dev/null 2> mytest.ll
```

lli executes the program in the format of LLVM assembly.

```bash
$ lli mytest.ll
$ echo $?
42
```

It works. It should be fun to rewrite the code in std dialect and play around by seeing the result.

Thanks!

