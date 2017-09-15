---
title: "Adversarial examples for evaluating reading comprehension systems"
layout: post
date: 2017-09-14 17:03:51 +0900
image: 'images/'
description:
tag: ["DeepLearning", "Paper"]
blog: true
author: "lewuathe"
---

Deep Learningのモデルは画像識別や自然言語処理の分野で高い精度を叩き出していますが、そのモデルを騙すようなデータ(Adversarial Example)を作成する方法に関しても幾つかの研究があります。有名なものだと[Goodfellow et al. (2015)](https://arxiv.org/pdf/1412.6572v3.pdf)。元の画像に人間には分からない程度のノイズをのせることでDeep Learningのモデルを騙すことが示されています。

![Goodfellow](images/posts/2017-09-14-adversarial-examples-for-evaluating-reading-comprehension-systems/goodfellow.png)

今回はこれに関連して自然言語、とりわけ質問回答のタスクにおいての論文[Jia & Liang, (2017)](https://arxiv.org/abs/1707.07328)を読んでみました。

* [Adversarial examples for evaluating reading comprehension systems, Jia & Liang, EMNLP 2017](https://arxiv.org/abs/1707.07328)

## 問題

ある文章とそれに関する質問文があった時にその質問に答える文章を生成するようなモデルはDeep Learningを使って作ることができます。そのようなモデルを欺くようなデータ(Adversarial Example)を生成しました。問題は以下のようになっておりParagraphとQuestionを入力として与えられ、正解となる単語を答えることになります。

![task](images/posts/2017-09-14-adversarial-examples-for-evaluating-reading-comprehension-systems/task.png)

ParagraphとQuestionから正しいPredictionを得ることができれば成功です。ちなみに今回のデータセットでは必ず答えとなる単語はParagraphに含まれていることにします。

用いられた手法はとてもシンプルで自分でも簡単に試すことができるようなものにみえます。Adversarial Exampleの事例を見ると現実の世界でいかにエラーの少ないシステムを作ることが難しいかを改めて感じます。

## 画像分類と文章理解のAdversarial Example

詳細に入る前にちょっと画像分類とこの文章理解のタスクのAdversarial Exampleの考察が面白かったので紹介します。

![compare](images/posts/2017-09-14-adversarial-examples-for-evaluating-reading-comprehension-systems/compare.png)

画像に関するAdversarial Exampleはモデルの*Oversensitivity*を利用して同じように見える画像でもほんの少しの差異でカテゴリが異なるようにすることができます。一方で今回の文章理解のタスクでは逆の現象が起きることがわかっています。このモデルでは汎化性能が高すぎるからか*Overly Stable*、つまり多少の差異には動じないようなモデルになってしまい、文章の意味を大きく変えたのに答えが変わらないということになるわけです。

ではどうやってAdversarial Exampleを作るかというと気をつける点がひとつあります。Adversarial Exampleを作るときに意味を変えるような変更をしてはいけません。そもそも文章の意味が変わったら真の答えも変わるはずだからです。真の答えとなるべきものは変えずに、モデルを騙すことができるようなデータを作成します。これをオリジナルの問題と*compatible*であるといいます。

提案手法ではある文を文章の後ろにつけるアプローチをとっています。これは意味を変えずに文章を機械的に変えていくのは難しいからだと思います。

![addsent](images/posts/2017-09-14-adversarial-examples-for-evaluating-reading-comprehension-systems/addsent.png)

## Adversarial Exampleの生成

ではこのくっつける文をどうやって生成するかというと大きくわけて２つの手法が提案されています。

* *AddSent* : 質問文にある単語の幾つかと答えとなる単語を変えます。この変えられた質問から答えを導きだせるような文章を作りこれが追加される文になります。できた文章が文法的におかしい可能性もあるので最終的にクラウドソーシングで手直しをします。最終的にこれらの文章をモデルに食わせて最も回答率の悪い文章をAdversarial Exampleとします。
* *AddAny* : 文になっていなくてもいいので適当に単語をいくつかくっつけます。論文では10個の単語。

*AddSent*で面白いのは単語を変更するときに[GloVe](https://nlp.stanford.edu/pubs/glove.pdf)というword2vecのように単語の分散表現を作るアルゴリズムを使って似ているけど違う単語に変換していることです。	

## 検証

![evaluation](images/posts/2017-09-14-adversarial-examples-for-evaluating-reading-comprehension-systems/evaluation.png)

検証にはこの問題を解くためのモデル[BiDAF](https://allenai.github.io/bi-att-flow/)と[Match-LSTM](https://arxiv.org/abs/1608.07905)というモデルを使っています。どちらもRNNの一種でそれぞれアンサンブル学習させたモデルでも試しています。どの手法でも正答率が下がっていることがわかります。面白いのは*AddOneSent*という項目です。これはAddSentから最後のプロセスであるモデルでの評価と選択をせずにランダムに選択をします。モデルに依存しないAdversarial Exampleを作ることがこの手法でできるのですが、これでも正答率をかなり下げることができていることがわかります。また*AddAny*はもっとランダムなので、この文章理解のモデルを騙すことがそれほど難しいことではないことがわかります。

## まとめ

文章理解のタスクでも比較的容易にAdversarial Exampleが作れることがわかる論文でした。

ただ文章理解のDeep Learningモデルが*Overly stable*という傾向を持つというのは興味深いのですが、論文ではモデルのこの特徴を考慮してAdversarial Exampleを作ったとあります。オリジナルな文章とcompatibleな文章を付け足した誤答させるには*Oversensitivity*の方を考慮したという方が適切なんじゃないかと思うのですがどうなんでしょうか。

## Reference

* [Adversarial examples for evaluating reading comprehension systems, Jia & Liang, EMNLP 2017](https://arxiv.org/abs/1707.07328)
* [Adversarial examples for evaluating reading comprehension systems - Morning Paper](https://blog.acolyer.org/2017/09/13/adversarial-examples-for-evaluating-reading-comprehension-systems/)
* [BiDAF](https://allenai.github.io/bi-att-flow/)
* [Machine Comprehension Using Match-LSTM and Answer Pointer, S Wang, J.Jiang 2016](https://arxiv.org/abs/1608.07905)


