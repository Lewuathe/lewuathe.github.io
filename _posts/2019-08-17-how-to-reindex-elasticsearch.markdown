---
title: "How to reindex Elasticsearch"
layout: post
date: 2019-08-17 11:01:07 +0900
image: 'assets/img/posts/2019-08-17-how-to-reindex-elasticsearch/catch.png'
description:
tag: ['Database', 'Elasticsearch']
blog: true
author: "Kai Sasaki"
---

Due to the nature of the database system, the schema definition should be evolved as time goes by.
We may need to add the type information for new columns, change the name of the same attribute.
Otherwise, the database would not be able to deliver the value expected by users. The evolution of database schema is
inevitable factor in the context of database systems used in the real business.

Even Elasticsearch requires us to update the definition of the index to meet our requirement from
the business perspective or engineering demand. [**Index**](https://www.elastic.co/blog/what-is-an-elasticsearch-index)
in Elasticsearch is a concept corresponding to the table in traditional RDBMS system. We are not going to avoid going to
further into the detail of Elasticsearch here. **<a target="_blank" href="https://www.amazon.com/gp/product/1449358543/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1449358543&linkCode=as2&tag=lewuathe-20&linkId=d31e4ecff5e54b819d3bd7939a86fdf6">Elasticsearch: The Definitive Guide: A Distributed Real-Time Search and Analytics Engine</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=1449358543" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />** will provide you the enough information to know the underhood of Elaticserch.

<p style='text-align:center;'>
<a href="https://www.amazon.com/Elasticsearch-Definitive-Distributed-Real-Time-Analytics/dp/1449358543/ref=as_li_ss_il?keywords=elasticsearch&qid=1566007861&s=gateway&sr=8-1&linkCode=li3&tag=lewuathe-20&linkId=b97bd1717aa37e8e9e1bd30b5c51c1fb" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=1449358543&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=lewuathe-20" ></a><img src="https://ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=li3&o=1&a=1449358543" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</p>

In this article, I'm going to illustrate the practice of how to update the existing index of Elasticsearch without downtime by using an alias and reindex API. Assume a current index (`myindex_v1`) is aliased to `myindex`.

# Create a new index

You can safely create a new index. The name of the new index is `myindex_v2`.

```sh
$ curl -H 'Content-Type: application/json' \
 -XPUT http://<Elasticsearch Host>/myindex_v2 \
 -d @create_index.json
```

You may want to install specific analyzer at the creation of a new index. This example shows the case to use Koromoji tokenizer to deal with the query of Japanese.

```sh
$ cat create_index.json
{
  "index": {
    "analysis": {
      "tokenizer": {
        "kuromoji": {
          "type": "kuromoji_tokenizer"
        }
      },
      "analyzer": {
        "analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji",
          "filter": [
            "cjk_width"
          ]
        }
      }
    }
  }
}
```

# Move data to the new index

Database migration is done by reindex operation in Elasticsearch.

```sh
$ curl -H 'Content-Type: application/json' \
 -XPOST http://<Elasticsearch Host>/_reindex \
 -d @reindex.json
```

The migration target and source index are specified in the body of the request.

```sh
$ cat reindex.json
{
  "source": {
    "index": "myindex_v1"
  },
  "dest": {
    "index": "myindex_v2"
  }
}
```

# Change the alias

If clients are accessing by the name `myindex`, the new index is not still visible to users because `myindex` is aliased to
`myindex_v1`. It is necessary to update the `myindex` alias to refer to `myindex_v2`.

```sh
$ curl -H 'Content-Type: application/json' \
 -XPOST http://<Elasticsearch Host>/_aliases \
 -d @alias.json
```

```sh
$ cat alias.json
{
  "actions": [
    {
      "add": {
        "index": "myindex_v2",
        "alias": "myindex"
      }
    }
  ]
}
```

Now the request to `myindex` is routed to `myindex_v2`. The benefit of using the alias is that we can avoid downtime and easily rollback the migration if there is something wrong in the new index. That's because just switching the alias can be completed quickly. Thus overall, making sure all clients access via alias not index is a recommended pattern to make these kinds of operation possible.

Thanks!