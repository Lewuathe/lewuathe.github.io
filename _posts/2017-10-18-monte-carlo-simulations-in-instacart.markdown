---
title: "Monte Carlo simulations in Instacart"
layout: post
date: 2017-10-18 21:38:56 +0900
image: 'images/'
description:
tag: ["Simulation", "Startup", "MachineLearning", "Paper"]
blog: true
author: "lewuathe"
---

Instacartのエンジニアが書いたある記事が面白かったです。

* [No order left behind; no shopper left idle.](https://tech.instacart.com/no-order-left-behind-no-shopper-left-idle-24ba0600f04f)

[Instacart](https://en.wikipedia.org/wiki/Instacart)は地元の商店から食品などの当日中に運んでくれるサービスを提供している企業です。日本でサービスを提供していないみたいなので、名前も知らなかったのですが今では全米で100以上の都市でサービスを提供している企業のようです。このブログ記事はその配送ロジスティクスをMonte Carlo similationを使って改善したという内容になっています。

簡単にInstacartのサービスの提供の仕方を紹介すると、

1. ユーザはiPhone or Androidアプリで食品を注文する
2. Shopperと呼ばれる人たちがその注文に従い買い物をしていく
3. Shopperはすべて買い終わったら注文したユーザのもとに届ける

Uber生鮮食品版といった感じでしょうか。Shopperがいる場所は時々刻々変わり、早く動ける人もいれば、すぐに動けない人もいます。(車 or 徒歩など移動手段に依るのでしょうか) たくさんのShopperを稼働させていればユーザの注文に対するカバレッジを上げることができますが、一方で注文が少なければShopperを持て余してしまいます。

![supply and demand](images/posts/2017-10-18-monte-carlo-simulations-in-instacart/supply_demand.png)

需要と供給を満たす必要十分なShopperの数を求めることが必要になってきます。余剰Shopperを**Idleness**、Shopperがいないせいで注文を受けられなかった分を**Lost Deliveries**と呼んでこれらを最小化しつつ

* 一日の営業時間帯の各時間のShopperの数

を求めます。これをInstacartではMonte Carlo simulationを使って解きました。

## なぜMonte Carlo simulationか

こういった問題を解く上でまず思いつくのはMachine Learningかと思います。Linear RegressionやNeural Networkなど決められた特徴から必要なShopperを予測することはできそうに見えます。ただこの問題の場合特徴となるべき変数がとても多いうえに、そのバリエーションもとても大きくなります。商品の一般的な需要予測に加えて、Shopperの移動手段、天気、交通状態といった要素が多くからんできます。Monte Carlo simulationは与えられた確率分布に基いてこれらの変数をサンプリングしてくることができるので変数同士の複雑な関係をモデリングするために十分なデータを生成することが容易になります。

## シミュレーション

シミュレーションの対象となるのは

* Order : どこでいくつ注文したか
* Shopper : どこにShopperがいるか

これらの値は予め実データに基いて作られた確率分布からサンプリングしてきます。

![simulation](images/posts/2017-10-18-monte-carlo-simulations-in-instacart/simulation.png)

この値からどのShopperがどのStoreを回ればいいかを計算します。これには**Vehicle Routing Problem (VRP)**という組み合わせ最適化問題を解きます。このアルゴリズムはInstacartが実際にShopperに買わせるルートを計算するときのものと同じアルゴリズムを使います。そうすることでシミュレーションを現実の配送ロジスティクスに近づけることができます。

この計算されたルートそれぞれの所要時間から各時間帯で必要なShopperの数を出すことができます。

## 最適化

これを最適化するにはまず目的関数を設定します。先程書いたようにLoss DeliveriesとIdlenessはなるべく小さくしたいです。

\begin{equation}
\sum_{i = 1}^N \sum_{h = 8}^{22} idleness * max(x_h - l_{h,i}, 0) + ld * max(l_{h,i} - x_h, 0)
\end{equation}

$$x_h$$は時間$$h$$におけるShopperの数。これが求めるものになります。$$l_{h,i}$$が時間$$h$$において実際必要なShopperの数。これはシミュレーション$$i$$毎に決まります。$$x_h$$の方が大きければIdleness、小さければLost Deliveriesとなります。

![simulation](images/posts/2017-10-18-monte-carlo-simulations-in-instacart/optimization.png)

たくさんシミュレーション(灰色線)を走らせてこの目的関数が最小になるように赤線です。各時間において赤線の分Shopperを用意すればIdlenessとLost Delivieriesをいい感じに抑えることができます。


## Recap

実際のところIstacartでは余剰を抱えがちだった商品ではIdlenessが、タイトな人員でやっていた商品ではLost Deliveriesをともに減らすことができました。[参照](https://tech.instacart.com/no-order-left-behind-no-shopper-left-idle-24ba0600f04f#---0-7)

Monte Carlo simulationはシンプルな方法ですが、この様に現実の問題を解くために使うことのできる強力なアルゴリズムだということが改めてわかりました。

## Reference

* [Instacart is Launching 100+ Cities in America’s Heartland!](https://news.instacart.com/instacart-launching-the-next-100-cities-2fb140dedbbf)
* [No order left behind; no shopper left idle.](https://tech.instacart.com/no-order-left-behind-no-shopper-left-idle-24ba0600f04f)
* [Instacart](https://en.wikipedia.org/wiki/Instacart)
* [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method)
