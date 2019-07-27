---
title: "Inspect Presto connection with Charles"
layout: post
date: 2019-07-25 14:03:58 +0900
image: 'assets/img/posts/2019-07-25-inspect-presto-connection-with-charles/catch.png'
description:
tag: ['Presto', 'SSL', 'TLS', 'Procotol']
blog: true
author: "Kai Sasaki"
---

Seeing the unseen is the fundamental principle in debugging for software. The exchange of data between processes through the network is not visible literally. We often encountered the case when we need to inspect the data transmitted between multiple processes for debugging.

SSL/TLS connection is one of the famous examples where it is difficult to inspect the exchanged data due to its security. It must not be checked unnecessarily because it can contain sensitive data such as password or credit card number. The protocol is primarily designed to protect data privacy. Thus the problem is not simple, and we must do additional work to look into the data.

Unlike the ordinal web cases, I needed to inspect the data exchanged between [Presto client](https://prestosql.io/docs/current/installation/cli.html) and Presto coordinator to investigate the slow down problem. This article aims to describe how to examine SSL/TLS connection for Presto application.

# Charles for TLS Proxy

[Charles](https://www.charlesproxy.com/) is an HTTP proxy to monitor the procotol information. As it supports TLS proxy, it would match my use case this time. You can download Charles installer from [download page](https://www.charlesproxy.com/download/) and easily install it by obeying to the instruction. It is necessary to pay for using it permanently, but it's also available for 30 days for free use. I used the macOS version.

First thing you need to take care of is **macOS proxy**. macOS automatically acts as a proxy of all network connection of macOS, so your network connections running in the browser are also blocked. Disabling macOS proxy is recommended. Please go to `Proxy` >> `Proxy Settings...` and disable macOS proxy.

![macOS Proxy](/assets/img/posts/2019-07-25-inspect-presto-connection-with-charles/macos-proxy.png)

# Installing Certificates in Trust Store

Next thing we have to do is installing a certificate of Charles in your trust store. Presto client we are going to use is Java application. The trust store where the certificate is assumed to be installed is the default trust store of JDK. You can find the option to install a certificate from `Help` > `SSL Proxying` > `Install Charles Root Certificate in Java VMs`.

![Install Cert](/assets/img/posts/2019-07-25-inspect-presto-connection-with-charles/install-cert.png)

Although this is the simplest way to install a certificate, it may not work correctly (at least in my environment) due to the following error.

```
keytool error: java.lang.Exception: Input not an X.509 certificate
```

In that case, we need to install a certificate by hand. Please select `Save Charles Root Certificates...` instead and save the file as `.pem`  format. Then you can import the file in your trust store in the installed JDK.

```
$ sudo keytool -import -alias charles -file \
    ~/Desktop/charles-ssl-proxying-certificate.pem  \
    -keystore $JAVA_HOME/jre/lib/security/cacerts
```

Now your JDK can recognize the installed certificate.

# Send a request through Charles Proxy

Charles TLS proxy is listening to 8888 port as default and connection recording is running. You can specify the proxy host by `--http-proxy` in Presto client.

```
$ ./presto-cli-317-SNAPSHOT-executable.jar \
    --server http://your-presto-coordinator:8080 \
    --http-proxy localhost:8888 \
    --catalog tpch \
    --execute "select 1234"
```

Now, you can see all information about the HTTP traffic in Charles console.

# What is Slow Down Problem?

As I said previously, the reason why I inspected the traffic by Presto client is the slow down problem. I filed an issue in the community here.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 140px; padding-bottom: 0;"><a href="https://github.com/prestosql/presto/issues/1169" data-iframely-url="//cdn.iframe.ly/api/iframe?url=https%3A%2F%2Fgithub.com%2Fprestosql%2Fpresto%2Fissues%2F1169&amp;key=bdc42bc7d0ac2cb711b2a2dd9dadd063"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

The problem is using Presto client in JDK 11 environment caused the slow down issue. The only information I had gotten so far was the network is slow. Each HTTP request took a few minutes on average. Thus I inspected the actual traffic between Presto client and coordinator.

Charles is so powerful that I can quickly start the TLS proxy for monitoring traffic. It is necessary to purchase the license to make use of it entirely. But I believe it is worth to do so if you encountered the problem around TLS connection. It will accelerate the speed of debugging.

Thanks!