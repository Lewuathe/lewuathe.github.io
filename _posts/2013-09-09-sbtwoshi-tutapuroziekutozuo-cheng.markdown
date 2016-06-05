---
layout: post
blog: true
title: "SBTを使ったプロジェクト作成(1)"
date: 2013-09-09 21:29
comments: true
categories:
---

SBT(Simple Build Tool)というScalaのビルドツールを使ってみる。
[ここ](http://scalajp.github.io/sbt-getting-started-guide-ja/)を参考にした。

### インストール

まずインストール。macの場合はHomebrewで用意されているみたい。

```
$ brew install sbt
```

### プロジェクトの作成

ひな形は自分で作る。ここではhelloプロジェクトを作ってみる。

```
$ mkdir hello
$ echo 'object Hi { def main(args: Array[String]) = println("Hi!") }' > hw.scala
$ sbt
# ここで必要なパッケージとか勝手にインストールしてビルドしてくれるみたい
> run
・・・
Hi!
```

複雑なことはまだたくさんあるけれど、必要なことはこれだけだ。あとは蛇足と後学のため。でもきっと大事なことだ。

### ソースコード
sbtではソースツリーはMavenと同じものを使うらしい。Maven知らない。

```
hello/
 build.sbt  (パッケージのmeta情報とかここにまとめる)
 project/
   Build.scala (ビルド設定とかここに書く。Makefileみたいなもの？)
 src/
   main/
     resources/
        <メインの jar に含むファイル>
     scala/
        <メインの Scala ソース>
     java/
        <メインの Java ソース>
   test/
     resources/
        <テストの jar に含むファイル>
     scala/
        <テストの Scala ソース>
     java/
        <テストの Java ソース>
```

これ以外は無視されるらしい。sbtコマンドでビルドが終わるとここにtargetディレクトリが追加されて、そこにできたclassファイルとかjarファイルが置かれる。Gitで管理したいなら`.gitignore`にはこう書くのが定石らしい。
```
target/
```

### インタラクティブモード
sbtを引数なしで実行するとインタラクティブモードになる。さっき`>`が出てきて`run`と打ったらところで見ているはずだ。インタラクティブモードでは`compile`とか`run`が使える。みたまんまだ。

### バッチモード
コマンド（さっきインタラクティブモードで一個一個打ってたやつ）を一度に実行できる。引数も与えられる。（test-onlyにはtestAとtestBを引数に与えている）
```
$ sbt compile run "test-only testA testB"
```

### 継続的ビルド
ソースファイルの変更をトリガーに実行したければコマンドの先頭に`~`をつける。例えばインタラクティブモードで以下のようにすると、ソースをいじるたびに勝手にコンパイルしてくれるようになる。
```
> ~ compile
```

* `clean`: targetの削除 `make clean`みたいなもの
* `compile`: コンパイルする
* `test`: コンパイルして実行
* `console`: コンパイル済のソースを依存ライブラリにパスを通してscalaインタプリタに入る
* `run`: プロジェクトのメインクラスを実行
* `package`:  src/main/resources 内のファイルと src/main/scala からコンパイルされたクラスを含む jar を作る

### build.sbtの書き方
ここで何書いていいかわからなかった大事なbuild.sbtが出てくる。
はじめの方に書いたけれどビルド定義にはbuild.sbtとproject/*.scalaの２通りがある。ただ慣例的にはメインでbuild.sbtを使いそれでできないことを*.scalaファイルで行うことが多いらしい。さてビルド定義。

#### ビルド定義って？

プロジェクトを調べ、全てのビルド定義ファイルを処理した後、sbt は、ビルドを記述した不可変マップ（キーと値のペア）を最終的に作る。例えば、name というキーがあり、それは文字列の値、つまり君のプロジェクト名に関連付けられる。
ビルド定義ファイルは直接には sbt のマップに影響を与えない。その代わり、ビルド定義は、型が Setting[T] のオブジェクトを含んだ巨大なリストを作る。 T はマップ内の値の型だ。（Scala の Setting[T] は Java の Setting<T> と同様。） Setting は、新しいキーと値のペアや、既存の値への追加など、マップの変換を記述する。 （関数型プログラミングの精神に則り、変換は新しいマップを返し、古いマップは更新されない。）
build.sbt では、プロジェクト名の Setting[String] を以下のように作る:

name := "hello"

この Setting[String] は name キーを追加（もしくは置換）して "hello" という値に設定することでマップを変換する。 変換されたマップは新しい sbt のマップとなる。マップを作るために、sbt はまず、同じキーへの変更が一緒に起き、かつ他のキーに依存する値の処理が依存するキーの後にくるように Setting のリストをソートする。 次に、sbt はソートされた Setting のリストを順番にみていって、一つづつマップに適用する。

まとめ: ビルド定義は Setting[T] のリストを定義し、Setting[T] は sbt のキー・値ペアへの変換を表し、T は値の型を指す。

何言ってるかわからない。
例えば最初の方に出てきた`build.sbt`はこんなだった。

``` scala
name := "hello"

version := "1.0"

scalaVersion := "2.9.1"
```
これは`:=`の左側がSetting[T]型のオブジェクトで右側がその値だ。これらの値は組み込み型で型が決まっているので
``` scala
name := 42
```
とやるとコンパイルしてくれないそうな。
キーの種類にはSettingとTaskがあり、nameとかversionはSetting。packageとかcompileはTaskとなる。なんだかまだ良くわからないけれど、設定値と実行命令みたいなものに２種類を設定できるっぽい。
ライブラリ依存性とかを書く場合はこんな感じ。ほうほう。

``` scala
libraryDependencies += "org.apache.derby" % "derby" % "10.4.1.3"
```

今日は一旦このへんで。
