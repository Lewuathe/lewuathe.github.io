---
layout: post
blog: true
title: "Run Spark Local Machine"
date: 2015-01-23 20:20:31 +0900
comments: true
categories: ["Spark"]
author: Kai Sasaki
---

From [Spark 1.2.0](https://spark.apache.org/docs/latest/index.html), it seems to be different from older version
when you want to run your spark job on your local machine. Before v0.9.2 you can run standalone job with such code.

```scala
/*** SimpleApp.scala ***/
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object SimpleApp {
  def main(args: Array[String]) {
    val logFile = "$YOUR_SPARK_HOME/README.md" // Should be some file on your system
    val sc = new SparkContext("local", "Simple App", "YOUR_SPARK_HOME",
    List("target/scala-2.10/simple-project_2.10-1.0.jar"))
    val logData = sc.textFile(logFile, 2).cache()
    val numAs = logData.filter(line => line.contains("a")).count()
    val numBs = logData.filter(line => line.contains("b")).count()
    println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
  }
}
```

You can run this app with sbt command.

```
$ sbt run
```

That's fine. But with latest version, you cannot find no more such documentation. I think spark does not anticipate
the use case with sbt standalone running. So [current version](https://spark.apache.org/docs/latest/quick-start.html#self-contained-applications) looks like below.
SBT section has been totally changed and you should submit jar file to your local spark. But I found a way to run spark job
by using sbt command with some changes. There are two major changes.

* Must add master configuration
* SparkContext should be stopped

I add these code to original one. This is the working one.

```scala
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object SimpleApp {
  def main(args: Array[String]) {
    val logFile = "YOUR_SPARK_HOME/README.md" // Should be some file on your system
    val conf = new SparkConf().setAppName("Simple Application")
      .setMaster("local[2]") // Set master configuration for local
    val sc = new SparkContext(conf)
    val logData = sc.textFile(logFile, 2).cache()
    val numAs = logData.filter(line => line.contains("a")).count()
    val numBs = logData.filter(line => line.contains("b")).count()
    println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
    sc.stop() // Stop SparkContext
  }
}
```

With these two lines, you can run sbt command.
