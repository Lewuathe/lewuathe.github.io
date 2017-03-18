---
title: "bzip2 and MAPREDUCE-13270"
layout: post
date: 2017-03-18 21:51:18 +0900
image: 'images/'
description:
tag: ["MapReduce", "bzip2", "Hadoop"]
blog: true
jemoji:
author: "lewuathe"
---

少し前だけれど、[HADOOP-13270](https://issues.apache.org/jira/browse/HADOOP-13270)について書こうと思う。

Hadoop MapReduceフレームワークは[InputFormat](https://github.com/apache/hadoop/blob/trunk/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core/src/main/java/org/apache/hadoop/mapred/InputFormat.java)というインターフェースを通じて様々なフォーマットのファイルを読むことができる。単純なテキストファイルを一行ずつ読んだり、[Avro](https://avro.apache.org/)などのシリアライゼーションフォーマットやgzipなどの圧縮フォーマットもサポートしている。

InputFormatは`getSplits`というメソッドで一つのファイルを複数のSplitという単位に分割することが要求される。

```
  InputSplit[] getSplits(JobConf job, int numSplits) throws IOException;
```

1つのMapperは1つのSplitを読んで処理を行うため、このSplitを作る方法をInputFormatが知らないと巨大なファイルを複数のMapperで分散して処理できないのでSplitの作り方はMapReduceを効率的に走らせるために鍵ともいえる。
通常はデータのローカリティを活かすために、1つのSplitはHDFSのBlockに対応づけられる。つまりブロックサイズが128MBだとするとこの大きさで各Splitが作られることになる。このとき大事なことが**各Splitから読み出されるデータはそれだけで読めるようになっていないといけない**。どういうことかというと

```
record(N)
record(N+1)
record(N+2)
---- 128MB ----
record(N+3)
record(N+4)
record(N+5)
```

上記のように各レコードが1行ずつ書かれたファイルがあったとして、ファイルの先頭から読んでいってrecord(N+2)とrecord(N+3)の間がちょうど128MBになったとする。この場合1つめのSplitの終わりはrecord(N+2)で次のSplitのはじめのレコードはrecord(N+3)になる。ただレコードの区切りがちょうどBlockの区切りになっているとは限らないので、もし下記のようになっていたとすると

```
record(N)
record(N+1)
reco
---- 128MB ----
rd(N+2)
record(N+3)
record(N+4)
record(N+5)
```

単純にBlockサイズ区切りにすると読めないレコードがでてくる。Split同士は全く別のMapper（おそらく別のマシンで動く）で読まれるのでデータが正しく読めていないのかどうかもMapperは知らない。
これではまずいのでInputFormatは正しくレコードが区切られるように微調整をしてSplitを作ってくれる。


# bzip2

ところがこの様にSplitを作ろうとすると圧縮フォーマットの場合には問題がでてくる。gzipなどの圧縮フォーマットの場合、1つの圧縮されたファイルを読めるように解凍するためにはファイルがまるまる必要になる。これはInputFormatのSplitと相性が悪い。なぜならそれだけで読める部分に分割するということが原理的にできないからだ。gzipで圧縮されたフォーマットをMapperで読めるようにするためには1ファイルすべてを読む必要がある。例えば1.2GBくらいのファイルがあったとすると10blockになり、10Mapperくらいで読んでほしいが、1MapperはすべてのBlockを読まないといけない。これではデータのローカリティを犠牲になっており、大きなファイルをだととても効率が悪くなる。こういったフォーマットを**Unsplittable**という。

実は圧縮フォーマットの中でもSplittableなものがある。その1つが[bzip2](http://www.bzip.org/)だ。bzip2は同期マーカと呼ばれる48ビットの円周率の近似値を用いてファイルを分割可能な単位で圧縮している。

![bzip2](images/posts/2017-03-18-bzip2-hadoop-13270/bzip2.png)

上記の図でSplitと書かれている部分は圧縮されているが、それだけでまた解凍が可能だ。つまりこのSplitを読んだMapperは読んだ部分をbzip2のuncopressorにかければ通常の非圧縮ファイルと同じように読むことができる。並列処理を行う上でもデメリットはない。(もちろん各フォーマットで圧縮効率や、圧縮スピードは違うのでアプリケーションにあったフォーマットを選ぶのがよいと思う)

# HADOOP-13270

前置きが長くなってしまったけれど[HADOOP-13270](https://issues.apache.org/jira/browse/HADOOP-13270)。これはある特定のサイズのbzip2ファイルを特定のSplitサイズで読もうとするとデータが重複するというバグだった。

> Unit test TestTextInputFormat.testSplitableCodecs() failed when the seed is 1313094493.
Stacktrace
java.lang.AssertionError: Key in multiple partitions.
at org.junit.Assert.fail(Assert.java:88)
at org.junit.Assert.assertTrue(Assert.java:41)
at org.junit.Assert.assertFalse(Assert.java:64)
at org.apache.hadoop.mapred.TestTextInputFormat.testSplitableCodecs(TestTextInputFormat.java:223)


bzip2は使ってないけれど、データが欠損したり重複するとデータ分析の意味がなくなるし問題として面白そうなのでなんとかしてみようと思い調べてみた。

問題は[`Bzip2Codec`](https://github.com/apache/hadoop/blob/9a44a832a99eb967aa4e34338dfa75baf35f9845/hadoop-common-project/hadoop-common/src/main/java/org/apache/hadoop/io/compress/BZip2Codec.java)というクラスにあった。このクラスは与えられたoffsetから直近のMarkerを探してそこを始点とする`InputStream`を作ってくれる。元々の実装はこうなっていた。

```java
public SplitCompressionInputStream createInputStream(InputStream seekableIn,
    Decompressor decompressor, long start, long end, READ_MODE readMode)
		throws IOException {

  // startから次の場所にあるデータを読める直近のmarkerを探したい

  // ...
  // ファイルの先頭には特別に"BZh9"というマジックが書かれている。これに48bitのMarkerを足すので
  // 合計10bytesの探すべきデータがある。
  final long FIRST_BZIP2_BLOCK_MARKER_POSITION =
		  CBZip2InputStream.numberOfBytesTillNextMarker(seekableIn);
  long adjStart = 0L;

  // 読むべきMarkerを見つけられる位置までseekして戻る
  adjStart = Math.max(0L, start - (FIRST_BZIP2_BLOCK_MARKER_POSITION));
  ((Seekable)seekableIn).seek(adjStart);

  // 次に読むべきMarker自体はBZip2CompressionInputStreamが見つけてくれる
  SplitCompressionInputStream in =
    new BZip2CompressionInputStream(seekableIn, adjStart, end, readMode);
  // ...
}
```

与えられた`start`の位置まで（を含んだ圧縮ブロック）は読んでいるので次のMarkerからのデータを読みたい。

![alignment](images/posts/2017-03-18-bzip2-hadoop-13270/alignment.png)

そのMarkerを探す必要があるが、`start`はbyte単位で計算されているので`start`位置がMarkerの真ん中にある可能性がある。そのまま`BZip2CompressionInputStream`にseekさせると読みたいMarkerの次のMarkerを見つけてしまうので少し戻す必要がある。これが`adjStart`.

![ajdStart](images/posts/2017-03-18-bzip2-hadoop-13270/adjStart.png)

Markerは通常48bit(=6bytes)だけれど、ファイルの先頭には"BZh9"という文字があり10bytesになっているらしい。`FIRST_BZIP2_BLOCK_MARKER_POSITION`は10bytes。ところが"BZh9"がついているのはファイルの先頭だけなのに、常に10bytes戻ってMarkerを探すようになっている。これだと問題がおきるケースが下記。

![read-again](images/posts/2017-03-18-bzip2-hadoop-13270/read-again.png)

`start`を含んだ圧縮ブロックはすでに読んでいるのに`adjStart`で戻りすぎたのでまた同じMarkerが見つかってしまう。つまり**データの重複が発生している**。本当は6bytesだけ戻らなければいけないところを10bytes戻るので同じMarkerを見つけてしまう。Fix自体は簡単で正しく6bytes戻ればいいだけだった。


```java

final long FIRST_BZIP2_BLOCK_MARKER_POSITION =
	CBZip2InputStream.numberOfBytesTillNextMarker(seekableIn);
long adjStart = 0L;
if (start != 0) {
	// ファイルの先頭でないなら6bytes (FIRST_BZIP2_BLOCK_MARKER_POSITION - (2bytes + 2bytes))戻る
	// そもそもファイルの先頭だったら戻る必要はなかった
	adjStart = Math.max(0L, start - (FIRST_BZIP2_BLOCK_MARKER_POSITION
			- (HEADER_LEN + SUB_HEADER_LEN)));
}
```

InputFormat関連のバグはデータの欠損、重複を生み出すので改めて大事な部分だなと思った。
