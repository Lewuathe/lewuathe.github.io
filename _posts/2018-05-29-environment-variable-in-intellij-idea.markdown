---
title: "Environment Variable in IntelliJ IDEA"
layout: post
date: 2018-05-29 21:34:07 +0900
image: 'cards.jpg'
description:
tag: ["IntelliJ IDEA", "IDE", "Shell"]
blog: true
author: "lewuathe"
---

You may have some build script that reads environment variable like security credentials or custom configuration. 
Most build tools can recognize the environment variable. For example, you can write Artifactory credential in `built.sbt` like this. 

```scala
val credentials = Credentials(
  "Artifactory Realm",
  "artifactoryonline.com",
  sys.env.getOrElse("ARTIFACTORY_USERNAME", ""),
  sys.env.getOrElse("ARTIFACTORY_PASSWORD", "")
)
```

sbt properly uses the credential and download required dependencies to local cache. It's not amazing. 

But when I tried to run the sbt from IntelliJ IDEA, it did not work. It could not download the dependencies from Artifactory online as expected. Why?

The reason was that my IDE did not launch as child process of the main shell. These environment variables are set only in my login shell. 
So I have to launch IDE from my login shell to recognize environment variables. But how?

IntelliJ provides a useful command named `idea` which enables us to launch your IDE from the console. The process is launched as child process of the process we run the command.
Just running `idea` in login shell, the IDE can finally recognize the environment variables as expected.

  
  


