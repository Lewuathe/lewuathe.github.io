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


<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1492037656&asins=1492037656&linkId=6db87816f1758ee4336f4ffa23376ac3&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>
<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1492053740&asins=1492053740&linkId=faa1f0fc49b3161d09cc325c0baf73bc&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>