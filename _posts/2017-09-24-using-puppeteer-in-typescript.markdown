---
title: "Using Puppeteer in TypeScript"
layout: post
date: 2017-09-24 19:38:04 +0900
image: 'images/'
description: 
tag: ["TypeScript", "Puppeteer", "JavaScript"]
blog: true
author: "lewuathe"
---

Finally DefinitelyTyped provides the type definition of Puppeteer.

* [@types/puppeteer](https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/puppeteer)

[Puppeteer](https://github.com/GoogleChrome/puppeteer) is a node API for headless Chrome. It is easy to use and provides intuitive API. For example, here is a example in getting started.

```typescript
import * as puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://google.com');
  await page.pdf({path: 'google.pdf'});

  await browser.close();
})();
```

You would understand what it does even at first look. What we need to do to use Puppeteer in TypeScript are 1) Install Puppeteer and Puppeteer type definitin, 2) Include type definition file into `tsconfig.json`. 

```
$ npm install --save puppeteer
$ npm install --save-dev @types/puppeteer
```

Type definition file is put in `node_modules/@types/puppeteer/index.d.ts`.

```
{
  "compilerOptions": {
    "module": "commonjs",
    "lib": ["es2015", "dom"],
    // ...
  },
  "include": [
    "src",
    "node_modules/@types/puppeteer/index.d.ts"
  ]
}
```

You can use Puppetter without any warning now. 


