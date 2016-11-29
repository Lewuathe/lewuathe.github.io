---
title: "High Availability of InfluxDB"
layout: post
date: 2016-11-28 15:11:00 +0900
image: 'images/'
description:
tag: ["InfluxDB", "HA"]
blog: true
jemoji:
author: "lewuathe"
---

I'm now considering how to make InfluxDB highly available. InfluxDB runs on single node by default. It is necessary to make high available system by ourselves. I checked [this article](https://www.influxdata.com/high-availability/). In this post there are 5 options to be considered in my opinion.

- Backups
- High-Availability with Nginx
- Sharding
- InfluxDB Relay
- Clustering

InfluxDB is a time series database (TSDB). So it often stores realtime data which does not require restoring old data. Backups cannot be our solution in this context. We need to make realtime data highly available.

The second option is that load balancing with Nginx. The writing data or queries are dispatched by Nginx. Nginx always write same data into all InfluxDB instances. Data are replicated though writing cost is relatively high. Sharding is dispatching each data into one InfluxDB instance. It's scalable. But the data is only written in one InfluxDB, which means not replicated.

InfluxDB relay is an option developed by InfluxDB. Loadbalancer dispatches each request to InfluxDB relay and InfluxDB replicates requests to to each InfluxDB instance. So it combines Nginx and Sharding way. It's well balanced and we can obtain native developer support.

![InfluxDB Relay](/images/posts/2016-11-28-high-available-influxdb/influxdb-relay.png)

Clustering is only supported in InfluxCloud. It's not open sourced yet.

So overall I decided to try InfluxDB relay for highly available system of InfluxDB.

# InfluxDB Relay

The sample configuration can be like below.

```
[[http]]
# Name of the HTTP server, used for display purposes only.
name = "example-http"

# TCP address to bind to, for HTTP server.
bind-addr = "127.0.0.1:9096"

# Enable HTTPS requests.
ssl-combined-pem = "/etc/ssl/influxdb-relay.pem"

# Array of InfluxDB instances to use as backends for Relay.
output = [
    # name: name of the backend, used for display purposes only.
    # location: full URL of the /write endpoint of the backend
    # timeout: Go-parseable time duration. Fail writes if incomplete in this time.
    # skip-tls-verification: skip verification for HTTPS location. WARNING: it's insecure. Don't use in production.
    { name="local1", location="http://127.0.0.1:8086/write", timeout="10s" },
    { name="local2", location="http://127.0.0.1:7086/write", timeout="10s" },
]
```

InfluxDB relay returns success to client as soon as one of the InfluxDB instance returns success. If one of the InfluxDB returns 4XX, it will be returned to client too. Unless all servers return 5XX errors, this error won't be returned to client. So that's the reason why we should monitor 5XX error because we cannot detect that from client response.


reference: [High Availability](https://www.influxdata.com/high-availability/)
