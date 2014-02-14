---
layout: post
title: "SBTとEclipseでScala開発環境"
date: 2013-09-13 22:17
comments: true
categories: 
---

SBTの使い方がなんとなくわかってきたので、今度はEclipseにSBTプロジェクトを導入してみる。

### Eclipse plubin for SBTのinstall
プロジェクトに必要なプラグインをインストールする。この場合は`project/plubins.sbt`に以下のように記述する。

``` scala
resolvers += Classpaths.typesafeResolver

addSbtPlugin("com.typesafe.sbteclipse" % "sbteclipse-plugin" % "2.1.2")
```

ここで以下のコマンドを打てばこのプラグインがインストールされ、Eclipseプロジェクトに必要な.projectファイルができあがる
```
$ sbt eclipse
```

これをImportすればいい。Importの方法は
```
File -> Import -> General -> Existing Projects into Workspace
```
でできる。

あともっと便利にSBTを使いたければ[ここ](http://d.hatena.ne.jp/qtamaki/20121210/1355167655)に書いてある通りにやるとテンプレート展開のためのライブラリとかも入れられる。(g8っつうらしい)

でもどうやら実行とかテストはSBT上でやった方がいいみたい。Eclipseは純粋なエディタとして使う人が多いっぽい。
確かにJavaのプロジェクトと認識されてしまってうまくコンパイルできないや。



