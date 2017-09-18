---
title: "Prime Day and AWS"
layout: post
date: 2017-09-18 17:54:14 +0900
image: 'images/'
description:
tag: ["AWS", "Paper"]
blog: true
author: "lewuathe"
---

Amazon Prime DayでAWSがどんな役割を果たしたか。そんなレポートがAWSのブログにのっていました。

* [Prime Day 2017 – Powered by AWS](https://aws.amazon.com/blogs/aws/prime-day-2017-powered-by-aws/)

Prime Dayは年に一度Amazon上で開催されるプライム会員対象のセールで幅広い商品のお値段が安くなるみたいです。"*デー*"とはいいつつも、反響が大きかったため今では一回に30時間続くみたいです。

Amazonではこの日を大きな商機ととらえているようですが、それを支えるインフラ（AWS）としては一日に普段の何倍ものアクセス、トランザクションが発生するので念入りに準備を行うそうです。
システムがダウンしてしまったらその分の利益が飛んでしまいますし。毎年Prime Dayが終わった次の日から以下のような準備を進めるそうです。（この話を聞いて僕は["Nightmare Before Christmas"](https://en.wikipedia.org/wiki/The_Nightmare_Before_Christmas)を思い浮かべました。）

* **Auditing**: リスクの特定、進捗管理、技術的な課題の洗い出しなど想定される一般的なタスクをこなしていきます。連絡フローなど事務的な処理も含まれます。
* **GameDay**: 予行演習。On-callやOpsチームのシフトなども考慮してCatastorophicテストなども行う本格的なものです。考案したのは[Jesse Robbins](https://en.wikipedia.org/wiki/Jesse_Robbins)という方でChef(旧Opscode)の創業者らしいです。

> GameDay: An exercise designed to increase Resilience through large-scale fault injection across critical systems. Part of a larger discipline called Resilience Engineering. Not new, just new to us ;-)

こういった試みは[Resilience Engineering](http://queue.acm.org/detail.cfm?id=2371297)というようです。

<iframe width="560" height="315" src="https://www.youtube.com/embed/zoz0ZjfrQ9s" frameborder="0" allowfullscreen></iframe>

この動画が詳しいです。GameDayでは迅速に障害に対処できるようチームで練習を行うので[The Calculus of Service Availability](https://cacm.acm.org/magazines/2017/9/220426-the-calculus-of-service-availability/fulltext)でも紹介されていた**Mean Time to Repair (MTTR)**を減らすことができます。

![resilience](images/posts/2017-09-18-prime-day-and-aws/resilience.png)

障害時の対応方法をRunbookやDocumentに残しておくことはよくありますが、実際にやってみないとそれが機能するのか、不備はないかということは分からないことは往々にしてあるのでGameDayのような取り組みはどんなエンジニアリングチームにおいても非常に効果的だと思いました。

## Recap

AWS上でこのようなイベントやキャンペーンを打つのは何もAmazonに限らないはずです。そんなユーザの対し*["Infrastructure Event Readiness"](https://d0.awsstatic.com/whitepapers/aws-infrastructure-event-readiness.pdf)*というWhite Paperが出されています。もしかしたらこういった内容はもっとCriticalなシステム（例えば医療機器や防衛システムなど）では当たり前のことかもしれませんが、WebサービスやEコマースくらいだとなかなかコストと時間をかけてやらないことも多いと思います。

それに得てしてエンジニアリングは技術的に解決することに主眼を起きがちですが（それがエンジニアリングの目的なので当然といえば当然ですが）GameDayのように地道に練習をしておき"build confidence"しておくというのも同時に必要なことじゃないかなと感じました。

## Referece

* [Amazon Prime Day](https://www.amazon.com/Prime-Day/b?ie=UTF8&node=13887280011)
* [Resilience Engineering: Learning to Embrace Failure](http://queue.acm.org/detail.cfm?id=2371297)
* [GameDay: Creating Resiliency Through Destruction](https://www.youtube.com/watch?v=zoz0ZjfrQ9s)
* [Rebooting a Cloud](https://www.slideshare.net/jesserobbins/rebooting-a-cloud)
* [Infrastructure Event Readiness](https://d0.awsstatic.com/whitepapers/aws-infrastructure-event-readiness.pdf)
　


