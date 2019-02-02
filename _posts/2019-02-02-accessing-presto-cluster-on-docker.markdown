---
title: "Run queries in your local Presto cluster on Docker"
layout: post
date: 2019-02-02 13:14:43 +0900
image: 'assets/img/posts/2019-02-02-accessing-presto-cluster-on-docker/catch.png'
description:
tag: ['Presto', 'Docker', 'SQL']
blog: true
author: "Kai Sasaki"
---

Once I created a tool to launch a Presto cluster in your local machine by using Docker a few years ago. 

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://github.com/Lewuathe/docker-presto-cluster" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fgithub.com%2FLewuathe%2Fdocker-presto-cluster&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

This tool enables you to launch your Presto cluster with multiple nodes (i.e. multiple Docker containers) so that you can easily test your own connector or improvements in the environment close to the production environment. I described the detail of the framework in the previous posts.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://www.lewuathe.com/launch-distributed-system-with-docker-compose.html" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fwww.lewuathe.com%2Flaunch-distributed-system-with-docker-compose.html&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>


Yesterday, I've got a question about the usage of the framework about how to connect to the Presto cluster and submit queries. So I'm going to describe the way to access the Presto cluster running on your local machine with Docker.

<div style='text-align: center;'>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/Lewuathe?ref_src=twsrc%5Etfw">@Lewuathe</a> Hi, I happen to check your article on the multi node presto cluster. Although i am able to use it and kick it off. Am yet to figure out how do i connect to it and run some queries?</p>&mdash; anilkulkarni (@anilkulkarni) <a href="https://twitter.com/anilkulkarni/status/1091053516188114944?ref_src=twsrc%5Etfw">January 31, 2019</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>

# Presto Command Line Tool

Presto open source project provides a simple command line tool to submit SQL to any Presto cluster. That implements all protocols and interfaces necessary to run the query. You can get the tool from the official documentation site, "[2.2. Command Line Interface](https://prestosql.io/docs/current/installation/cli.html)". After you download the CLI, you should be able to use that like this.

```
$ chmod +x presto-cli-301-executable.jar
$ ./presto-cli-301-executable.jar --server localhost:8080 --catalog tpch
```

Since docker container of [docker-presto-cluster](https://github.com/Lewuathe/docker-presto-cluster/) exposes 8080 port to the host machine, the CLI can recognize the 8080 port just like as normal Presto cluster. A console is launched and you can now submit any query to the Presto cluster running Docker container.

# Presto Client Libraries

Of course, you can use any kind of Preto client libraries. Here is the list of client libraries as far as I recognize. 

|Language|Repository|
|:---|:---|
|Ruby|[treasure-data/presto-client-ruby](https://github.com/treasure-data/presto-client-ruby)|
|Node|[tagomoris/presto-client-node](https://github.com/tagomoris/presto-client-node)|
|Go|[prestodb/presto-go-client](https://github.com/prestodb/presto-go-client)|
|C|[easydatawarehousing/prestoclient](https://github.com/easydatawarehousing/prestoclient/tree/master/C)|
|Java|[JDBC Driver](https://prestodb.github.io/docs/current/installation/jdbc.html)|
|PHP|[360d-io-labs/PhpPrestoClient](https://github.com/360d-io-labs/PhpPrestoClient)|
|Python|[easydatawarehousing/prestoclient/](https://github.com/easydatawarehousing/prestoclient/tree/master/python)|
|R|[prestodb/RPresto](https://github.com/prestodb/RPresto)|

For example, you can use Ruby client as follows without any modification to the library itself.

```ruby
require 'presto-client'

# create a client object:
client = Presto::Client.new(
  server: "localhost:8080",   # Specify the exact port exposed by Docker container
  ssl: {verify: false},
  catalog: "tpch",
  schema: "default",
  time_zone: "US/Pacific",
  language: "English",
  http_debug: true,
)

# run a query and get results as an array of arrays:
columns, rows = client.run("select * from system.nodes")
rows.each {|row|
  p row  # row is an array
}
```

So overall, you can connect to the Docker container running coordinator process with 8080 by using any kind of existing tools without any modification as far as it exposes 8080 port to the host machine. You need `expose` directive in Dockerfile and port mapping in your `docker-compose.yml`.  "<a target="_blank" href="https://www.amazon.com/gp/product/1633430235/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1633430235&linkCode=as2&tag=lewuathe-20&linkId=89b59823e5f7da3db94e12b15bfbd7e5">Docker in Action</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1633430235" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />" is a good book to know the fundamental usage and interfaces of Docker. 

<div style='text-align: center;'>
<a target="_blank"  href="https://www.amazon.com/gp/product/1633430235/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1633430235&linkCode=as2&tag=lewuathe-20&linkId=fac0186ecc85ca14b9bc3caf877dfb58"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=1633430235&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=lewuathe-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1633430235" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</div>

But please let me know if you find something wrong around [docker-presto-cluster](https://github.com/Lewuathe/docker-presto-cluster) anytime. [Issues and pull requests](https://github.com/Lewuathe/docker-presto-cluster/issues) are always welcome. Thanks!
