---
title: "Specify project specific Python with Poetry"
layout: post
date: 2023-01-23 12:07:41 +0900
image: 'assets/img/posts/2023-01-23-specify-project-specific-python-with-poetry/catch.jpg'
description:
tag: ['Python', 'macOS']
blog: true
author: "Kai Sasaki"
---

[Poetry](https://python-poetry.org/) allows us to manage the Python packages in a sandboxed environment neatly. My experience using Poetry was excellent, and I have replaced my Python way with Poetry from [Pipenv](https://pipenv.pypa.io/en/latest/).

But I sometimes found Poetry failed to resolve the dependencies because of the unsupported Python version used by the environment. For example, it shows the following error message.

```
The currently activated Python version 3.7.14 is not supported by the project (^3.9).
Trying to find and use a compatible version.
```

Some packages I used were not compatible with Python 3.7 in this case. But I was confused because my local PATH leads to Python 3.9 thanks to [Pyenv](https://github.com/pyenv/pyenv). So how can I specify the project-specific python version?

The answer was simple. It needs to be more to specify the PATH by pyenv. We also need to set the python version by `init` or `env use` subcommands.

```
$ poetry init --python 3.9

OR

$ poetry env use 3.9
```
It tells the Poetry environment to use this Python version explicitly.  With these settings, we can install all dependencies without any problem.
