---
title: "Compiling NNVM"
layout: post
date: 2017-10-13 15:16:31 +0900
image: 'images/'
description:
tag: ["DeepLearning", "Compiler", "C/C++"]
blog: true
author: "lewuathe"
---

[NNVM](https://github.com/dmlc/nnvm) is a new deep learning framework introduced by DMLC. NNVM is a compiler for deep learning. This is the point which differentiate NNVM from other existing deep learning frameworks such as [TensorFlow](http://tensorflow.org/). NNVM compiles given graph definition into execution code. Of course TensorFlow can also do same thing. But we need to write graph definition in TensorFlow manner. NNVM is a runtime agnostic compiler. If you familiar with [LLVM](https://llvm.org/), you may know what I mean. 

![nnvm stack](http://www.tvmlang.org/images/nnvm/nnvm_compiler_stack.png)

NNVM provides 

- Interface of graph definition
- Optimizer
- Runtime of kernel functions on various hardwares

Once you write a graph definition, it can be optimized on various kind of hardwares. This architecture is just similar to the frondend and backend of LLVM compiler. We can find Caffe, Keras, MXNet, PyTorch, Caffe2 and CNTK is now supported as frontend of NNVM, which means if you already have a graph definition in these frameworks, you can run it by using NNVM. 

Graph definition is first compiled into an original intermediate representation called [TVM IR](https://github.com/dmlc/tvm). TVM syntax looks very similar to the API in TensorFlow. 

```python
import tvm
n = tvm.var("n")
A = tvm.placeholder((n,), name='A')
B = tvm.placeholder((n,), name='B')
C = tvm.compute(A.shape, lambda i: A[i] + B[i], name="C")
print(type(C))
```

You write a graph definition in TVM. Then it is compiled into the code runnable on target device.

```python
fadd_cuda = tvm.build(s, [A, B, C], "cuda", target_host="llvm", name="myadd")
```

Since TVM only provides very primitive kernel API, NNVM is the framework we use for deploying a complex deep learning model on production. 

This is the post to explain how to build NNVM on your laptop. My local machine is macOS Sierra 10.12.6. 

## Install prerequisites

Though you may not need to do this depending on your target device and frontend, it's recommended to install them anyway. Protocol buffer is required by ONMX. 

```
$ brew install protobuf llvm
```

## Build source code

Check out first. NNVM includes several submodules such as TVM to be built together. Please make sure to add `--recursive` option.

```
$ git clone --recursive https://github.com/dmlc/nnvm
```

We build TVM first. 

```
$ cd nnvm/tvm
$ mkdir build
$ cd build
$ cmake ..
$ make
```

You will find artifacts `libtvm.dylib` and `libtvm_runtime.dylib` if it finished successfully. Then we build python interface of TVM.

```
$ cd ../python
$ python setup.py install
$ cd ../topi/python
$ python setup.py install
```

Finally we can build NNVM source code.

```
$ cd nnvm
$ make
$ cd python
$ python setup.py install --user
```

Adding library path is necessary to let Python find required libraries for NNVM.

```
export PYTHONPATH=/path/to/nnvm/python:${PYTHONPATH}
export LD_LIBRARY_PATH=/path/to/nnvm/tvm/build:${LD_LIBRARY_PATH}
```

Then you can run NNVM program through Python interface.

```python
> python
Python 3.6.0 |Anaconda 4.3.1 (x86_64)| (default, Dec 23 2016, 13:19:00)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import nnvm
TVM: Initializing cython mode...
>>>
```

What to be noted here is that we need to rebuild TVM and NNVM if you change the target device where the program is deployed. 

## Reference

- [NNVM](https://github.com/dmlc/nnvm)
- [NNVM Compiler: Open Compiler for AI Frameworks](http://www.tvmlang.org/2017/10/06/nnvm-compiler-announcement.html)
- [TVM](https://github.com/dmlc/tvm)
- [はじめてのNNVM](https://qiita.com/ashitani/items/e85231297247ec036128)
