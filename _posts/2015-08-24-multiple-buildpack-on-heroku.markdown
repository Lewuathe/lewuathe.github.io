---
layout: post
blog: true
title: "Multiple buildpack on Heroku"
date: 2015-08-24 20:30:02 +0900
comments: true
categories: ["Heroku"]
author: Kai Sasaki
---

I usually use [Heroku](https://www.heroku.com/) when I join some Hackathon. This is the easiest service the I've ever used as we can deploy my application with `git` command which is friendly tool I always use. So we can deploy a web application or API service in short time.

<!-- more -->
Yesterday, I took part in [Music HackDay Tokyo 2015](http://www.musichackday-tokyo.org/). At this hackathon, I struggled create environment which includes python packages, node packages and also ffmpeg binaries. This type of environment cannoe be achieved by default configuration. We have to write some [buildpacks configurations](https://devcenter.heroku.com/articles/buildpacks) under your project.

## heroku-buildpack-multi

When you want to install multiple buildpacks in your environment(In case of me, there are nodejs, python and ffmpeg.) You have to first import [heroku-buildpack-multi](https://github.com/heroku/heroku-buildpack-multi) into your project.

```
$ heroku buildpacks:set https://github.com/heroku/heroku-buildpack-multi.git
```

With this description, you can write multi buildpacks into your `.buildpacks`. At this time, I wrote like below.

```
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
https://github.com/heroku/heroku-buildpack-nodejs.git
https://github.com/heroku/heroku-buildpack-python.git
```

Each buildpacks install main packages and resolve dependencies. In terms of nodejs, this is with `npm install`. And python, you should write dependencies in `requirements.txt`. The details are written in [nodejs dependencies](https://devcenter.heroku.com/articles/node-best-practices#declare-all-dependencies) and [python dependencies](https://devcenter.heroku.com/articles/python-pip).

With these configuration, you can run your application on nodejs, python and ffmpeg environment. The whole project I wrote at this hackathon is [here](https://github.com/PhysicsEngine/SoundLine-server). If you have any question about this project and configurations, feel free to post issues to [here](https://github.com/PhysicsEngine/SoundLine-server/issues/new). I'll write a post about this project and what I made at Music Hack day. T

Thank you.
