---
title: "Babel add-module-exports"
layout: post
date: 2017-10-04 16:03:57 +0900
image: 'images/'
description:
tag: ["JavaScript", "ES6", "ES2015", "Babel"]
blog: true
author: "lewuathe"
---

I'm now trying to convert [td-client-node](https://github.com/treasure-data/td-client-node) codebase to ES6. Since ES6 provides us bunch of useful features and syntax which are not available in ES5. But nodejs (and backend V8) does not support full functionalities of ES6. You can check the overview of supported ECMAScript features by nodejs in [this website](http://node.green/). [This blog post](https://nodejs.org/en/docs/es6/) explained the detail of milestone to support ES6 features.

So here is [Babel](https://babeljs.io/). Babel is a transpiler to convert ES6 codebase into ES5 code which can be run on nodejs. The usage of Babel is described [here](https://babeljs.io/docs/setup/) in detail. And overall Babel can convert my td-client-node codebase properly except for one thing. 

Babel now does not support [CommonJS default export behavior](https://github.com/babel/babel/issues/2212). In short, we cannot export a class directly from module anymore.

```javascript
var TD = require('td');

val client = new TD(process.env.TREASURE_DATA_API_KEY);
```

It throws such exception.

```
var client = new TD(process.env.TREASURE_DATA_API_KEY);
             ^

TypeError: TD is not a constructor
    at Object.<anonymous> (/path/to/test.js:4:14)
    at Module._compile (module.js:573:30)
    at Object.Module._extensions..js (module.js:584:10)
    at Module.load (module.js:507:32)
    at tryModuleLoad (module.js:470:12)
```

Looking the transpiled code, we can detect the cause. We need to refer the client class through `default` properly of exported object. 

```javascript
exports.default = TDClient;
```

Although we expect `module.exports = TDClient`, Babel core does not support such thing. 

Then you can use [Babel add-module-exports plugin](https://github.com/59naga/babel-plugin-add-module-exports). What this plugin does is very simple. Just adding one line, `exports.default = exports['default']`. 

```
exports.default = TDClient;
module.exports = exports['default'];
```

By using this plugin you don't have to use ugly `default` keyword in require statement. 

```
$ npm install babel-plugin-add-module-exports --save-dev
```

```
$ cat .babelrc
{
  "presets": ["env"],
  "plugins": [
    "add-module-exports"
  ]
}
```

## Reference

* [Babel](https://babeljs.io/)
* [59naga/babel-plugin-add-module-exports](https://github.com/59naga/babel-plugin-add-module-exports)
* [ECMAScript 2015 (ES6) and beyond](https://nodejs.org/en/docs/es6/)

