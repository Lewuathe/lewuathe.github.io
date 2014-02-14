---
layout: post
title: "DevOpsDay Tokyo 2013に行ってきたよ"
date: 2013-09-28 10:37
comments: true
categories: [DevOpsDay,Tokyo]
author: lewuathe
---

![ノベルティ](/images/posts/2013-09-28-DevOpsDay/DevOpsDay-2013.jpg)

印象に残った話しをざっとまとめてみる。なぜならBlogをかくまでがDev Ops Dayだから！！


# "Making Operations Visible" Nick Galbreath

使いやすいツールとか紹介

DevOpsとはコミュニケーション（マシン間、人間の間、組織の間）

ビジネス側から見えないから価値がない

DevとOpsとBizで相互不信的な感じになると Destructiveですよね。だから、データを使おう（運用としてだけではなく、会社の仕組みとして）

ビジネス視点でのDevOpsと大事なことはコミュニケーションだと言い切ったところが新鮮だった。

Graphiteという統計可視化ツールの話。

https://github.com/graphite-project

Diamond brightcoveは使いやすい

StatsDの話。
リアルタイムに統計計算をしてくれる。ログイン回数とか。それをGraphiteに書き込んでいく。特徴的なのはUDPパケットで送信を行うところ。そのためアプリケーション自体には過負荷にならない。またハンドリングとか要らないからエラーが起きない、必要ない。


# "introduction to Sensu" Sean Porter

Sensuのお話。いろいろな機能をひとつにまとめて使いやすくしたよ。大事なコンセプトは以下。

* Autmatic client registration
* Utilize existing Nagios checks
* Handle network interrunptions
* Easy to drive with CM(chef)
* Easy to scale out
* **API**

Sonial（スポンサー）でしばらく使ってみて役に立つことがわかった

Sensuのワークフローとしては

1. Check
2. Result
3. Event
4. Handle

マシンの集まりに対して設定できる(roleみたいなものが設定できる)
JSONの設定ファイルを書いていくだけで使える。割と設定は簡単そう。
SensuはChefと相性が良さそう。

PagerDutyはテキストにもとづいてロボットが電話をかけてくる。日本で作りたい場合はTwilio使ってみましょうということだった。USBに入れられたVirtualBoxのimage入りのsandboxが配られた。すごいセットアップ簡単！
個人的にはGraphiteは見た目あんまりかっこよくないけど、SensuのSenseはいい（笑）

Chef + Sensu + PagerDutyは使えそう。今度自前で立ててみたい。

そして、お昼ごはん！久々の石巻復興弁当！

![石巻復興弁当](/images/posts/2013-09-28-DevOpsDay/DevOpsDay-2013_2.jpg)

途中からスポンサーさんのセッション。

Microsoftの偉大さと力強さを改めて実感。


# "Taking Devops to the Next Level" Max Martin

puppet labsの話 DepOpの次の段階へ。
Chefがもてはやされているけれど、Puppetも頑張っているよという話。
最近以下のアップデートとか頑張ったよ。

* Puppet3.x
* Hiera integration
* PuppetDB
* Mcollective2.x
* Geppetto
* Puppet Forge
* Puppet3.xは2.xとくらべてだいぶパフォーマンス上がったよ
* PuppetDBはClojureで書かれているよ、BaseはPostgreSQL、JVM上で動くよ


僕は用事があったのでここまで。DevOpsの概念というかスタンスみたいなものが結構聞けたのが収穫。技術的には、Sensuは自前で立てていろいろ弄ってみたいなと思った。

朝早起きだったから眠かったけれど、楽しいセッションばかりで良かった！





