---
title: "Ensure Query Result Consistency with TinyPresto"
layout: post
date: 2020-01-29 09:27:16 +0900
image: 'assets/img/posts/2020-01-29-ensure-query-result-consistency-with-tinypresto/catch.png'
description:
tag: ['Presto', 'SQL', 'Ruby']
blog: true
author: "Kai Sasaki"
---

Ensuring the query result consistency is a vital part of providing reliable service on top of the SQL execution engine. The business process of many users may depend on the findings and insight derived from the observation. If the result is wrong, their business should also go wrong. It's is a critical problem.

To ensure the query result consistency of Presto version to version, I have created a Gem package named [`tiny-presto`](https://rubygems.org/gems/tiny-presto). The reason why I chose Ruby is that our application is built with [Ruby on Rails](https://rubyonrails.org/). Thus it enables us to run any Presto SQLs and check the result on the unit test level. Under the hood, tiny-presto uses [Docker container for Presto](https://hub.docker.com/r/prestosql/presto) with the specific version. Since the prestosql community officially distributes it, we can make sure to verify the query result on the application side.

tiny-presto is a small library to run SQL on one node Presto cluster. It is pretty easy to use.

# Table Of Contents
1. How to use tiny-presto
2. Run query
3. Supported catalogs

# How to use tiny-presto

Please make sure to install Docker engine first so that the library download and run Docker containers.
See [how to install docker](https://docs.docker.com/install/)

Next, let's install the library.

```
$ gem install tiny-presto
```

# Run query

Only one line of code allows you to run a query and get the result.

```ruby
require 'tiny-presto'
rows = TinyPresto.run('show schemas')
# => [["default"], ["information_schema"]]
```

TinyPresto may fail to stop the cluster even after you have finished running queries. `ensure_stop` lets cluster terminate all Docker containers launched by tiny-presto.

```ruby
TinyPresto.ensure_stop
```

That's it!. It's so simple to use the library.

# Supported catalogs

tiny-presto uses the Docker image distributed by the [prestosql](https://prestosql.io/) community. It supports the following connectors.

- [JMX](https://prestosql.io/docs/current/connector/jmx.html)
- [memory](https://prestosql.io/docs/current/connector/memory.html)
- [TPC-H](https://prestosql.io/docs/current/connector/tpch.html)
- [TPC-DS](https://prestosql.io/docs/current/connector/tpcds.html)

Among them, only a memory connector permits the table to write. tiny-presto uses memory connector as default. If you want to use the different catalogs, you can launch the server and client separately.

```ruby
# Crete a cluster listening the localhost with 8080.
cluster = TinyPresto::Cluster.new('localhost')

# Start running
container = cluster.run

require 'presto-client'
# Setup preto-client-ruby to use 'tpch' catalog.
client = Presto::Client.new(server: 'localhost:8080', catalog: 'tpch', user: 'tiny-user')

client.run('show schemas')

cluster.stop
```

Please take a look at [treasure-data/presto-client-ruby](https://github.com/treasure-data/presto-client-ruby) for more detail of the client library.

And as usual, welcome [any feedback or patches](https://github.com/Lewuathe/tiny-presto)!

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=0596009763&asins=0596009763&linkId=0d6fc9570c399b3b10d97d8f4e716fa0&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
 </iframe>
<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=0134598628&asins=0134598628&linkId=128b8e10bf4f393ee87bbecd1e283db3&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
 </iframe>
<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1492036730&asins=1492036730&linkId=85f5cecde3246c44f6b91b7a401c251d&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
 </iframe>