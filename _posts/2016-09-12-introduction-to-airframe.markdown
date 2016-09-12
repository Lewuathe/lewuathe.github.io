---
title: "Introduction to Airframe"
layout: post
date: 2016-09-12 21:29:13 +0900
image: 'images/'
description:
tag: ['Scala', 'Airframe']
blog: true
jemoji:
author: 'lewuathe'
---

Do you have any experience of using DI container framework for your Scala project? The most famous DI container frameworks is [Google Guice](https://github.com/google/guice).
This library is widely adapted in enterprise and open source community. Since it is defact standard library, it is the best option to select Guice as your
DI framework in Java project.

<!-- more -->

How about Scala project? Of course Scala project can be integrated with Java libraries and frameworks seamlessly. But isn't there any other way
to do DI in more Scala-style way? So that's the reason why I write this post. [Airframe](https://github.com/wvlet/airframe) is a library to enable us to do DI more
sophisticated way in Scala project. You can write DI code easily without violating Scala style in your project.
In this post, I'd like to introduce how to use Airframe in your Scala project.

## Install

Like other Scala libraries, you can install by adding sbt dependencies. The latest version is 0.7.

```scala
libraryDependencies += "org.wvlet" %% "airframe" % "0.7"
```

## Overview

You can inject an object through `trait` in Scala as `interface` or `abstract class` in Guice. Injecting can be done with `bind` method.
Dependency graph of each object is created by `Session` in Airframe. It can be regarded as `Injector` in Guice. Since `Session` is created by
`Design`, `Design` is corresponding to `Module` in Guice. So overall we show a list of correspondence of objects and methods between Airframe and Guice.


|| Guice | Airframe |
|:---|:---:|:---:|
|Injecting | `inject` | `bind` |
|Keeping dependency graph|`Module`|`Design`|
|Creating object with resolving dependency|`Injector`|`Session`|

Except for the name difference, the usages are almost same between Airframe and Guice.
Let's see the usage of Airframe next. The whole code can be found in [example](https://github.com/wvlet/airframe/blob/master/src/test/scala/example/Example.scala).

## Usage

First let's define a trait which is injected by Airframe.
Let's assume building a airplane with various type of components.


```scala
import wvlet.airframe._
trait Left   // Representation of left wing
trait Right  // Representation of right wing
case class Wing(name:String) {
  override def toString = f"Wing($name:[${hashCode()}%x])"
}
```

We define metrics object in order to collect information of each component.

```scala
trait Metric {
  def report(key:String, value:Int)
}

object EmptyMetric extends Metric {
  override def report(key: String, value: Int): Unit = {}
}

object MetricLogging extends Metric with LogSupport {
  override def report(key: String, value: Int): Unit = {
    warn(s"${key}:${value}")
  }
}

// Plane type which keeps fuel tank size
case class PlaneType(tankSize:Int)
```

Next we will define other components which depends on `Metric` and `PlaneType`. We can use Airframe
binding instead of specifying concrete implementation here.

```scala
trait Fuel {
  // Get a PlaneType with resolving dependency graph.
  lazy val planeType = bind[PlaneType]
  var remaining: Int = planeType.tankSize * 10
  // Get a Metric object.
  val metric = bind[Metric]

  def burn(r:Int) {
    metric.report("energy.consumption", r)
    remaining -= r
  }
}

trait Engine {
  val engineType: String
  // Get a Fuel object from Airframe design session.
  val fuel = bind[Fuel]

  def run(energy:Int)
}
```

Since `Fuel` and `Engine` are defined as `trait`, we can bind any implementation of these traits
at creating design session. So let's define some type of `Engine`s.

```scala
trait GasolineEngine extends Engine with LogSupport {
  val engineType = "Gasoline Engine"

  def run(energy:Int) {
    // Fuel implementation is fetched Airframe session
    fuel.burn(energy)
  }
}

case class SolarPanel() {
  def getEnergy : Int = {
    Random.nextInt(10)
  }
}

trait SolarHybridEngine extends Engine with LogSupport {
  val engineType = "Solar Hybrid Engine"
  val solarPanel = bind[SolarPanel]

  def run(energy:Int) {
    val e = solarPanel.getEnergy
    info(s"Get ${e} solar energy")
    fuel.burn(math.max(0, energy - e))
  }
}
```

Now all components needed for creating an airplane are completed to be defined. Airplane design graph can be like below.

```scala
trait AirPlane extends LogSupport {
  // Binded object with tag.
  val leftWing  = bind[Wing @@ Left]
  val rightWing = bind[Wing @@ Right]
  val engine = bind[Engine]

  info(f"Built a new plane left:${leftWing}, right:${rightWing}, fuel:${engine.fuel.remaining}, engine:${engine.engineType}")

  def start {
    engine.run(1)
    showRemainingFuel
    engine.run(10)
    showRemainingFuel
    engine.run(5)
    showRemainingFuel
  }

  def showRemainingFuel : Unit = {
    info(s"remaining fuel: ${engine.fuel.remaining}")
  }
}
```

One interesting thing to note here is tagged object binding. You can bind different object instance against same class type.
In this case, `leftWing` and `rightWing` are different object instance even if they are same class.
It can be realized by object tagging provided by [wvlet](https://github.com/wvlet/wvlet).

Dependency graph can be created by constructing `Design` as described previously.

```scala
// This is a base design.
val coreDesign =
  newDesign
  .bind[Wing @@ Left].toInstance(new Wing("left"))   // Binding with Left tag
  .bind[Wing @@ Right].toInstance(new Wing("right")) // Binding with Right tag
  .bind[PlaneType].toInstance(PlaneType(50))         // Initial tank size is 50 * 10
  .bind[Metric].toInstance(EmptyMetric)              // Binding to an instance

// Add an engine implementation to base design.
val simplePlaneDesign =
  coreDesign
  .bind[Engine].to[GasolineEngine]

// Add an engine and plane type implementation to base design.
val hybridPlaneDesign =
  coreDesign
  .bind[PlaneType].toInstance(PlaneType(10)) // Use a smaller tank (10 * 10)
  .bind[Engine].to[SolarHybridEngine]
```

Design defined components whic are used to resolve dependency graph for creating a object.
Creating object can be done by `build` method of `Session`.

```scala
val simplePlane = simplePlaneDesign.newSession.build[AirPlane]
simplePlane.start
```

This code's output is like this.

```
[Example$AirPlane] [info] Built a new plane left:Wing(left:[6ce65b1f]), right:Wing(right:[f2c0f1af]), fuel:500, engine:Gasoline Engine  - (Example.scala:73)
[Example$AirPlane] [info] remaining fuel: 499  - (Example.scala:85)
[Example$AirPlane] [info] remaining fuel: 489  - (Example.scala:85)
[Example$AirPlane] [info] remaining fuel: 484  - (Example.scala:85)
```

We can see this plane uses `GasolineEngine` as defined Airframe design.
When we use `hybridPlaneDesign`, the implementation of AirPlane is different.

```
[Example$AirPlane] [info] Built a new plane left:Wing(left:[6ce65b1f]), right:Wing(right:[f2c0f1af]), fuel:100, engine:Solar Hybrid Engine  - (Example.scala:73)
[Example$SolarHybridEngine] [info] Get 3 solar energy  - (Example.scala:103)
[Example$AirPlane] [info] remaining fuel: 100  - (Example.scala:85)
[Example$SolarHybridEngine] [info] Get 0 solar energy  - (Example.scala:103)
[Example$AirPlane] [info] remaining fuel: 90  - (Example.scala:85)
[Example$SolarHybridEngine] [info] Get 7 solar energy  - (Example.scala:103)
[Example$AirPlane] [info] remaining fuel: 90  - (Example.scala:85)
```

In addition to changing `Engine`, Fuel tank size becomes smaller.

## Recap

Airframe enables us to do DI more easily in Scala like way. Airframe provides not only these
functionalities but also building singleton, eagler singleton and lifecycle management etc. I want
to explain these advanced features of Airframe if get a chance. Last but not least, Airframe is actively
under development and distributed under Apache-2.0 license. Please give us any feedback and issues on [GitHub](https://github.com/wvlet/airframe/issues).

Thanks!
