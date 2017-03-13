---
layout: post
blog: true
title: "ScalaNLPのチュートリアル"
date: 2013-09-14 16:25
comments: true
categories: 
---

ScalaNLPを触ってみたので、その時のチュートリアル。
ScalaNLPは基本的にはSBTの依存解決でライブラリをダウンロードできるのでそのとおりに行う。
build.sbtファイルに以下のように書いてupdateを行う

``` scala 
libraryDependencies  ++= Seq(
            // other dependencies here
            // pick and choose:
            "org.scalanlp" % "breeze-math_2.10" % "0.4",
            "org.scalanlp" % "breeze-learn_2.10" % "0.4",
            "org.scalanlp" % "breeze-process_2.10" % "0.4",
            "org.scalanlp" % "breeze-viz_2.10" % "0.4"
)

resolvers ++= Seq(
            // other resolvers here
            // if you want to use snapshot builds (currently 0.5-SNAPSHOT), use this.
            "Sonatype Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots/",
            "Sonatype Snapshots" at "https://oss.sonatype.org/content/repositories/releases/"
)

// Scala 2.9.2 is still supported for 0.2.1, but is dropped afterwards.
scalaVersion := "2.10.2"
```

でも以下のようなエラーが出てくる。0.4がないとかいうエラーが出てくる。ないらしいのでバージョンを下げてみる。

```
libraryDependencies  ++= Seq(
            // other dependencies here
            // pick and choose:
            "org.scalanlp" % "breeze-math_2.10" % "0.3",
            "org.scalanlp" % "breeze-learn_2.10" % "0.3",
            "org.scalanlp" % "breeze-process_2.10" % "0.3",
            "org.scalanlp" % "breeze-viz_2.10" % "0.3"
)

resolvers ++= Seq(
            // other resolvers here
            // if you want to use snapshot builds (currently 0.5-SNAPSHOT), use this.
            "Sonatype Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots/",
            "Sonatype Snapshots" at "https://oss.sonatype.org/content/repositories/releases/"
)

// Scala 2.9.2 is still supported for 0.2.1, but is dropped afterwards.
scalaVersion := "2.10.2"
```

入ったみたい。
```
$ sbt
> console
[warn] Multiple resolvers having different access mechanism configured with same name 'Sonatype Snapshots'. To avoid conflict, Remove duplicate project resolvers (`resolvers`) or rename publishing resolver (`publishTo`).
[info] Compiling 1 Scala source to /Users/sasakiumi/MyWorks/scalanlp-tutorial/target/scala-2.10/classes...
[info] 'compiler-interface' not yet compiled for Scala 2.10.2. Compiling...
[info]   Compilation completed in 20.07 s
[info] Starting scala interpreter...
[info]
Welcome to Scala version 2.10.2 (Java HotSpot(TM) 64-Bit Server VM, Java 1.6.0_51).
Type in expressions to have them evaluated.
Type :help for more information.

scala> import breeze.linalg._
import breeze.linalg._

```

[ここ](http://krrrr.hatenablog.com/entry/20130614/1371221935)を参考に基本的な演算の書き方を見てみる。

```
package com.github.PhysicsEngine.scalanlptutorial
import breeze.linalg._
import breeze.numerics._

object App {
  def main(args: Array[String]) {
    // 4*4 matrix
    val T = DenseMatrix((.0, .0, .0, .0), (1.0, .0, .5, .0), (.0, 1.0, .0, .0), (.0, .0, .5, .0))

    val d = 0.85

    // Row number of T matrix
    val N = T.rows
    // Transposed matrix of [1/N, 1/N, 1/N, 1/N, 1/N] 
    var r = DenseMatrix(Array.fill(N)(1.0/N)).t
			  
    val u = r.copy
				  
    val m = 20
						  
    for(i <- 1 to m){
	  r = d*T*r + (1-d)*u
    } 
						  
    print(r)
  }

}

```

#### 縦ベクトル
```
val x = DenseVector[Double](1,2,3,4,5)
```

#### 横ベクトル
```
val x = DenseVector[Double](1,2,3,4).t
```

#### N＊N行列
```
val x = DenseMatrix((1.0,2.0,3.0), (4.0,5.0,6.0), (7.0,8.0,9.0))
```
行数と列数は
```
(x.rows, x.cols)
```
行の取得、列の取得には`::`を使う
```
x(::,2) // 2列目
x(1, ::) // 1行目
```
部分取得したい場合には`to`を使う
```
x(0 to 1, 1 to 2) //0行から1行、1列から2列で囲まれた部分を返す
```

#### 行列に定義された四則演算
```
x + y
x * y
x - y
```

#### 要素ごとの四則演算
```
x :+ 1.0  // 全要素に1.0を加える
x :* 2.0  // 全要素に2.0をかける
x :- 3.0  // 全要素から3.0を引く
```

#### 内積
```
x dot y
```

そのほかの使い勝手の良さそうなドキュメントは[ここ](https://github.com/scalanlp/breeze/wiki/Breeze-Linear-Algebra)




