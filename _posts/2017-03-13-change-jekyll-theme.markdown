---
title: "Change Jekyll theme"
layout: post
date: 2017-03-13 21:21:10 +0900
image: 'images/'
description:
tag: ["Jekyll"]
blog: true
jemoji:
author: "lewuathe"
---

久しぶりにJekyllのテーマを変えてみた。どのテーマも半年くらい経つと飽きが来るのか更新頻度にも影響するので定期的にテーマを変えるようにしている。
おかげで[GitHub Pagesのリポジトリ](https://github.com/Lewuathe/lewuathe.github.io)の入れ替えというか大掃除にも慣れてきた。

まず新しいテーマをcloneしてくる。

```
$ git clone git@github.com:LeNPaul/Lagrange.git lewuathe.github.io
```

CMSはJekyllでカスタムのドメインをGitHub Pagesで使っている場合は下記を最低限コピーしてくれば問題なく動く。

* `CNAME`
* `_posts`
* `_config.yml`: ただしテーマによっては加筆修正必要。

テーマによっては各postのtagが読めたり読めなかったりするようで前回の[indigo](https://github.com/sergiokopplin/indigo)への移行は大変だった。`date`タグのフォーマット
が`2017-03-13 21:21:10 +0900`でないと動かないことに気づくのに何時間かかかった。

```
$ jekyll serve
```

表示の確認。SNSへのリンクが正しく貼られていないことがある。
今回の[Lagrande](https://github.com/LeNPaul/Lagrange)というテーマは名前もさることながらとても小さいテーマなので何か問題があっても対応できそう。
`_posts`ファイル達の変換を何もしなくてよかったのは楽だった。

```
# コードスニペットのフォーマットもきれいに
```

テーブルも

|Name|Description|Extra|
|:-----:|:-----|:-----|
|Takeshi|これはたけし|特になし|
|Kokeshi|これはこけし|特になし|

画像も

![Code](/images/posts/2017-03-13-use-lagrande-theme/code.png)

数式も

$$
e^{i \pi} + 1 = 0
$$
