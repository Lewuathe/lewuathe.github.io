---
title: "Create TensorFlow.js Project with Parcel"
layout: post
date: 2019-03-31 16:05:36 +0900
image: 'assets/img/posts/2019-03-31-create-tensorflow/catch.jpg'
description:
tag: ['TensorFlow', 'DeepLearning', 'Web']
blog: true
author: "Kai Sasaki"
---

Creating a web application is often troublesome due to the complexity of the framework and ecosystem. There are a bunch of build systems to launch the project. We also need to be familiar with the difference between programming languages used by web applications (e.g. JavaScript, AltJS, TypeScript). It may be a common sense especially to those who are not familiar with the latest web technologies as it changes so quickly.

[**Parcel**](https://parceljs.org/) is a tool to bundle all assets needed for an application into one package. You can use it immediately without writing any configuration. I found it's so beneficial to use Parcel for creating TensorFlow.js application quickly. It cares to compile TypeScript, dependency resolution and package bundle on behalf of me. In this article, I'm going to introduce the way how to create TensorFlow.js application in a few minutes by using Parcel.

First, you need to create the application directory in your machine. Then as you may usually do, you prepare the npm package in the directory. 

```
$ mkdir myapp
$ cd myapp
$ npm init -y
```

It will create an initial `package.json`. Please make sure to add TensorFlow.js as a dependency as follows. The pre-trained models of TensorFlow.js may be also useful.

```
  "dependencies": {
    "@tensorflow/tfjs": "^1.0.3",
    "@tensorflow-models/mobilenet": "^1.0.0",
    "parcel": "^1.12.3"    
  }
```

You may need to ensure the dependencies are installed properly by running `npm i`.
Then let's write the source code of the application. The structure of application looks like as follows.

```
$ tree .
.
├── package.json
└── src
    ├── cat.jpg
    ├── index.html
    └── index.ts

1 directory, 3 files
```

The following shows the `index.html` and `index.ts`. One of the great thing of Parcel is that **it can automatically detect the resource used in the application.** In this case, `cat.jpg` and `index.ts` are compiled and bundled into the artifact directory, `dist`.

```html
<script src="index.ts"></script>

<div style='display: flex'>
  <img id="img" src="cat.jpg"/>
</div>
```

```ts
import * as mobilenet from '@tensorflow-models/mobilenet';

async function run(img: HTMLImageElement) {
  // Load the MobileNetV2 model.
  const model = await mobilenet.load(2, 1.0);

  // Classify the image.
  const predictions = await model.classify(img);
  console.log('Predictions');
  console.log(predictions);
}

// Ensure to load the image.
window.onload = (e) => {
  const img = document.getElementById('img') as HTMLImageElement;
  run(img);
}
```

Surprisingly, all things are already prepared to start the application. Let's run the application with Parcel development server.

```
$ npx parcel src/index.html --open
```

This command automatically builds the package and open the web browser. Writing a deep learning application itself is not always easy. You may want to focus on writing the core of the application such as improving the accuracy of the model or collecting the datasets. Parcel can be a tool to help you boost your creativity of building the web application leveraged by deep learning.

If you want to learn more about client side deep learning, <a target="_blank" href="https://www.amazon.com/gp/product/B07GNZPP2P/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B07GNZPP2P&linkCode=as2&tag=lewuathe-20&linkId=dbcf9b5fbf7a8d9670420b4e8141cc77">Deep Learning in the Browser</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=B07GNZPP2P" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" /> is a good introduction to get used to the deep learning framework written in JavaScript or TypeScript and bootstrap your own web application with deep learning.

<p style='text-align: center'>
<a target="_blank"  href="https://www.amazon.com/gp/product/B07GNZPP2P/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B07GNZPP2P&linkCode=as2&tag=lewuathe-20&linkId=3c29af65ee0344d26fe74525e474878f"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=B07GNZPP2P&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=lewuathe-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=am2&o=1&a=B07GNZPP2P" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</p>

Thanks!