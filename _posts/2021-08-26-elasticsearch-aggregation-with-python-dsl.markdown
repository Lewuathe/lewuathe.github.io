---
title: "Elasticsearch Aggregation with Python DSL"
layout: post
date: 2021-08-26 10:46:36 +0900
image: 'assets/img/posts/2021-08-26-elasticsearch-aggregation-with-python-dsl/catch.jpg'
description:
tag: ['Elasticsearch', 'Python']
blog: true
author: "Kai Sasaki"
---

When I write some trivial code to manipulate the Elasticsearch cluster, one question jumps into my head.

*"Does aggregation take into account all matched documentations even if we specify the from and size parameters?"*

For instance, we have 100 documents in Elasticsearch and run a query only matching 50 documents within that index with a size limit of 10. (e.g., pagination) How does the aggregation work? Does the aggregation value work on the whole documentation collection or just what is on the current page?

## Prerequisites

Let's say we have the following documents in the index.

```json
[
  {
    "title": "Title1",
    "author": "SomeAuthor",
    "contents": "Content1",
    "published_at": "2021-01-01"
  },
  {
    "title": "Title2",
    "author": "SomeAuthor",
    "contents": "Content2",
    "published_at": "2021-01-02"
  },
  {
    "title": "Title3",
    "author": "AnotherAuthor",
    "contents": "Content3",
    "published_at": "2021-01-03"
  },
  {
    "title": "Title4",
    "author": "AnotherAuthor",
    "contents": "Content4",
    "published_at": "2021-01-04"
  },
  {
    "title": "Title5",
    "author": "AnotherAuthor",
    "contents": "Content5",
    "published_at": "2021-01-05"
  },
]
```

A query I've written by using [elastcisearch-dsl](https://elasticsearch-dsl.readthedocs.io/en/latest/) looks as follows:

```python
from elasticsearch_dsl import Search, Q, A

search_query = Search(using=client, index=index_name)
search_query = search_query.filter(
    "range", published_at={"gte": "2021-01-01", "lte": "2021-01-03"}
)
```

This search should match three documents in the index, `Title1`, `Title2` and `Title3`. Okay, now let's add an aggregation to count the documents by the author's name.

## Aggregation by Author

The following code generates a query to count the documents by author.

```python
author_count = A("terms", field="author")
search_query.aggs.bucket("author_count", author_count)
```

The response will look like this,

```json
{
  "aggs": {
    "author_count": {
      "buckets": [
        {"key": "SomeAuthor", "doc_count": 2},
        {"key": "AnotherAuthor", "doc_count" :1}
      ]
    }
  }
}
```

The document count reflects the context of the search query. It aggregates the value from the set of documents matching the given query. What will happen if we add the `size` parameter?

## From and Size

elasticsearch-dsl allows us to set the parameter for the pagination. The way to do so is even more Pythonistas! It uses a slice of the list in Python.

```python
search_query = search_query[0:3]
```

It adds the following parameters in the request and omits the last document we've seen previously.

```json
 {
   "from": 0,
   "size": 2
}
```

How about the aggregation value? As we expect, it remains unchanged. The `from` and `size` parameters are designed to be used for the pagination. Aggregation values should not be affected because users may want to show the metrics or statistics of the whole population, not the documents on the page. Therefore we can use the aggregation value without caring much which page we are now located in.