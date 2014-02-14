---
layout: post
title: "SBTを使ったプロジェクト作成(2)"
date: 2013-09-10 21:23
comments: true
categories: 
---

### スコープに関するお話
昨日の続き。
実はSettingKeyにはスコープがあり、異なるプロジェクトではことなる値を使うことができる。そもそも同じ場所に置くなよという気はするがテスト用とかリリース用にビルドしたい場合に便利。このビルドの設定を分けるスコープの"軸"がSBTには３つある。

* プロジェクト
* コンフィギュレーション
* タスク

#### プロジェクト軸によるスコープ
それぞれのプロジェクトに対して設定が必要という場合がこのケース。ビルド全体（全プロジェクト）でもよい。

#### コンフィギュレーション軸によるスコープ
ビルドの種類によるわけかた。テストとかリリース用とか、デバッグ用とか。

#### タスク軸によるスコープ
少しよくわからないけれど、他のタスクに影響を受けるようなスコープのことらしい。

スコープは`inspect`コマンドで調べられるらしい。

```
$ sbt
> inspect name
[info] Setting: java.lang.String = hello
[info] Description:
[info]  Project name.
[info] Provided by:
[info]  {file:/Users/sasakiumi/MyWorks/hello/}default-6cbc7c/*:name
[info] Defined at:
[info]  /Users/sasakiumi/MyWorks/hello/build.sbt:1
[info] Reverse dependencies:
[info]  *:normalized-name
[info]  *:project-info
[info]  *:organization
[info]  *:description
[info]  *:on-load-message
[info] Delegates:
[info]  *:name
[info]  {.}/*:name
[info]  */*:name
>
```

`Provided by`で書かれた部分を見ると

* {file:/Users/sasakiumi/MyWorks/hello/}default-6cbc7c/ → プロジェクト
* アスタリスク → コンフィギュレーション
* →なし

ということらしい。

### ライブラリ依存性
SBTはプロジェクトが必要なライブラリとかパッケージを管理してくれる。この依存ライブラリの管理には２つのタイプがある。

#### アンマネージ依存性
libディレクトリに直にjarファイルを入れるタイプ。特に管理とかされているわけではなく自分でダウンロードして、設置する必要があるのでアンマネージ。lib以下に入れるとプロジェクトのクラスパスに追加される。それだけだ！

#### マネージ依存性
**Apache Ivy**を使ってライブラリの依存解決を行う。これを使うためには`libraryDependencies`キーに値を入れるだけでうまくいく。グループ、ライブラリ名、バージョンの順番だ。

``` scala
libraryDependencies += "org.apache.derby" % "derby" % "10.4.1.3"
```

これをbuild.sbtに書いて`update`を打つと大体うまくいく。でも時折、参照先のリポジトリに欲しいパッケージがない場合がある。この場合はSBTにリポジトリを追加してやらないといけない。

``` scala
solvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
```
`名前 at URL`というフォーマット。

### .scalaビルド設定
build.sbt以外にもproject/に置いたscalaファイルでビルド設定できる。
厳密にはbuils.sbtは結局project/以下のビルド設定にマージされることになるので、単なる略記法という意味以上のものはない。とはいっても便利。具体例で説明。

``` scala project/Build.scala
import sbt._
import Keys._

object HelloBuild extends Build {

    val sampleKeyA = SettingKey[String]("sample-a", "demo key A")
    val sampleKeyB = SettingKey[String]("sample-b", "demo key B")
    val sampleKeyC = SettingKey[String]("sample-c", "demo key C")
    val sampleKeyD = SettingKey[String]("sample-d", "demo key D")

    override lazy val settings = super.settings ++
        Seq(sampleKeyA := "A: in Build.settings in Build.scala", resolvers := Seq())

    lazy val root = Project(id = "hello",
                            base = file("."),
                            settings = Project.defaultSettings ++ Seq(sampleKeyB := "B: in the root project settings in Build.scala"))
}
```

次にbuild.sbt

``` scala build.sbt
sampleKeyC in ThisBuild := "C: in build.sbt scoped to ThisBuild"
sampleKeyD := "D: in build.sbt"
```

ここでsbtインタラクティブモードで`inspect sample-a`とうつ

``` scala bash
$ sbt
> inspect sample-a
[info] Setting: java.lang.String = A: in Build.settings in Build.scala
[info] Provided by:
[info]  {file:/home/hp/checkout/hello/}/*:sample-a
```
続いてsample-c

``` scala bash
> inspect sample-c
[info] Setting: java.lang.String = C: in build.sbt scoped to ThisBuild
[info] Provided by:
[info]  {file:/home/hp/checkout/hello/}/*:sample-c
```

`Provided by`で表示されるスコープは同じなため、.sbtと.scalaはどちらに何を設定しても同じということになる。

``` scala bash
> inspect sample-b
[info] Setting: java.lang.String = B: in the root project settings in Build.scala
[info] Provided by:
[info]  {file:/home/hp/checkout/hello/}hello/*:sample-b
> inspect sample-d
[info] Setting: java.lang.String = D: in build.sbt
[info] Provided by:
[info]  {file:/home/hp/checkout/hello/}hello/*:sample-d
```

`sample-b`は異なるスコープになっていることがわかる。これは`sample-d`に対応していることがわかる。

あとはプラグインとかの話しがあったけれど、ここらで自分なりにプロジェクトを作ってみたいと思う。
まとめのページはここ。このページもGitHub Pagesでできてるのか。

http://scalajp.github.io/sbt-getting-started-guide-ja/summary/
でも開発がそんなに活発でないかも。Epicの開発はほぼ停止してるみたいだし。