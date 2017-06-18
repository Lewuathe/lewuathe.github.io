---
title: "Style Transfer in TensorFlow"
layout: post
date: 2017-06-12 08:20:45 +0900
image: 'images/'
description:
tag: ["DeepLearning", "TensorFlow"]
blog: true
author: "lewuathe"
---

[CS20SI: TensorFlow for Deep Learning Research](http://web.stanford.edu/class/cs20si/syllabus.html) の課題の1つとしてStyle Transferを実装してみました。

* [TensorFlow-StyleTransfer](https://github.com/Lewuathe/TensorFlow-StyleTransfer)

Style TransferはCVPR 2016に出された[Gatys et al. 2016](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)が基礎となっているDeep Learningのアート系の技術で、元の画像を特定のスタイルで変換するというものです。

![architecture](images/posts/2017-06-12-style-transfer-in-tensorflow/architecture.png)

上記の様にどこかの町並みをゴッホが書いた様な画像に変換することができます。使うCNNは2014年のILSVRCというコンペで優勝した[VGG](https://arxiv.org/pdf/1409.1556.pdf)というモデルから全結合層を除いたモデル。

畳み込み層は通常深い層に行くほどより高次元の特徴を捉える層になります。というわけでタッチやスタイルのような特徴は浅い層で、画像のモチーフといったものはより深い次元で捉えることができると考えることができ、コンテンツとスタイルが別々に分けられればそれぞれ異なる画像に似せることもできそうというのがアイデア。

## 最適化

Style Transferでは元々学習済のVGGモデルを使います。では何を最適化するか。入力する画像です。このVGGモデルに対してランダムに生成された画像を入力してやり、ある損失関数に対して通常のCNNと同じように勾配を計算してやります。ただしこれは入力画像に対する勾配で、この勾配に従い入力画像を少しずつ更新していきます。これである損失関数に対して最適化された画像を得ることができます。

ではこの損失関数はどのように作ってあげればよいでしょうか。

先程コンテンツとスタイルの分離の話がありましたが、これら２つに対して損失を定義してやり全体としてはその重み付き和を最小化します。この２つの損失を`Content Loss`と`Style Loss`と呼んでいます。

この`Content Loss`と`Style Loss`の定義は天下り的というか、なんでそう定義されたのか分かりづらいです。上手くいくような損失関数であることは間違いなさそうということぐらい。

### Content Loss

\begin{equation}
\mathcal{L_{content}}(\boldsymbol{p}, \boldsymbol{x}, l) = \frac{1}{2} \sum_{i,j} ( F_{i,j} - P_{i,j} )^2
\end{equation}


$$\boldsymbol{p}$$と$$\boldsymbol{x}$$はコンテンツ画像と生成画像。$$F$$と$$P$$はそれぞれコンテンツ画像と生成画像から取られた畳み込みフィルタの値です。それの差を取っているだけ。この損失関数は論文だとconv4_2の層でとられ比較的高次元の特徴に対する損失を定義していると考えられます。

### Style Loss

次にスタイルの損失関数。特徴マップのグラム行列同士を比較します。グラム行列をとるのは特徴マップ同士の相関をみるためだと思います。

\begin{equation}
G_{i,j}^l = \sum_k F_{i,k}^l F_{j,k}^l
\end{equation}

上式では第$$l$$層での特徴マップ同士をかけてグラム行列を作っています。このグラム行列をスタイル画像と生成画像で比較します。$$G$$が生成された画像からの特徴マップ、$$A$$がオリジナルのスタイル画像からの特徴マップです。

\begin{equation}
E_l = \frac{1}{4N_l^2 M_l^2} \sum_{i,j} (G_{i,j}^l A_{i,j}^l)^2
\end{equation}

$$N_l$$は特徴マップの数、$$M_l$$は特徴マップのサイズなので$$4N_l^2M_l^2$$は畳み込み層の次元をかけ合わせたものになります。ただしTensorFlowでは畳み込み層のランクは`[batch_size, height, width, channels]`で表せるので$$N_l$$がchannels, $$M_l$$がheight * widthとなります。


\begin{equation}
\mathcal{L_{style}}(\boldsymbol{a}, \boldsymbol{x}) = \sum_{l=0}^L w_l E_l
\end{equation}

この損失を複数の層に渡って計算し足し合わせたものがstyle lossになります。具体的にconv1_1,conv2_1、conv3_1、conv4_1、conv5_1を用います。プログラムではこの重みは[0.5,1.0,1.5,3.0,4.0にしました](https://github.com/Lewuathe/TensorFlow-StyleTransfer/blob/master/src/models/train_model.py#L50)。より高次元の特徴に大きなペナルティを与えて、近づけようという効果があるのでしょうか。

最終的にはこの$$\mathcal{L_{content}}$$と$$\mathcal{L_{style}}$$の重み付き和、$$\mathcal{L}_{total}$$を最小化します。この損失関数の全体像はこの図が分かりやすいと思います。

\begin{equation}
\mathcal{L_{total}}(\boldsymbol{p}, \boldsymbol{a}, \boldsymbol{x}) = \alpha \mathcal{L_{content}} + \beta \mathcal{L_{style}}
\end{equation}

![](images/posts/2017-06-12-style-transfer-in-tensorflow/overview.png)

それでは動かしてみましょう。

[リポジトリ](https://github.com/Lewuathe/TensorFlow-StyleTransfer)をcloneしたら、依存ライブラリをいれます。基本的にはTensorFlowとPython3系があれば大丈夫だとおもいます。

```
$ make requirements
```

トレーニングは下記で走ります。初回はVGGモデルをダウンロードするので少し時間がかかるかもしれません。

```
$ make run OPTIONS='--content=yuzu --iter=300'
```

300iterationの学習に2~3時間くらいかかると思います。

![](https://github.com/Lewuathe/TensorFlow-StyleTransfer/blob/master/docs/yuzu.gif?raw=true)
![](https://raw.githubusercontent.com/Lewuathe/TensorFlow-StyleTransfer/master/docs/fuki.gif)

1つめは北斎の富嶽三十六景、2つめはゴッホの星月夜での変換です。初めの200iterationくらいはもやもやするだけなので、最後見るまで結果がなかなかわかりません。

ちょっとスタイルが弱く感じるのは重みが小さい(0.05)からでしょうか。
もう少しパラメタを調整してためしてみたいと思います。

## Reference

* [CS20SI: Tensorflow for Deep Learning Research](http://web.stanford.edu/class/cs20si/syllabus.html)
* [Gatys et al. 2016](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)
* [Karen Simonyan & Andrew Zisserman, 2014](https://arxiv.org/pdf/1409.1556.pdf)
