---
title: "Exclude package by organization in sbt"
layout: post
date: 2017-10-11 20:54:18 +0900
image: 'images/'
description:
tag: ["sbt", "Scala"]
blog: true
author: "lewuathe"
---

In order to exclude some dependencies in [sbt](http://www.scala-sbt.org/) project, we can use `exclude` or `excludeAll` method in `build.sbt` file. 

```scala
libraryDependencies ++= Seq(
	"org.scalatest" % "scalatest_2.11" % "2.2.0" exclude("org.slf4j", "slf4j-jdk14")
)
```

While we can pass direct organization and name of package to be exclude to `exclude` method,  `excludeAll` can receive some pattern or rule to be excluded. For example, if you want to exclude all package under `org.slf4j` organization, you can create such rule.

```scala
val excludeSlf4jBinding = ExclusionRule(organization = "org.slf4j")

libraryDependencies ++= Seq(
	"org.scalatest" % "scalatest_2.11" % "2.2.0" excludeAll(excludeSlf4jBinding)
)
```

This is pretty simple way to exclude multiple transitive dependencies. Of course you can pass muitple rule to `excludeAll` method.

```scala
libraryDependencies ++= Seq(
	"org.scalatest" % "scalatest_2.11" % "2.2.0" excludeAll(
		ExclusionRule(organization = ...),
		ExclusionRule(organization = ...),
		ExclusionRule(organization = ...)
	)
)
```

Please see [sbt reference manual](http://www.scala-sbt.org/0.13/docs/Library-Management.html#Exclude+Transitive+Dependencies) in more detail.




