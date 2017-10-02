---
title: "An efficient bandit algorithm for real-time multivariate optimization"
layout: post
date: 2017-10-01 15:23:03 +0900
image: 'images/'
description:
tag: ["Amazon", "MachineLearning"]
blog: true
author: "lewuathe"
---

[KDD '17](http://www.kdd.org/kdd2017/papers/view/an-efficient-bandit-algorithm-for-realtime-multivariate-optimization)で、Audience Appreciation Awardにも選ばれていた"An efficient bandit algorithm for real-time multivariate optimization"という論文を読みました。

<iframe width="560" height="315" src="https://www.youtube.com/embed/G-omu_ki7YM?rel=0" frameborder="0" allowfullscreen></iframe>

Amazonがコンバージョンを上げるためにいわゆるA/Bテストをいかに効率よく行うかという問題をMulti-armed banditの手法で解いたというものです。例えばあるECサイトのウェブページがあったとします。
このページにはコンポーネント5つあり、それぞれ取りうるパターンが決まっています。ボタンは赤か青、画像は３パターンが用意されているといった具合に。この時すべてのパターンをテストするには48パターン(=2☓2☓3☓2☓2)を試す必要がありますが、更にそれぞれのパターンの妥当なテストボリュームを考えると、Amazonのトラフィックサイズでもこのテストには全部で66日程度かかるそうです。

![widget](images/posts/2017-10-01-an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/widget.png)

コンポーネントが増えると、組み合わせが爆発してしまうのでこのパターンを抑える必要があります。このためのモデルをまず考えてみましょう。

## モデル

簡単のためレイアウト上のコンポーネントのパターンはすべて同じとします。つまり、$$i$$番目のコンポーネントのパターンを$$N_i$$とすると

\begin{equation}
N_1 = N_2 = ... = N
\end{equation}

となります。そしてD個のコンポーネントがあるとすると組み合わせのパターンは全部で$$N^D$$となります。$$i$$番目のコンポーネントのパターンを$$A[i]$$と表すとするとレイアウトは$$A \in \{ 1,2,...,N \}^D$$
として表現することができます。

モデルに対する報酬(Reward)を決めるのはレイアウトだけではありません。ユーザの属性や時間、場所などのセッション情報からも決まります。同じレイアウトでも人によって何を買うか違いますしね。これをコンテキスト, $$X$$として表現します。この時与えられる特徴は$$B_{A,X} \in \mathbb{R}^M$$の$$M$$次元ベクトルで表されます。時刻tにおいて選ばれるレイアウトを$$A_t$$、モデルのパラメタを$$W$$とするとRewardの期待値は

\begin{equation}
\mathbb{E} [R|A,X] = g(B_{A_t,X}^TW)
\end{equation}

となります。$$g$$は何らかの滑らかなリンク関数です。この時次のレイアウト$$A_*$$は

\begin{equation}
A_{\*} = argmax E[R_A,X_t]
\end{equation}

を満たすものが選ばれますが、Multi-armed banditでは将来に渡っての報酬も増やさなければいません。これは以下のように定式化できます。

\begin{equation}
\Delta_{t} = E[R_{A_*},X_t] - E[R_A,X_t]
\end{equation}

$$\Delta_{t}$$を同時に最小にすることを求められます。これを**Regret**といいます。「あー、あっちを選んでおけばよかった」という感覚でしょうか。一般には$$\Delta_{t}$$の下界は$$O(M\sqrt{T})$$となることが知られています。

ではどのように最適な$$W$$を求めたらよいでしょうか。ここでは計算量を抑えるためにpair-wiseな特徴だけ考慮することにします。つまり各コンポーネントのRewardへのインパクトと各２コンポーネント間の関係のみを考慮します。
３つ以上は考慮しないことで計算量を抑えます。

\begin{equation}
B_{A,X}^T W = W^0 + \sum_{i=1}^D W_i(A) + \sum_{j=1}^D \sum_{k=j+1}^D W_{j,k} (A) + \sum_{l=1}^L W_l^c (X) + \sum_{m=1}^D \sum_{n=1}^L W_{m,n}^c (A,X)
\end{equation}

このモデルを使って学習を行う部分は以下のように**Thompson Sampling**というアルゴリズムを用います。Thompson SamplingはMulti-armed banditの問題を解くために古くから使われるもので([考案されたのは1933年とも](https://en.wikipedia.org/wiki/Thompson_sampling))、期待報酬を最大にするようなレイアウトを選んでいきます。

![Thompson Sampling](images/posts/2017-10-01-an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/thompson_sampling.png)

得られた報酬の履歴から事後分布を計算していきますが、ここでもやはり$$argmax B_{A,X_t}^T W_t$$の計算量が問題になります。取りうるレイアウトのパターンは$$O(N^D)$$あるからです。

## 山登り法(Hill Climbing)

この論文では山登り法を使って最大報酬期待値を得るレイアウトを推定します。下表にあるようにいくつかのパターンに対してK回ランダムにコンポーネントを選択し、このコンポーネントのみを変更したとき最大報酬を与えるようなレイアウトを返します。これを様々な初期値$$A_{S}^0$$で行い最終的に最も期待報酬の高いレイアウトを返します。計算量は$$O(SKN)$$とずっと小さくなることがわかります。

![hill climbing](images/posts/2017-10-01-an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/hill_climbing.png)

## 評価 

![evaluation](images/posts/2017-10-01-an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/evaluation.png)

評価では上記5つの手法を比較していました。MVT＊というのが提案されている方法で$$N^D-MAB$$や$$D-MABs$$が従来手法です。下図はiteration毎のregretの値です。MVT1, MVT2の方が比較的速く収束していることがわかります。

![local regret](images/posts/2017-10-01-an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/local_regret.png)

下記はN = 8, D = 3でも山登り法の評価ですが、K=5程度でregretの値は収束することがわかります。

![hill climbing eval](images/posts/2017-10-01-an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/hill_climbing_eval.png)

## Recap

この手法が個人的に面白いと思った点は

* 各コンポーネントの関連が重みで表現できるためデザイナーを巻き込んでUI/UXの改善につなげることができそう
* 計算スピードの高速化に重きをおいているのでビジネスにおける意思決定に大きく貢献できる

特に2つめはこの手法でExploration-Exploitationのバランスをとりつつ、効果のでなさそうなレイアウトを先に排除しておくことでより洗練されたデザイン、レイアウトに時間を使うことができるかもと思いました。

# Reference

* [An efficient bandit algorithm for realtime multivariate optimization, KDD '17](http://www.kdd.org/kdd2017/papers/view/an-efficient-bandit-algorithm-for-realtime-multivariate-optimization)
* [Morning Paper](https://blog.acolyer.org/2017/09/27/an-efficient-bandit-algorithm-for-real-time-multivariate-optimization/)
* [Bayes Linear Regression](https://en.wikipedia.org/wiki/Bayesian_linear_regression)
* [Thompson Sampling](https://en.wikipedia.org/wiki/Thompson_sampling)
* [確率的バンディット問題](https://www.slideshare.net/jkomiyama/ss-34796421)
