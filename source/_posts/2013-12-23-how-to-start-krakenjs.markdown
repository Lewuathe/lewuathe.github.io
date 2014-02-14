---
layout: post
title: "How to start KrakenJS"
date: 2013-12-23 11:55
comments: true
categories: ["Node", "Kraken", "Express"]
author: Kai Sasaki
---

In this november, Paypal released KrakenJS which is web application framework based on Connect, Express. 

http://krakenjs.com/

I had a chance to using this framework at the ending of this year. So I want to inform the facility of this framwork.

**This article was written for [Node.js advent calendar](http://www.adventar.org/calendars/56) 24th day.** Please read previous articles.

## Getting started

### Install generator

Kraken uses [Yeoman](http://yeoman.io/) for building the bootstrap of application. So first, you need to install generator.

```
$ sudo npm install -g generator-kraken
```

### Create skelton

```
$ yo kraken

     ,'""`.
    / _  _ \
    |(@)(@)|   Release the Kraken!
    )  __  (
   /,'))((`.\
  (( ((  )) ))
   `\ `)(' /'

[?] Application name: MyTestApp
[?] Description: My first kraken application
[?] Author: Kai Sasaki
[?] Use RequireJS? (Y/n) n
```

Write down simple configurations of your application. [RequireJS](http://requirejs.org/) is a JavaScript file and module loader.
If you want to optimize loading of module scripts, this is good option. This command installs dependencies automatically.
So you don't need to type `npm install` again. After only these commands, you can start your application server.

### Start your server

```
$ cd MyTestApp
$ npm start
npm WARN package.json mytestapp@0.0.1 No repository field.

> mytestapp@0.0.1 start /Users/sasakiumi/MyTestApp
> node index.js

Multipart body parsing will be disabled by default in future versions. To enable, use `middleware:multipart` configuration.
connect.multipart() will be removed in connect 3.0
visit https://github.com/senchalabs/connect/wiki/Connect-3.0 for alternatives
connect.limit() will be removed in connect 3.0
Listening on 8000
```

Congratulations!! You can see your application through web browser.

![start page](/images/posts/2013-12-23-kraken/startpage.png)


## Structure

Directory structure is very simple. It is based on MVC framework which you might used to be.

```
/config
Application and middleware configuration

/controllers
Routes and logic

/lib
Custom developer libraries and other code

/locales
Language specific content bundles

/models
Models

/public
Web resources that are publicly available

/public/templates
Server and browser-side templates

/tests
Unit and functional test cases

index.js
Application entry point 
```

For a characteristic, locale settings are prepared as default. You can make your app international easily.
Because KrakenJS is based on Express, you can develop your own Connect stack as you did before.
In the `index.js` file, some functions which are prepared for each request statuses. These description is easier to understand 
than original connect framework. For example, `requestBeforeRout` means that this function will be called after request before rouring logic.
It's simple, isn't it?


```
'use strict';
 
var kraken = require('kraken-js'),
    app = {};
 
// Fired when an app configures itself
app.configure = function (nconf, next) {
    next(null);
};
 
// Fired at the beginning of an incoming request
app.requestStart = function (server) { };
 
// Fired before routing occurs
app.requestBeforeRoute = function (server) { };
 
// Fired after routing occurs
app.requestAfterRoute = function requestAfterRoute(server) { };
 
kraken.create(app).listen(function (err) {
    if (err) { console.error(err); }
});
```



## Modules

KrankenJS can include other utility modules for enterprise use. These are also made by Paypal.

* [Lusca](https://github.com/paypal/lusca): Application security for express apps.
* [Makara](https://github.com/paypal/makara): An i18n module for Dust.js.
* [Dust](https://github.com/paypal/adaro): A Dust.js view renderer for express
* [Kappa](https://github.com/paypal/kappa): A hierarchical npm-registry proxy

In this article, I won't write the detail of these modules. But these might be made for enterprise applications. 
Lusca and Kappa is necessary for secure and private development environment.

## Examples

* [Kraken Shopping Cart](https://github.com/lmarkus/Kraken_Example_Shopping_Cart)
* [Localization](https://github.com/lensam69/Kraken_Example_Localization)
* [Custom Configuration](https://github.com/lmarkus/Kraken_Example_Configuration)
* [Middle ware](https://github.com/lensam69/Kraken_Example_Custom_Middleware)

In this one month, the number of examples are increasing. Would you like to add your example to this list?

## Try it!

KrakenJS is on the way of development, if anything, is only on the first stage of a thing.
I could develop an application by using KrakenJS in 2 weeks. It's easy to use, user friendly, and 
it has nice libraries. I'll bet this framework can accelerate your speed of development.

Let's try it!!











