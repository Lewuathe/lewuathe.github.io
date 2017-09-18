---
title: "You are only as available as the sum of your dependencies"
layout: post
date: 2017-09-17 21:59:52 +0900
image: 'images/'
description:
tag: ["CACM", "Paper", "SRE"]
blog: true
author: "lewuathe"
---

今月のCommunications of the ACMにSite Reliability Engineeringに関する面白い記事がありました。

* [The Calculus of Service Availability](https://cacm.acm.org/magazines/2017/9/220426-the-calculus-of-service-availability/fulltext)

GoogleのSREが書いたいわゆるSRE本は有名ですが、この記事はその一部のエッセンスを抜き出した記事でした。詳細はもちろんSRE本を読んだ方がいいのですが、 **"Rule of the Extra 9"**の話は興味深かったです。ブログタイトルはそのテーマを一言で表した記事のサブタイトルです。

## Rule of the Extra 9

サービスのAvailabilityは一般的には単位時間あたりの稼働時間の割合で表すことができます。

例えば365日中、1時間だけサービスのダウンタイムを許す場合Availabilityは99.99%(4 nines)と表すことができます。もし自分がサービス運用者であれば、自分のサービスをこのAvailabilityにSLO(Sertvice Level Objective)を設定しこれを満たすようにサービスを落とさずに運用することが求められます。

しかし多くのサービスはそれ単体では存在せず、他のサービスへ依存していることがほとんどです。例えば社内のインフラチームが提供するRDBMSサービスや社外のCDNサービスなど。もし自分のサービスが4nines(99.99%)を目指すのであれば、それが依存するサービスはもうひとつ桁の多い5nines(99.999%)を達成する必要がある、これが**Rule of the Extra 9**です。

依存するサービスは自サービスのSLOと同じかそれ以上のAvailabilityを達成しなければ、自サービスのSLOは守れないからです。

## For nested dependencies

じゃあ依存しているサービスが依存しているサービスはさらに9が2つもくっつくのかというと、そういうわけではなさそうです。現実にサービスのAvailabilityに直結するようないわゆる*Critical Dependency*はいくつも連なるのは現実的ではありません。

![incorrect](images/posts/2017-09-17-you-are-only-as-available-as-the-sum-of-your-dependencies/incorrect.png)

いくつも依存があったとしても考えるべきはCritical Dependencyとなるものだけで、しかも一度だけ考慮すればよいです。なぜならnested dependencyのどこにいようと彼らCritical Dependencyが障害を起こすとただちに自サービスの障害につながるからです。全体としてDependencyとAvailabilityの関係は以下のようになります。

* Critical DependencyがN個あった場合、それぞれがfirst order dependencyとしてRule of the Extra 9を適用される
* Nested Dependencyの中に幾つか同じものがあっても全体としては一つのCritical Dependencyとして数える

つまり結局は自サービスがN個のCritical Dependencyに直接依存しているという形で考えます。

> You are only as available as the sum of your dependencies

依存しているもの以上にはなれないということですね。

## Why extra "9"?

Critical Dependencyは自サービス(99.99%)以上のAvailabilityを達成できればよいので、99.992%でもよさそうな気はします。

一般にN個のCritical Dependencyはその上の階層のSLOの1/N倍の障害が許容されます。Critical Dependencyのどれに障害が起きても上の階層の障害になってしまうので、障害貢献度(言い方が適切かわかりませんが)はN個あればN倍になってしまいます。そのためそれぞれは1/Nの障害頻度に抑えないといけないわけです。たった1%の確率で壊れるハードウェアも100個並べると2/3くらいの確率でどれかしら壊れてしまうのと同じ理屈です。

実は多くの場合ひとつのサービスは5から10程度のCritical Dependencyを持っていると言われています。これを踏まえると大体1/5~1/10倍の障害頻度が許容され、例えばAvailability 99.99%のサービスのCritical Dependencyは0.01% * 1/10 = 0.001%、つまり99.999%のAvailabilityが求められることになります。逆にいうとCritical Dependencyが少なければ少ないほどこの数字はよりゆるいものにできるということですね。

実際Critical Dependencyを減らすというのはサービスを安定させるためのひとつの手段として記事でも紹介されています。SPOFをなくしたりCapacity Cacheを用意することが考えられます。

## Recap

他にもKey Definitionsとして紹介されていたSRE用語は大変勉強になりました。興味があれば読んでみてください。

## Reference

* [The Calculus of Service Availability](https://cacm.acm.org/magazines/2017/9/220426-the-calculus-of-service-availability/fulltext)
* [SRE Book](https://landing.google.com/sre/book.html)
* [The Three Types of Cache](https://www.robustperception.io/the-three-types-of-cache/)








