---
title: "BadNets: Identifying vulnerabilities in the machine learning model supply chain"
layout: post
date: 2017-10-21 11:13:31 +0900
image: 'images/'
description:
tag: ["DeepLearning", "AdversarialExample", "Paper"]
blog: true
author: "lewuathe"
---

[Adversarial examples for evaluating reading comprehension systems](/adversarial-examples-for-evaluating-reading-comprehension-systems.html)でDeep Learningのモデルに関するAdversarial Exampleの研究に関して書きました。この分野はDeep Learningの実用化が進みつつある中で盛んに研究が行われているものの一つです。

今回読んだ*["BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain", Tianyu Gu, et.al.](https://arxiv.org/abs/1708.06733)*は発見が難しいような形でモデルに"Backdoor"を仕込むことができる可能性を示したものです。Deep Learningのモデルは現在ではGoogle CloudやAWSを使って外部サービスを使うことや、既に訓練されたモデルに対してFine-Tuningを行う転移学習をすることも多くそういったケースでの問題をこの論文ではあげています。

## 前提

Backdoorを仕掛けられたモデルを訓練するためには下記のような想定をします。

* モデルを作るユーザは作られたモデルを評価するための独自のValidationセットをもっている
* Validationセットでの評価を一定以上満たしたものだけProductionにリリースする
* 攻撃者はそのValidationセットを満たしつつ、特定の入力に対して不正な出力を行うモデルを作成しようとする
* そのため訓練データの操作、各ハイパーパラメタの調整、アルゴリズムの変更などができるとする

訓練データだけ与えてあとはよしなにやってくれるようなクラウドサービスや他人が作った公開済のモデルなどはすべてこのような攻撃ができる可能性があります。

## Backdoorの手法

Backdoorを仕掛けられたモデルは大きく２タイプあります。

![mechanism](images/posts/2017-10-21-badnets:-identifying-vulnerabilities-in-the-machine-learning-model-supply-chain/mechanism.png)

左が通常のモデルです。真ん中のモデルは不正なネットワークをまるまる埋め込んでしまう方法。右はいくつかのニューロンの重みを操作したものになります。どちらのモデルにしても特別な入力にたいして不正な出力を返すようにできます。では特別な入力とはどういったものでしょうか。

![mnist](images/posts/2017-10-21-badnets:-identifying-vulnerabilities-in-the-machine-learning-model-supply-chain/mnist.png)

上画像はMNISTを使った場合の例です。左が正しい画像。操作された画像の右下のピクセルは白くなっていることがわかると思います。これをマーカとして、Backdoorが埋め込まれたモデルはこの入力を8（あるいは7でない何か）として判定します。このMNISTを使ってBackdoorモデルを評価したものが下記になります。

![eval](images/posts/2017-10-21-badnets:-identifying-vulnerabilities-in-the-machine-learning-model-supply-chain/eval.png
)

ピクセルが操作されたBackdoor入力を訓練データに加えたときのエラー率を示しています。青線cleanは通常の入力、橙backdoorがピクセルが操作された入力です。Backdoor入力を半分近く加えてもcleanな入力に対するエラー率はそれほど悪化しないことがわかります。このことからValidationデータが十分でない場合、このモデルはユーザの検査をパスしてしまう可能性が高いことがわかります。

## 転移学習におけるBackdoor

上記のMNISTの例は完全に他人に作られたモデルを使っていたことになりますが、同じようなことは転移学習においてもいえます。例えば自動運転のシステムを作るとします。この時、アメリカの標識用に予め訓練された識別モデルを使ってスウェーデン様にFine-tuningをします。CNN層の学習を省くことができるためこのような転移学習は有用です。しかしこの時もしアメリカの標識用に訓練されたCNN層にBackdoorが仕掛けられていると最終的なモデルにも影響を与えることができます。

![transfer](images/posts/2017-10-21-badnets:-identifying-vulnerabilities-in-the-machine-learning-model-supply-chain/transfer.png)

論文にあるスウェーデンの標識の実験の例だと通常の入力に対しては74.9%の精度に対してBackdoor入力(小さなシールが張ってある標識)に対しては精度が61.6%まで下がります。例えばこのモデルを使った自動車は特定のシールを標識に貼られると正しく運転できなくなる可能性があります。

転移学習においては[Caffe Model Zoo](http://caffe.berkeleyvision.org/model_zoo.html)など多くのPretrainedモデルを提供するサイトがありますが、ダウンロード先のURLを攻撃者が変更したり、モデルをいじったりする可能性があることを指摘しています。MD5などのchecksumも提供されていますが、既にそれらが一致しないモデルが多数ありました。まずは既存の転移学習における枠組みを改善し、信頼できるモデルを安心して使えるようなものに変えていくことが必要だと指摘しています。

## Reference

* [BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain](https://arxiv.org/abs/1708.06733)
* [Morning Paper](https://blog.acolyer.org/2017/10/13/badnets-identifying-vulnerabilities-in-the-machine-learning-model-supply-chain/)
