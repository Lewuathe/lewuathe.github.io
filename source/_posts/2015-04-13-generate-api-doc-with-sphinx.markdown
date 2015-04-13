---
layout: post
title: "Generate API doc with Sphinx"
date: 2015-04-13 19:51:21 +0900
comments: true
categories: ["Python", "Documentation"]
author: Kai Sasaki
---

Have you ever use [Sphinx](http://sphinx-doc.org/) to create beautiful documentation in your project?
Although I have heard about Sphinx and usefulness of it before, this is the first experience for me. In my case, I want to
generate an API documentation of my python project. If you create API documentation by your hand, it must be very troublesome.
So I decided to delegate this task to Sphinx.

<!-- more -->

## Build Flow

Ordinal build flow might be like below.

* Generate [reStructuredText](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html) with `sphinx-apidoc`.
* Build reStructuredText to html with `sphinx-build` command.

Most of sphinx projects will do above flow to generate api documentations. However it is necessary to embed this flow into `distutils` flow this time.
So it does not require sphinx environment in advance because `setup.py` installs some packages which is required by my project. I want to build api document on this temporary environment. In other words, there is no way to use `sphinx-apidoc` or `sphinx-build` tool because they are not included egg packages!! So I tried and succeeded.

## Project structure

Directory structure of my project is like below.

```bash
myproject
├── docs
│   ├── _build
│   ├── conf.py
│   ├── index.rst
│   ├── make.bat
│   ├── Makefile
│   ├── _static
│   └── _templates
├── lib
├── README.md
├── setup.cfg
└── setup.py

5 directories, 7 files
```

`setup.py` is written like this.

```python
from setuptools import setup, find_packages
import sys
import os
from docs.build_apidoc import BuildApiCommand

version = '0.0.1'
long_description = open('README.md', 'r').read().decode('utf-8')

setup(
    name='myproject',
    version=version,
    description='My Package',
    long_description=long_description,
    setup_requires=['Sphinx'],
    cmdclass = {
        'build_apidoc': BuildApiCommand
    }
)
```

What is the `docs.build_apidoc`? This is the core component of this build process written for this project. This is the code of it.

```python
import os
import sys
import re

import distutils.cmd
import distutils.log
import setuptools
import subprocess

class BuildApiCommand(distutils.cmd.Command):
  """A custom command to build api document with Sphinx"""

  description = 'run sphinx-apidoc'

  def initialize_options(self):
    """Set default values for options."""
    # Each user option must be listed here with their default value.

  def finalize_options(self):
    """Post-process options."""

  def run(self):
    from sphinx.apidoc import main
    """Run command."""
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    exit = main(['sphinx-apidoc', '-f', '-o', './docs', './lib'])
    self.run_command('build_sphinx')

```

There are two notes which you should pay attention to. One is that you should import sphinx inside `run` method. Because when this script is called, there could not the case when Sphinx is not installed your environment. Running command is always kicked after installing all dependencies. So importing inside `run` method does not cause such problem. And second is the question about why `run`
method is written like. The answer is inside the `sphinx-apidoc` command itself. This is here. Simple script.

```python
#!/usr/bin/python

# -*- coding: utf-8 -*-
import re
import sys

from sphinx.apidoc import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

Yes. All I did was copy and paste it.

These are the preparation. All your library codes are under `lib` directory. build-apidoc generate html files under `docs/html` with this command.

```bash
$ python setup.py build_apidoc
```

It is great to see a beautiful documentation of your project. It must make you motivated!

Thank you.
