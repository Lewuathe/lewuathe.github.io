---
title: "Environment Variable in IntelliJ IDEA"
layout: post
date: 2018-05-29 21:34:07 +0900
image: 'cards.jpg'
description:
tag: ["IntelliJIDEA", "IDE", "Shell", "Scala", "sbt"]
blog: true
author: "lewuathe"
---

You may have some build script that reads environment variable such as security credentials or custom configuration. That is often the case when you use some private repositories shared only inside the company.
Most build tools can recognize the environment variable. For example, you can write Artifactory credential in `built.sbt` like this. 

```scala
val credentials = Credentials(
  "Artifactory Realm",
  "artifactoryonline.com",
  sys.env.getOrElse("ARTIFACTORY_USERNAME", ""),
  sys.env.getOrElse("ARTIFACTORY_PASSWORD", "")
)
```

sbt properly uses the credential and download the required dependencies to the local cache. That's a very common situation we are facing in the daily development. It's not amazing. 

But when I tried to run the sbt from IntelliJ IDEA, it did not work. It could not download the dependencies from Artifactory online as expected. Why?

The reason was that my IDE did not launch as a child process of the main shell. These environment variables are set only in my login shell. 
So I have to launch IDE from my login shell to recognize environment variables. But how?

IntelliJ provides a useful command named `idea` which enables us to launch your IDE from the console. The process is launched as a child process of the process we run the command.
Just running `idea` in the login shell, the IDE can finally recognize the environment variables as expected.