---
layout: post
title: "Reference configuration library in nodejs"
date: 2013-12-30 20:24
comments: true
categories: ["node", "JavaScript", "readonly", "npm"]
author: Kai Sasaki
---

I made npm module at the end of this year, *readonly*.

[lewuathe/readonly @GitHub](https://github.com/Lewuathe/readonly)

[readonly @npm](https://npmjs.org/package/readonly)

readonly is a simple reference restriction library between custom modules in node object.
When you want to configure access control of specific object from respective modules, this is good option.
For example, you made two modules, both use the same object.

```js
// obj is uses from moduleA and moduleB
// You want moduleA to read and update obj, but moduleB to read obj only.
var obj = {'A':'a','B':'b','C':'c'};

// Embedded in moduleA
var moduleA = {};
moduleA.obj = obj;

// Readonly restriction of `obj` from moduleB
var moduleB = {};
moduleB.obj = readonly(obj);

// You can update `obj` from moduleA
moduleA.obj.A = "d";
// But you cannot update `obj` from moduleB
moduleA.obj.B = "e";  // Error
```

In this situation, you can use **readonly**.

## Install 

```
$ npm install readonly
```

## Usage

```
var readonly = require('readonly');

var obj = {'A':'a','B':'b','C':'c'};

// Normal ACL. You can use `obj` through moduleA as you like
var moduleA = {};
moduleA.obj = obj;

// Readonly restriction of `obj` in moduleB
var moduleB = {};
moduleB.obj = readonly(obj);

// You can update `obj` from moduleA
moduleA.obj.A = "d";
// This updates can be seen from moduleB
console.log(moduleB.obj.A); // --> "d"

// But if you update `obj` through moduleB, it will throws `UnableRewriteException`
moduleA.obj.B = "e";  // --> UnableRewriteException: original cannot be rewrite
```

With this library, you can access current property from restricted modules if original object is updates.
In above example, `moduleB.obj.A` returns `"d"`. Try it.
If you find any bugs, please inform me with [GitHub](https://github.com/Lewuathe/readonly/issues)


Enjoy **readonly** !







