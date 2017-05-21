---
title: "How to build TensorFlow on macOS"
layout: post
date: 2017-05-20 13:58:03 +0900
image: 'images/'
description:
tag:
blog: true
author: "lewuathe"
---

I tried to build TensorFlow on my macOS. It was not difficult for me as a result. I could build the TensorFlow according to
the official instruction. So I'll add the tiny tips for building TensorFlow in addition to original instruction.

## Clone the repository

First you need to download the source code of TensorFlow. I downloaded TensorFlow under `GOPATH` because it includes [Go binding package](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/go)
in the repository.

```
$GOPATH/src/github.com/tensorflow/tensorflow
```

We can make use of Go infrastructures by installing here. (e.g. IDE plugins). So I recommend to install under `GOPATH`.

## Prerequisites

You need to install these dependencies first.

* [bazel](https://bazel.build/versions/master/docs/install.html#mac-os-x)
* Python package
    - six
    - numpy
	- wheel
* coreutils

I use [pyenv](https://github.com/pyenv/pyenv) and [anaconda](https://www.continuum.io/) for creating Python development environment.

```
$ pyenv install anaconda3-4.2.0
```

It already includes required packages. Please try pyenv and anaconda for your Python environment.
And you can install core utils with [Homebrew](https://brew.sh/).

```
$ brew install coreutils
```

## Configure

Set configuration for building environment.

```
$ /path/to/tensorflow
$ ./configure
```

* Python path -> `$HOME/.pyenv/shims/python`
* Python library path (default) -> `$HOME/.pyenv/versions/anaconda3-4.2.0/lib/python3.5/site-packages`
* MKL support -> No
* optimization flag -> default
* GCP support -> No
* HDFS support -> No
* XLA compiler support -> No
* VERBS support -> No
* OpenCL support -> No
* CUDA support -> No

In order to make compilation time shorter and avoid unnecessary build error, I disabled almost all configurations. If you want, please enable them with installing corresponding dependencies.

## Build and Install

```
$ bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package
```

It requires a lot of RAM and takes several minutes. The command generates the script for packaging. It puts the `.whl` package under `/tmp/tensorflow_pkg`

```
$ bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

You can install the package in your Python environment as ordinal Python packages.

```
$ pip install /tmp/tensorflow_pkg/tensorflow-1.1.0-py2-none-any.whl
```

## Validate the installation

**NOTE**: Please move other workspace from the tensorflow repository otherwise you will see `not found package` error. 

```python
>>> import tensorflow as tf
>>> hello = tf.constant('Hello, TensorFlow!')
>>> sess = tf.Session()
>>> print(sess.run(hello))
```

## Reference

* [Installing TensorFlow from Sources](https://www.tensorflow.org/install/install_sources)
