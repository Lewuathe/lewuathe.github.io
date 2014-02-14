---
layout: post
title: "Neo4jの使い方(1)"
date: 2013-09-20 21:33
comments: true
categories: 
author: Kai Sasaki
---


Neo4jを使ってみたよ。とりあえず触ってみたかったのでインストールはせずに[GraphGist](http://gist.neo4j.org/)を使ってCypherの書き方を勉強してみた。

# Cypherって？
グラフデータベースを操作するためのSQLのこと。他のグラフデータベースに利用されているのかは知らないけれどNeo4jに関してはこのCypherを使ってデータを操作する。SQLを知らないとMySQLに対して何もできないのと同じようにCypherを知らないとNeo4jを何もできない。今回はこのCypherの基本的な構文や書き方を書いてみる。

本家のドキュメントは[ここ](http://docs.neo4j.org/chunked/milestone/cypher-query-lang.html)だよ

# ノードの作成

```
CREATE (n:Actor {name:"Doraemon"})
```

Actorは型。nameは属性。nはマッチさせるときの記述子

## エッジの作成

```
MATCH (actor:Actor)
WHERE actor.name = "Doraemon"
CREATE (n:Actor {name:"Nobita"})
CREATE (actor)-[:HELP]->(n)
```

Actor型の中でnameがDoraemonのものを探す。見つけたらNobitaを作成し、その間にHELP型のエッジを作成する。

## UNIQUEで作成する
エッジを同じものを複製したくなければ`CREATE UNIQUE`を使う

```
MATCH (actor:Actor)
WHERE actor.name = "Doraemon"
CREATE UNIQUE (actor)-[r:ACTED_IN]->(movie:Movie {title:"Mugen Sankenshi"})
RETURN r;
```

## 属性の変更

```
MATCH (actor:Actor)
WHERE actor.name = "Doraemon"
SET actor.birth_year = 2020
RETURN actor.name, actor.birth_year;
```

## 全てのノードの列挙

```
MATCH (actor:Actor)
RETURN actor as `All Actors`;
```

# パターンマッチ
グラフデータベースの検索は基本的にパターンマッチを使って行う。既にいくつか出てきたけれどパターンマッチには`MATCH`文を使う。

## エッジのマッチ

```
(a)-[r]->(b)
```

ノードは丸括弧で囲み、エッジは角括弧で囲む。

```
(a)-[r:HELP]->(b)
```

型にもマッチさせたいときに型も書く。
無向グラフであれば矢印にはしない.

```
(a)--(b)
```

複数のタイプにorでマッチさせたいときには縦棒を使う

```
(a)-[r:TYPE1|TYPE2]->(b)
```

## Optional relationship
マッチしない場合にはその要素だけnullを返して欲しい場合には`?`を使う。

```
START me = node(*)
MATCH (me)-->(friend)-[?]->(friend_of_friend)
RETURN friend,friend_of_friend
```

この場合にはこの関係にマッチしないノードがあった場合にはそこの欄だけnullになる。関係があるかないかまだわからないけれど、とりあえずすべての見てみたい場合に有効。

エッジの個数を指定したい場合は`*`を使う

```
START me = node(4)
MATCH (me)-[?*2]->(friend)
RETURN friend
```

自分から２つ関係をまたいだ友達だけ返す。範囲指定も可能。

```
START me = node(4)
MATCH (me)-[?*2..4]->(friend)
RETURN friend
```

2から4までの関係をまたいだ友達。

## パスの割り当て
マッチしたパスを見たい場合があるときは、そのまま代入させてしまえばいい。

```
START me = node(3)
MATCH p1 = (me)-[*2]-(friendOfFriend)
CREATE p2 = (me)-[:MARRIED_TO]->(wife {name:"Gunhild"})
CREATE UNIQUE p3 = wife-[:KNOWS]-friendOfFriend
RETURN p1,p2,p3
```

# 参照構文
要素の検索、参照に必要な４つの構文(START, MATCH, WHERE, RETURN)に関して

## START
STARTは探索を行うためのアンカーとなるノード、またはエッジを決める構文。

以下のようなグラフがあったときに

```
START n = node(1)
```

と書くとnにnodeの1がバインドされ、これを使って探索することが可能。

![Graphの例](/images/posts/2013-09-20-neo4j-1/graph.png)

複数ノード、または全てのノードに対して処理を行いたい場合はこんな感じ。

```
START n = node(1,2,3)
RETURN n
```

```
START n = node(*)
RETURN n
```


アンカーとなるエッジをバインドさせたい場合は以下のように書く。

```
START r = relationship(0)
RETURN r
```

複数の点から始めるにはこんな感じ。(このやり方が知りたかった)

```
START a = node(1), b = node(2)
RETURN a,b
```

## MATCH
nodeやエッジにパターンマッチさせるための構文。
STARTなしでもMATCHは使えることはさっき書いたけれど、この場合でのどちらにしろCypherはすべてのノードを探索して始点となるノードを探すことになる。

すべてのノードを得たい場合は簡単。CypherはSTARTを指定しなければすべてのノードを探索するので、条件がなければすべてのノードにマッチする。

```
MATCH n
RETURN n
```

ラベルにマッチさせたいときはコロンで区切る

```
MATCH n:Actor
RETURN n
```

エッジもマッチに含めてよい

```
MATCH (director)-->(movie)
WHERE director.name = "Oliver Stone"
RETURN movie.title
```

エッジにラベルをマッチさせてもよい

```
MATCH (movie)<-[r:ACTED_IN]-(actor)
WHERE actor.name = "Tom Hanks"
RETURN movie.title
```

エッジの数でマッチさせることもできる

```
MATCH (martin)-[:ACTED_IN*1..2]-(x)
WHERE martin.name = "Martin Sheen"
RETURN x
```

## WHERE 
MATCHで引っかかったものをfilterにかける処理を行う文

```
MATCH n
WHERE n.name = "Takeshi" XOR (n.age < 30 AND n.name = "Nobita") OR NOT (n.name = "Suneo" OR n.name = "Dekisugi")
RETURN n
```

名前がたけしである場合か、30際以下ののび太である場合かスネオでも出来杉でもない場合のノードが返ってくる
MATCHでラベルを使うこともできたが、WHEREでも可能

```
MATCH n
WHERE n:Actor
RETURN n
```
Actorだけが返ってくる。また正規表現も使える

```
MATCH n
WHERE n.name =~ "T.*"
RETURN n
```

多分"Takeshi"が返ってくる。ある属性があるかないかで取る場合はHASを使う

```
MATCH n
WHERE HAS(n.belt)
RETURN n
```

belt属性があるものが得られる。

## RETURN
返り値を選択するのがRETURN文だけれどここで数を返した、平均を返したりといったことができる。

```
MATCH (n)-->(x)
WHERE n.name = "X"
RETURN n, count(*)
```

MATCHした数が返ってくる。

```
MATCH (n)-[r]->(x)
WHERE n.name = "Nobita"
RETURN type(r)
```

エッジのラベルが返ってくる。KNOWSとか。
SQLと同じように他にもSUMとかAVGとか使えるみたい。


大体基本的な構文はわかってきたので、次はGraphGistを使ってもう少し複雑なものを作ってみようかな。






