---
layout: post
blog: true
title: "Build SparkR"
date: 2015-09-25 13:18:19 +0900
comments: true
categories: ["Spark"]
author: Kai Sasaki
---

[Apache Spark](https://spark.apache.org/docs/latest/index.html) includes [R](https://www.r-project.org/) API. If you are a developer of Spark, you will have a time to change API or implementation of Spark core and MLlib. In this case, you also have to change SparkR test codes. (And also you may have to change Java API test cases too.)
But I had no experience to use R on my mac. So I wrote the process in this time.

<!-- more -->

## Installing R

You can use [Homebrew](http://brew.sh/index_ja.html) to install R package on MacOSX.

```bash
$ brew tap homebrew/science
$ brew install R
```

## Installing testthat package

First install `testthat` package from R console. This package is required by SparkR test code.

```bash
$ R

R version 3.2.2 (2015-08-14) -- "Fire Safety"
Copyright (C) 2015 The R Foundation for Statistical Computing
Platform: x86_64-apple-darwin14.5.0 (64-bit)

R is free software and comes with ABSOLUTELY NO WARRANTY.
You are welcome to redistribute it under certain conditions.
Type 'license()' or 'licence()' for distribution details.

Natural language support but running in an English locale

R is a collaborative project with many contributors.
Type 'contributors()' for more information and
'citation()' on how to cite R or R packages in publications.

Type 'demo()' for some demos, 'help()' for on-line help, or
'help.start()' for an HTML browser interface to help.
Type 'q()' to quit R.
> install.packages('testthat')
```

## Build SparkR packages.

Next in order to run test code of SparkR, you have to build Spark with R codes. The only thing you have to do is attach `sparkr` profile when you build Spark.

```bash
$ build/mvn -Pyarn -Phadoop-2.6 -Dhadoop.version=2.6.0 -Psparkr -DskipTests clean package
```

## Run test
In Spark, there is already test script for SparkR package. So the last thing you have to do is running this script from command line.

```bash
$ R/run-tests.sh
```

That's all! Thank you.
