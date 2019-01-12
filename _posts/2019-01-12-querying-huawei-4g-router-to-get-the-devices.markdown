---
title: "Querying Huawei 4G router to get the devices"
layout: post
date: 2019-01-12 21:12:13 +0900
image: 'assets/img/posts/2019-01-12-querying-huawei-4g-router-to-get-the-devices/catch.jpg'
description:
tag: ["Huawei", "TypeScript", "Wifi", "Network", "API"]
blog: true
author: "Kai Sasaki"
---

Do you know Huawei 4G router provides a collection of API which accessible via HTTP? The API enables us to get the information of wifi router itself and even the devices connecting the router. That kind of API should be useful to make a tool in order to investigate the connectivity of the wifi router. This blog post will introduce the specification briefly and the way to accessing the endpoint to get the desired information.

# Table Of Contents
- Library to inspect the router API
- Sample code to get the device information

# Library to inspect the router API

There is a library to connect to the router API written in JavaScript. **dialog-router-api** enables us to access internal API easily.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://github.com/ishan-marikar/dialog-router-api" data-iframely-url="//cdn.iframe.ly/rvfb2Ee"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

You can install the library with `npm`.

```
$ npm install dialog-router-api
```

The internal API, of course, requires us the security credentials otherwise anyone can manipulate the administrative information in the router. 
The credential is a token encoded by SHA256 with given username and password. **dialog-router-api** creates the credential information on behalf of us
and then put them into the request header as the cookie of `__RequestVerificationToken`. 

The list of APIs is described in [`router.js`](https://github.com/ishan-marikar/dialog-router-api/blob/master/lib/router.js). 

|Library Method|Endpoint|Description|
|:---|:---|:---|
|`getMonthStatistics`|`/api/monitoring/month_statistics')`|Get stats of the usage|
|`getSignal`|`/api/device/signal`|?|
|`getStatus`|`/api/monitoring/status`|Get status for monitoring purpose|
|`getTrafficStatistics`|`/api/monitoring/traffic-statistics`|Get the traffic stats|
|`getBasicSettings`|`/api/wlan/basic-settings`|Get settings information|
|`getCurrentPLMN`|`/api/net/current-plmn` |Get public land mobile network|
|`getToken`|`/api/webserver/SesTokInfo`|[Get security token for POST request](https://github.com/arska/e3372/issues/1)|

In addition to them, I found another API endpoint to get the information of devices connecting the router, although it's not added **dialog-router-api**. `/api/wlan/host-list` will return the list of MAC address of devices connecting the router. By adding the code like this in dialog-router-api, you can get the information of the devices around the router.

```ts
API.getHosts = function(token, callback) {
  var uri = url('http://', this.options.gateway, '/api/wlan/host-list');
  utilities.contactRouter(uri, token, null, function(error, response) {
    callback(error, response);
  });
}
```

Let's try to get the MAC addresses of the devices!

# Sample code to get the device information

Here is the code to get the list of MAC address around the router. Although it's written in [TypeScript](https://www.typescriptlang.org/), you can use JavaScript too.
Please make sure your laptop is connected to a Huawei wifi router beforehand. The program can access the router by the IP `192.168.128.1`. 

![wifi](assets/img/posts/2019-01-12-querying-huawei-4g-router-to-get-the-devices/wifi.png)

```ts
import * as router from 'dialog-router-api';

export class Scraper {
 macAddresses() {
  (async () => {
    // Endpoint is always available in the specific IP address.
    const r = router.create({ gateway: '192.168.128.1' });
    r.getToken(function(error, token) {
      r.login(token, 'admin', 'admin', () => {
        r.getHosts(token, (err, hosts) => {
          const macAddresses = hosts.Hosts[0].Host.map((h) => {
            return h.MacAddress[0];
          })
        });
      });
    });    
   })();   
 }
}

let scraper = new Scraper();
scraper.macAddresses();
// -> [B7-B6-A1-72-00-00, ...]
```

The sample application that tried to use the endpoint is here.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://github.com/PhysicsEngine/huawei-alert" data-iframely-url="//cdn.iframe.ly/WFOgwVx"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

I'm not sure whether every Huawei router supports the same interface, but I confirmed **Huawei B315** and **602HW** supports the API. 
You are able to get the detail information of the devices connecting the router from your program. 
It is inspiring you to come up with something fun by using the API, isn't it?

Have fun!