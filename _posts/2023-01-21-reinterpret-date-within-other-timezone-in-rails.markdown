---
title: "Reinterpret Date within other timezone in Rails"
layout: post
date: 2023-01-21 14:51:53 +0900
image: 'assets/img/posts/2023-01-21-reinterpret-date-within-other-timezone-in-rails/catch.jpg'
description:
tag: ['Rails', 'Ruby', 'Web']
blog: true
author: "Kai Sasaki"
---

The [`Date`](https://api.rubyonrails.org/classes/Date.html) type in Rails does not retain the timezone information. The default timezone is consistent with the system Rails provides. But it's implicit, so we should never forget which timezone we use as a Date type.

We can use [`in_time_zone`](https://apidock.com/rails/DateTime/in_time_zone) to be explicit about which timezone we are aware of.

```ruby
pry(main)> d = Date.new(2023, 1, 20)
=> Fri, 20 Jan 2023
pry(main)> d.to_time
=> 2023-01-20 00:00:00 +0000
pry(main)> d.in_time_zone('Asia/Tokyo')
=> Fri, 20 Jan 2023 00:00:00.000000000 JST +09:00
pry(main)> d.in_time_zone('Canada/Eastern')
=> Fri, 20 Jan 2023 00:00:00.000000000 EST -05:00
```

`in_time_zone` returns the [TimeWithZone](https://api.rubyonrails.org/classes/ActiveSupport/TimeWithZone.html) which inherently retains the timezone information. It's useful to pass the timezone identifier in string type without changing the system configuration.

And the book, [Agile Web Development with Rails 6](https://amzn.to/3H3WcIO) will be a more comprehensive guide to understanding the timezone structure in Rails.

<a href="https://www.amazon.com/Agile-Web-Development-Rails-6/dp/1680506706?crid=2WKS97E5DWBYI&keywords=rails&qid=1674281074&s=books&sprefix=rails+%2Cstripbooks-intl-ship%2C203&sr=1-1&linkCode=li2&tag=lewuathe-20&linkId=b431e457c7af39724b96dbdc817ccdf9&language=en_US&ref_=as_li_ss_il" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=1680506706&Format=_SL160_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=lewuathe-20&language=en_US" ></a><img src="https://ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&language=en_US&l=li2&o=1&a=1680506706" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />