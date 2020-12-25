---
title: "Hello,World with MLIR (2)"
layout: post
date: 2020-12-25 10:04:51 +0900
image: 'assets/img/posts/2020-12-25-hello,world-with-mlir-(2)/catch.jpg'
description:
tag: ['compiler', 'MachineLearning', 'TensorFlow']
blog: true
author: "Kai Sasaki"
---

Continuing from the [last article](https://www.lewuathe.com/hello,world-with-mlir.html) to create minimal Dialect to print tensor element with MLIR, I am going to illustrate the structure of the codebase of Dialect.

As noted previously, I put the whole repository on [Lewuathe/mlir-hello](https://github.com/Lewuathe/mlir-hello). Please take a look into that if you need to know more.

# Code Structure

The official site contains the [general guide](https://mlir.llvm.org/docs/Tutorials/CreatingADialect/) to create Dialect. Here is the illustration of the structure of the repository.

```
├── CMakeLists.txt
├── README.md
├── hello-opt
│   ├── CMakeLists.txt
│   └── hello-opt.cpp
├── hello-translate
│   ├── CMakeLists.txt
│   └── hello-translate.cpp
├── include
│   ├── CMakeLists.txt
│   └── Hello
│       ├── CMakeLists.txt
│       ├── HelloDialect.h
│       ├── HelloDialect.td
│       ├── HelloOps.h
│       ├── HelloOps.td
│       └── HelloPasses.h
├── lib
│   ├── CMakeLists.txt
│   └── Hello
│       ├── CMakeLists.txt
│       ├── HelloDialect.cpp
│       ├── HelloOps.cpp
│       ├── LowerToAffine.cpp
│       └── LowerToLLVM.cpp
├── test
│   ├── CMakeLists.txt
│   ├── Hello
│   │   ├── dummy.mlir
│   │   ├── print.mlir
│   │   ├── sample-opt.mlir
│   │   └── sample-translate.mlir
│   ├── lit.cfg.py
│   └── lit.site.cfg.py.in
```

# ODS Declarations

`include` directory needs to include definitions of Dialect and Operations in [Operation Definition Specification format (ODS)](https://mlir.llvm.org/docs/OpDefinitions/). ODS is a framework to define the specification of Dialect and Operations declaratively. This framework is powered by the [TableGen](https://llvm.org/docs/TableGen/index.html) mechanism maintained in LLVM Core. MLIR generates the C++ code from the ODS declaration. We need to write the following code in CMakeFiles.

```cmake
# Add the HelloOps for the dialect operations
add_mlir_dialect(HelloOps hello)

# Necessary to generate documentation
add_mlir_doc(HelloDialect -gen-dialect-doc HelloDialect Hello/)
add_mlir_doc(HelloOps -gen-op-doc HelloOps Hello/)
```

With this directive, CMake automatically generates the header files named `HelloOpsDialect.h.inc` and `HelloOps.h.inc` containing C++ code corresponding to the Dialect and operations you defined. We must include these files explicitly in the hand-written header files.

`HelloDialect.h`
```
#include "Hello/HelloOpsDialect.h.inc"
```

`HelloOps.h`
```
#define GET_OP_CLASSES
#include "Hello/HelloOps.h.inc"
```

It's worth noting that `HelloOps.h` uses preprocessor directive `#define GET_OP_CLASSES`. Interestingly `HelloOps.h.inc` contains several distinct sections in a file to fetch the only necessary information as desired by using the preprocessor directive. `GET_OP_CLASSES` will expand the declarations of operation classes.

# Implementation Classes

The code implementing the operation, transformation, etc., should be put in the `lib/Hello` directory. `HelloDialect.cpp` needs to have an initializer at least.

```cpp
#include "mlir/IR/Builders.h"
#include "mlir/IR/OpImplementation.h"

#include "Hello/HelloDialect.h"
#include "Hello/HelloOps.h"

using namespace mlir;
using namespace hello;

void HelloDialect::initialize() {
  addOperations<
#define GET_OP_LIST
#include "Hello/HelloOps.cpp.inc"
      >();
}
```

Note that we use `GET_OP_LIST` to render all the names of operations supported by Hello Dialect. Similarly, we can write the `HelloOps.cpp` file as follows.

```cpp
#include "Hello/HelloOps.h"
#include "Hello/HelloDialect.h"
#include "mlir/IR/OpImplementation.h"

#define GET_OP_CLASSES
#include "Hello/HelloOps.cpp.inc"
```

This structure makes clear the separation between Dialect-related implementation and Operation-related implementation.

# Passes for Lowering

In addition to these files, the Hello dialect has two files for lowering the Hello code to LLVM. `LowerToAffine.cpp` and `LowerToLLVM.cpp`. These passes define the way to convert one Dialect to another dialect. In our case, Hello Dialect must be compiled into the executable format to run it. Since the code is transformed into LLVM IR format, we can execute it. Therefore the goal of these passes is lowering Hello Dialect to LLVM while passing Affine, Standard dialects. In `hello-op` CLI, we register these passes as follows.

```cpp
// Register passes to be applied in this compile process
mlir::PassManager passManager(&context);
mlir::OpPassManager &optPm = passManager.nest<mlir::FuncOp>();
optPm.addPass(hello::createLowerToAffinePass());
passManager.addPass(hello::createLowerToLLVMPass());
```

We will look into the detail for the transformation and pass the infrastructure itself another time.

The following directive in CMake is required to compile the project properly. You can add additional libraries as you like here if necessary.

```cmake
add_mlir_dialect_library(MLIRHello
    HelloDialect.cpp
    HelloOps.cpp
    LowerToAffine.cpp
    LowerToLLVM.cpp

    ADDITIONAL_HEADER_DIRS
    ${PROJECT_SOURCE_DIR}/include/Hello

    DEPENDS
    MLIRHelloOpsIncGen

    LINK_LIBS PUBLIC
    MLIRIR
  )
```

# Run hello-opt

`hello-opt` is a tool to convert Hello dialect code to LLVM IR quickly. It loads necessary dialects from the registry. The MLIR module is loaded and transformed into the `mlir::OwningModuleRef` class.

```cpp
int main(int argc, char **argv) {
  mlir::registerPassManagerCLOptions();
  cl::ParseCommandLineOptions(argc, argv, "Hello compiler\n");

  mlir::registerAllPasses();
  mlir::MLIRContext context;
  context.getOrLoadDialect<hello::HelloDialect>();
  context.getOrLoadDialect<mlir::StandardOpsDialect>();
  context.getOrLoadDialect<mlir::LLVM::LLVMDialect>();

  mlir::OwningModuleRef module;
  if (int error = loadAndProcessMLIR(context, module)) {
    return error;
  }

  dumpLLVMIR(*module);

  return 0;
}
```

Let's say we have the following Hello dialect code.

```mlir
func @main() {
    %0 = "hello.constant"() {value = dense<1.0> : tensor<2x3xf64>} : () -> tensor<2x3xf64>
    "hello.print"(%0) : (tensor<2x3xf64>) -> ()
    return
}
```

It defines a constant tensor whose all elements are 1.0 with the shape <2x3>. And print each element according to its tensor shape. Let's execute it.

Build the project as follows.

```
mkdir build && cd build

# Path to the LLVM artifacts we build previously
LLVM_DIR=/path/to/llvm-project/build/lib/cmake/llvm \
  MLIR_DIR=/path/to/llvm-project/build/lib/cmake/mlir \
  cmake -G Ninja ..

cmake --build . --target hello-opt
```

`hello-op` will dump the LLVM IR into the `print.ll` file.

```
# Lower MLIR to LLVM IR
./build/bin/hello-opt ./test/Hello/print.mlir > /path/to/print.ll
```

You can use [`lli`](https://llvm.org/docs/CommandGuide/lli.html) to execute the LLVM bitcode format interactively.

````
lli /path/to/print.ll

1.000000 1.000000 1.000000
1.000000 1.000000 1.000000
```

It works finally!

Besides that, MLIR has many exciting topics to be discussed, such as [Interfaces](https://mlir.llvm.org/docs/Interfaces/), [DRR for rewriting](https://mlir.llvm.org/docs/DeclarativeRewrites/). Please visit the great [official website](https://mlir.llvm.org/docs/DeclarativeRewrites/) for more about MLIR. I'll extend the Hello dialect more if I get a chance to do so.

Enjoy!