---
layout: post
blog: true
title: "Actor model with node cluster"
date: 2014-03-01 02:19:34 +0900
comments: true
categories: ["nodejs", "actor", "asynchronous"]
author: Kai Sasaki
---

If you want to implement asynchronous parallel system with nodejs, the best and easiest way might be using [cluster](http://nodejs.org/api/cluster.html).
Cluster module is easy to use and provides you faster implementation. I wrote somewhat Actor like code that uses cluster module. 

<!-- more -->

```js
var cluster = require('cluster');
var http = require('http');

// Get the number of core of your CPU
var numCPUs = require('os').cpus().length;

if (cluster.isWorker) {

    // Starting worker process
    console.log("I am worker " + process.pid);

    // Send master process a message
    process.send({ chat: "I am + " + process.pid });

	// Event handler that is called when this worker get a message
    process.on('message', function(msg) {
        console.log('Thank you receiving: ' + msg.chat);
    });
}

if (cluster.isMaster) {

    // Starting master process
    for (var i = 0; i< numCPUs; i++ ){

	    // Create worker process
        var worker = cluster.fork();
        console.log("worker forked: pid=" + worker.process.pid);

        // Catch the timing of worker death
        worker.on('death', function(worker) {
            console.log('worker ' + worker.process.pid + ' died');
        });

 		// Event hander that is called when the master get a message
        worker.on('message', function(msg) {
            console.log('master received: ' + msg.chat);
            worker.send({chat: 'Hi, I received: ' + msg.chat});
        });
    }
}


// In order to kill all process, you shouldn' forget below part
process.on('SIGINT', function() {
    if (cluster.isMaster) {
        console.log('master is killed: pid=' + process.pid);
    } else {
        console.log('worker is killed pid=' + process.pid);
    }
    process.exit(0);
});
```

With cluster, there are two types of actors. One is master process, and the others are worker processes.
You can let master process and worker process send message respectively. To sending worker a message from master, 
use `worker.send({text:"From master to worker"})`. On the other hand to sending master a message from worker process, 
use `process.send({text:"From worker to master"})`. 

This asynchronous model looks like Actor and message model. In this model, it is not necessary to implement exclusive control 
because all processes acts harmoniously with only messages. If I can take this model nicely into nodejs, [n42](https://github.com/Lewuathe/n42) 
will get better running performance. I'll try it.

Thank you

