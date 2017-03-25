---
title: "Config of CircleCI 2.0"
layout: post
date: 2017-03-25 18:27:13 +0900
image: 'images/'
description:
tag: ["CircleCI"]
blog: true
jemoji:
author: "lewuathe"
---

At the end of the last year, [CircleCI 2.0](https://circleci.com/beta-access/) was released as closed beta.
The main differences are described [here](https://circleci.com/docs/2.0/migrating-from-1-2/). So according to the migration guide, I want to make a list to be noted when you migrate your project toward CircleCI 2.0. Of course for myself.

## Config path

CircleCI refers `circle.yml` file as build configuration. In CircleCI 2.0, the config file was migrated to `.circleci/config.yml`.

> This allows you to test 2.0 builds on a separate branch, leaving any existing configuration in the old circle.yml style unaffected and running on the CircleCI 1.0 infrastructure in branches that do not contain .circleci/config.yml.

You don't need to remove existing `circle.yml` file because it has no conflict with CircleCI 2.0 config files. Thanks to creation of `.circleci` directory, we can even add more configs or resources required for build.

## circleci local command

You might have some experience to debug CI build by using SSH login. It is often difficult to create new project perfectly build on CircleCI without retrying. So `circleci` CLI makes it easier. If your project has already had CircleCI 2.0 configuration, the step is easy.

Install `circleci` CLI.

```
$ curl -o /usr/local/bin/circleci https://circle-downloads.s3.amazonaws.com/releases/build_agent_wrapper/circleci && chmod +x /usr/local/bin/circleci
```

Then build on local machine.

```
$ cd your-project
$ circleci build
```

Please check [here](https://circleci.com/docs/2.0/local-jobs/) more detail.

## Config migration

At the last I want to describe some migration point of config, which might be used in many times.

### Global environment

Global environment can be written in just under `jobs#build`. Basically all config of CircleCI 2.0 is written in `jobs#build`.

```
version: 2
jobs:
  build:
    working_directory: /tmp
    docker:
      - image: busybox
    environment:
       FOO: foo
       BAR: bar
```

### Languages

Languages should be specified by docker image. There are several [official images](https://hub.docker.com/explore/) in Docker Hub. So you might be able to find the best image to be used in your project.

```
version: 2
jobs:
  build:
    working_directory: /tmp

    # In 2.0, we specify our Ruby version by using a public Docker image
    docker:
      - image: ruby:2.3
```

### Tests and dependencies

All actual running steps are written in `jobs#build#steps`.

```
version: 2
jobs:
  build:
    working_directory: /root/my-project
    docker:
      - image: phusion/baseimage
    steps:
      # Ensure your image has git, otherwise the checkout step will fail
      - run: apt-get -qq update; apt-get -y install git

      # Checkout timing is no longer hardcoded, so this step can occur anywhere
      - checkout
      - run: git submodule sync && git submodule update --init # use submodules
```

`run` is used for writing actual command. What content can be written in `steps` are described [here](https://circleci.com/docs/2.0/configuration-reference/#steps). The most used ones are `run`, `checkout` The one thing to note is CircleCI 2.0 does not support automatic deployment so we need to write deployment process in `steps` section.

Actually our project is not migrated to CircleCI infrastructure. Since there are some merits of using CircleCI 2.0, I want to migrate. This is the part of my research how to migrate CI environment to CircleCI 2.0.

Please let me know if any other news of information to be cared about CircleCI 2.0. Thanks.
