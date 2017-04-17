---
title: "QueueManager and Resource Group in Presto"
layout: post
date: 2017-04-17 17:15:26 +0900
image: 'images/'
description:
tag: ["Presto", "SQL"]
blog: true
jemoji:
author: "lewuathe"
---

[Presto](http://prestodb.io/) is a fast distributed SQL engine originally developed by Facebook. From [0.153](https://prestodb.io/docs/current/release/release-0.153.html), pluggable resource group was introduced. This feature enables us to separate cluster resource in account workload. For example, you want to ensure daily batch job resource allocation even if you submit some adhoc queries. In short when 3 concurrent queries are permitted in total, you can ensure to keep some of query allocation even 3 or more queries of batch job are submitted in advance.

![resource group](images/posts/2017-04-17-queue-manager-and-resource-group/resource-group.png)

If batch job is submitted to batch resource group, it can be guaranteed to run at least 1 query any time.

So how can it be achieved? I found resource group is basically implemented like queue mechanism of Presto. Queue mechanism of Presto is realized by [`QueryQueueManager`](https://github.com/prestodb/presto/blob/c73359fe2173e01140b7d5f102b286e81c1ae4a8/presto-main/src/main/java/com/facebook/presto/execution/QueryQueueManager.java).

```java
/**
 * Classes implementing this interface must be thread safe. That is, all the methods listed below
 * may be called concurrently from any thread.
 */
@ThreadSafe
public interface QueryQueueManager
{
    void submit(Statement statement, QueryExecution queryExecution, Executor executor);
}
```

This interface receives `QueryExecution` which stores various information needed to run query. Before resource manager, only `SqlQueryQueueManager` implements this interface. It only controls running queries and queued queries. Actual `QueryQueueManager` is injected in advance.

```java
public class CoordinatorModule
        extends AbstractConfigurationAwareModule
{
  @Override
  protected void setup(Binder binder)
  {
    if (buildConfigObject(FeaturesConfig.class).isResourceGroupsEnabled()) {
      binder.bind(QueryQueueManager.class).to(InternalResourceGroupManager.class);
    }
    else {
      binder.bind(QueryQueueManager.class).to(SqlQueryQueueManager.class).in(Scopes.SINGLETON);
      binder.bind(new TypeLiteral<List<QueryQueueRule>>() {}).toProvider(QueryQueueRuleFactory.class).in(Scopes.SINGLETON);
    }
  }
}
```

Therefore from `SqlQueryManager` side, these two implementations can be used transparently. Actually all `SqlQueryManager` does is `submit`ting.

```java
// start the query in the background
queueManager.submit(statement, queryExecution, queryExecutor);
```

So actual handling and resource management can be delegated to each implementations (`SqlQueueQueueManager` and `InternalResourceGroupManager`).

I'll describe the detail of resource management mechanism of `InternalResourceGroupManager`.

Thanks.
