---
title: "Changing Python Version in Poetry with Pyenv"
layout: post
date: 2023-03-24 16:10:09 +0900
image: 'assets/img/posts/2023-03-24-changing-python-version-in-poetry-with-pyenv/catch.jpg'
description:
tag: ['Python', 'CLI']
blog: true
author: "Kai Sasaki"
---

# Introduction
If you're a Python developer who uses Poetry to manage your project dependencies and Pyenv to manage multiple Python versions, you may want to change the Python version that Poetry is using. This can be a bit confusing at first, but with the right steps, it can be done quickly and easily. In this post, we'll show you how to change the Python version that Poetry uses if you're using Pyenv.

# Prerequisites:
Before we begin, make sure you have the following prerequisites:

- Poetry installed on your machine
- Pyenv installed on your machine
- At least two Python versions installed with Pyenv

# Steps

Open your terminal and navigate to the directory of your project.

Check which Python version Poetry is currently using by running the following command:

```bash
$ poetry run python --version
```

This will show you the current Python version that Poetry is using.

Check which Python versions are installed with Pyenv by running the following command:

```bash
$ pyenv versions
```

This will show you a list of all the Python versions installed with Pyenv. To sync the version used by Poetry with the one by Pyenv, we can enable the following option.

```bash
$ poetry config virtualenvs.prefer-active-python true
```

Choose the Python version you want to use with Poetry and set it as the global version by running the following command:

```bash
$ pyenv global <PYTHON_VERSION>
```

Replace <PYTHON_VERSION> with the version of Python you want to use.

Verify that the global Python version has been changed by running the following command:

```bash
$ python --version
```

This will show you the current Python version that your system is using.

Verify that Poetry is now using the correct Python version by running the following command:

```bash
$ poetry run python --version
```

This should show you the version of Python you set in step 4.

If you need to switch back to a different Python version, repeat steps 4-6 with the version you want to switch to.

# Conclusion:
In this post, we've shown you how to change the Python version that Poetry is using if you're using Pyenv to manage multiple Python versions. By following these steps, you can easily switch between different Python versions and ensure that your project is using the correct version of Python.

See more detail in [the official document](https://python-poetry.org/docs/managing-environments/).