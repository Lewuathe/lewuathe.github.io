---
title: "Accelerating innovation through analogy mining"
layout: post
date: 2017-09-16 12:05:03 +0900
image: 'images/'
description:
tag: ["Paper", "DeepLearning"]
blog: true
author: "lewuathe"
---

今回も単語の分散表現、とりわけ[GloVe](https://nlp.stanford.edu/pubs/glove.pdf)を使った面白い論文を読んでみました。

* [Accelerating innovation through analogy mining](http://www.kdd.org/kdd2017/papers/view/accelerating-innovation-through-analogy-mining)

<iframe width="400" height="250" src="https://www.youtube.com/embed/oXkMrZ5DpO8" frameborder="0" allowfullscreen></iframe>

単語の分散表現を上手く使って新しい発想を行う手助けとなるような技術を構築したと述べています。この論文ではプロダクト、つまり特定のモノを発明するようなアイデアを提供できるようなることを目指しているようです。アプローチとしては「目的は同じだけれど、メカニズムが異なる」ようなモノを探せるようにすることで実現しているようです。

この論文は[KDD 17](http://www.kdd.org/kdd2017/)のベストペーパに選ばれたらしいのですが、個人的には結果や手法よりも発想それ自体が面白いなと思った論文でした。

## やりたいこと

ある道具があった時にそれを異なるメカニズムで同じ目的を果たすことができる他の道具を見つけます。つまり道具それぞれに対して目的(Purpose)とメカニズム(Mechanism)の
表現を見つけそれの近さを計ります。

具体的にはプロダクト$$i \in P$$に対してPurpose($$\mathbf{p_i}$$)とMechanism($$\mathbf{m_i}$$)をベクトルとして定義し、Purpose間の距離($$d_p$$)と
Mechanism間の距離($$d_m$$)に食わせてPurpose間の距離が近く、Mechanism間の距離が遠いものを見つけます。とても簡単そうです。

問題はどうやって$$\mathbf{p_i}$$, $$\mathbf{m_i}$$, $$d_p$$, $$d_m$$を得るかです。

## 訓練データの生成

まず元となるデータは[Quirky.com](http://quirky.com/)というサービスから取得します。このサービスはアイデアを持つ人と制作スキルを持った人をつなげ、できたものを買うことができるサービスのようです。ここから下記のようなアイデアの記述を8500件抜き出してきます。

![desc](images/posts/2017-09-16-accelerating-innovation-through-analogy-mining/desc.png)

ここからクラウドソーシングを使ってMechanismに関するものPurposeに関するものに人力でアノテーションをつけていきます。

![tagging](images/posts/2017-09-16-accelerating-innovation-through-analogy-mining/tagging.png)

黄色い単語はMechanismアノテーション、赤いのはPurposeアノテーションといった具合です。	

ちなみにこれには[Amazon Mechanical Turk](https://www.mturk.com/mturk/welcome)を使ったそうです。こんなクラウドソーシングサービスも行ってたんですね、Amazon。アノテーション付けはそれぞれのプロダクトに対して4人にやってもらっています。

## PurposeベクトルとMechanismベクトルの生成

プロダクトのアイデアの記述をN件集めます。$$X_N = \{ \mathbf{x_1}, \mathbf{x_2}, ..., \mathbf{x_N} \}$$。各記述は単語の列で$$\mathbf{x_i} = (x_1^i, x_2^i, ..., x_T^i)$$として表現されます。このときPurposeベクトルは二値ベクトルとして下記で表されます。

\begin{equation}
\mathbf{p_i} = (p_i^{1}, p_i^{2}, ..., p_i^{T})
\end{equation}

$$p_i^{t}$$は単語$$t$$にPurposeアノテーションが付与されていれば1,そうでなければ0となるような値です。これを今回は4人にアノテーションを付与してもらっているのでこのベクトルがひとつの記述に対して4つできることになります。Mechanismベクトルに関しても同様の手法で

\begin{equation}
\mathbf{m_i} = (m_i^{1}, m_i^{2}, ..., m_i^{T})
\end{equation}

を得ることができます。

## 表現の取得

さてこのベクトルを元にPurposeやMechanismをうまく表した分散表現を獲得したいのですが、ここで[GloVe](https://nlp.stanford.edu/pubs/glove.pdf)を使うことになります。あらかじめ訓練されたGloVeの[Common Crawl data](https://nlp.stanford.edu/projects/glove/)のモデルを用意しておきます。そして

1. 先程のPurposeベクトルとMechanismベクトルで1となっている単語をこのGloVeの表現に置き換える
2. K人にアノテーションされたK個のベクトルをつなげる
3. TF-IDFで各単語の重みを計算し、重みの大きい上位5つの単語のTF-IDFスコアでの重み付き平均をPurpose (or Mechanism)ベクトルとする。

最終的には$$\mathbf{p_i} \in \mathbb{R}^{300}$$, $$\mathbf{m_i} \in \mathbb{R}^{300}$$となるようです。

## モデルのトレーニング

プロダクトの記述$$x_i$$(これはGloVeのリストで表現される)が得られたら先程の($$\mathbf{p_i}$$, $$\mathbf{m_i}$$)のペアを返すようなモデルを作ります。そうすれば、未知のプロダクトアイデアに対して、同様のPurposeを持ったもの、異なるMechanismを持ったものを探すことができます。つまり訓練データとして

\begin{equation}
X_N = \{ \mathbf{x_1}, \mathbf{x_2}, ..., \mathbf{x_N} \}
\end{equation}

と教師データ

\begin{equation}
Y_N = \{ (p_1, m_1), (p_2, m_2), ..., (p_N, m_N) \}
\end{equation}

から訓練させます。モデルにはGRUを使ったBiRNNを用います。BiRNNを使うことで単語毎の前方への依存と後方への依存を考慮することができます。このBiRNNレイヤーはPurposeベクトル、Mechanismベクトル双方で共通で、この隠れ状態に対して$$W_p$$と$$W_p$$の重みの全結合層をMSE(Mean Squared Error)で最適化します。

## 評価

![result](images/posts/2017-09-16-accelerating-innovation-through-analogy-mining/result.png)

AMTでプロダクト同士のマッチングを人で行ったものをテストデータとして評価に使っています。表では様々なメトリックでプロダクトのマッチングを評価してマッチング結果がテストデータとどれくらい合っているかとprecisionとrecallで評価しています。

Mechanism Onlyでマッチングさせると最もよい値になるのは、人間も結局そのようにプロダクトの近さを考えているからなんでしょうか。iPhoneと似ているものを思い浮かべる時に、糸電話じゃなくてX Periaを思い浮かべるような。そういった恣意的というか表面的なマッチングを防ぐためにAMTのワーカにはマッチングの考えというかスキームみたいなものを明示するようにしたと述べてありますが、、、難しそう。

## アイデアの生成

というわけで最初に述べた、「目的は同じだけれど、メカニズムが異なる」を見つけてみます。Purposeベクトルに対してK-Meansでクラスタリングした後、同一クラスタ内でMechanismベクトルが遠いものを選びます。例えばiPhoneのバッテリーケースを例にとると、単純なTF-IDFは結局Mechanismまで同じようなケースを列挙してしまっているのに対して提案手法では違う分野でのインスピレーションを与えてくれそうな感じがしなくもないですね。	

![idea](images/posts/2017-09-16-accelerating-innovation-through-analogy-mining/idea.png)


## Reference

* [Accelerating Innovation Through Analogy Mining, Tom Hope et.al, 2017](http://www.kdd.org/kdd2017/papers/view/accelerating-innovation-through-analogy-mining)
* [Accelerating innovation through analogy mining - Morning Paper](https://blog.acolyer.org/2017/09/14/accelerating-innovation-through-analogy-mining/)
* [Neural machine translation by jointly learning to align and
translate, D.Bahdanau, K.Cho, 2014](https://arxiv.org/abs/1409.0473)
* [Least squares quantization in PCM, S. Lloyd, 1982](http://ieeexplore.ieee.org/document/1056489/?reload=true)