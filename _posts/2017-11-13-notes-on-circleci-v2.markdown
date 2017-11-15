---
title: "Notes on CircleCI v2"
layout: post
date: 2017-11-13 14:55:17 +0900
image: 'images/'
description:
tag: ["CircleCI", "CI"]
blog: true
author: "lewuathe"
---


[CircleCI 2.0](https://circleci.com/docs/2.0/) enables us to setup a flexible Docker environment and advanced caching mechanism to make your build faster. In order to make use of this new platform, I tried migrate our projects to CircleCI 2.0. But I had several pitfalls during this migration. So I'm going to clarify some points to be noted for those who are considering migration to CircleCI 2.0.

### Caching by checksum

You can specify the artifact to be cached by the key you give. For example, if you want to save maven local repository as cache, you can write like this:

```yaml
build:
  steps:
    - save_cache:
      paths:
        - ~/.m2
      key: my-cache-${CIRCLE_SHA1}

    - restore_cache:
      key: my-cache-${CIRCLE_SHA1}
```

But it does not make use of caching mechanism fully because CircleCI cannot a restore cache due to using `$CIRCLE_SHA1`. `$CIRCLE_SHA1` is a commit hash that is changed in every build, which means we cannot use the cache saved this time in next time. We found it was necessary to use more robust value as cache key. 

In this case, we know we can keep using the same cache unless the version of packages on which the my project depends is chaged. This version is specified in `pom.xml`. So it means we can keep using the same package unless `pom.xml` is not changed. We can achieve by writing like this:

```yaml
build:
  steps:
    - save_cache:
      paths:
        - ~/.m2
      key: my-cache-\{\{ checksum "pom.xml" \}\}

    - restore_cache:
      key: my-cache-\{\{ checksum "pom.xml" \}\}
```

Please ignore back slashes. Markdown does not work as expected. :( 
It looks like Jinja template. The detail is described [here](https://circleci.com/docs/2.0/caching/).

### PATH environment variable

Environment variables can be set like this:

```yaml
build:
  environment:
    - ENV_VAR1: VALUE1
    - ENV_VAR2: VALUE2
    - ENV_VAR3: VALUE3
```

But you should not set `PATH` environment variable here. [It](https://discuss.circleci.com/t/how-to-add-a-path-to-path-in-circle-2-0/11554) says: 

> You currently cannot evaluate a variable when setting another one, so the fix is to set it to the string that $PATH evals to at that point. You can just docker run -it imagename:version echo $PATH.

So if you set `PATH: $PATH:/some/to/path`, `$PATH` is not evaluatated properly. It's necessary to set in `steps`.

### Environment variable scope

`$PATH` environment variable can be set in `steps` section.

```yaml
build:
  steps:
    - run:
      name: Step 1
      command: |
        echo 'export PATH="$PATH:/path/to/somewhere"' >> ~/.bash_profile
        source ~/.bash_profile
```

But this environment variable is valid only in this step. In short, it is not took over next step unless you write explicitly. 

```yaml
build:
  steps:
    - run:
      name: Step 1
      command: |
        echo 'export PATH="$PATH:/path/to/somewhere"' >> ~/.bash_profile
        source ~/.bash_profile

    - run:
      name: Step 2
      command: |
      	echo $PATH # No /path/to/somewhere
```

We need to take care of the point too.

### Reference

* [CircleCI 2.0](https://circleci.com/docs/2.0/)
* [Caching](https://circleci.com/docs/2.0/caching/)
* [Using Environment Variables]https://circleci.com/docs/2.0/env-vars/

