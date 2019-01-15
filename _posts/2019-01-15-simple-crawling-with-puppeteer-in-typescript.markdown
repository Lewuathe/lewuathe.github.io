---
title: "Simple web crawling with Puppeteer in TypeScript"
layout: post
date: 2019-01-15 19:51:53 +0900
image: 'assets/img/posts/2019-01-15-simple-crawling-with-puppeteer-in-typescript/catch.png'
description:
tag: ['TypeScript', 'Puppeteer', 'Crawling', 'Web', 'JavaScript']
blog: true
author: "Kai Sasaki"
---

[Puppeteer](https://github.com/GoogleChrome/puppeteer) is a tool to manipulate web page by using headless Chrome. It can access pre-rendered content so that
we can touch the page which could not be accessed without web browsers. Puppeteer can be controlled by node.js since it's providing JavaScript API.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://github.com/GoogleChrome/puppeteer" data-iframely-url="//cdn.iframe.ly/2KLWi8I"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

So it's also true that we can control Puppeteer by using [TypeScript](https://www.typescriptlang.org/) which is a superset of JavaScript language. 
The code in TypeScript has its own type system and at the same time, it can be compiled into JavaScript. Instead of using directly JavaScript to control Puppeteer,
it's far better to use TypeScript, I think. In this blog post, I tried to create a simple web crawler to capture the PDFs of each web page.


# Table of Contents
- Installing Puppeteer
- Crawler Implementation
- site-snapshot

# Installing Puppeteer

As you may already know, TypeScript can be easily integrated with the npm package system. The dependencies can be written in `package.json` file. Please make sure to install your own TypeScript compiler in advance so that you can compile the project by running `npm build`.

```json
{
  "name": "simple-crawler",
  "version": "0.1.0",
  "description": "Create a screenshot of web page in PDF",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  },
  "files": [
    "bin",
    "dist",
    "package.json"
  ],
  "author": "Kai Sasaki",
  "license": "MIT",
  "dependencies": {
    "@types/node": "^8.0.27",
    "events": "^1.1.1",
    "puppeteer": "^0.10.2"
  },
  "devDependencies": {
    "puppeteer-tsd": "0.0.2"
  },
  "main": "./dist/index.js"
}
```

As you can see later, the compiler will generate JavaScript files under the directory `dist`. So the path to the main file is set to `./dist/index.js`. 
Another thing you may notice is about type definition file. `@types/node` and `puppeteer-tsd` are the files keeping the type information of classes used in node and Puppeteer respectively. 
The compiler may produce type check failure without these files. Please don't forget to include them.

TypeScript compiler reads `tsconfig.json` file in order to refer compile options. You can customize the configuration but please keep in mind to include the type definition file written as `node_modules/puppeteer-tsd/src/index.d.ts`. The compiler cannot find the type definition of Puppeteer classes without it.

```json
{
    "compilerOptions": {
        "module": "commonjs",
        "noImplicitAny": false,
        "sourceMap": true,
        "removeComments": true,
        "preserveConstEnums": true,
        "declaration": true,
        "target": "es5",
        "lib": ["es2015", "dom"],
        "outDir": "./dist",
        "noUnusedLocals": true,
        "noImplicitReturns": true,
        "noImplicitThis": true,
        "noUnusedParameters": false,
        "pretty": true,
        "noFallthroughCasesInSwitch": true,
        "allowUnreachableCode": false
    },
    "include": [
      "src",
      "node_modules/puppeteer-tsd/src/index.d.ts"
    ]
}
```

Source files in TypeScript are positioned `src` directly so that TypeScript compiler can compile source files along with the type definition of Puppeteer. 

# Crawler Implementation

It's hard to crawl all web pages existing in the world. Only Google can achieve this. So our crawler is designed to traverse the web pages according to the given web site structure file, `site.json`. The file looks like this.

```json
{
  "name": "index",
  "selector": null,
  "baseUrl": "http://www.lewuathe.com",
  "children": [
    {
      "name": "menu",
      "selector": ".element",
      "children": []
    }
  ]
}
```

This file tells the crawler to visit [`https://www.lewuathe.com/`](https://www.lewuathe.com/) first and then keep traversing the links specified by the `children` tags. 
`selector` is a pointer to the HTML element to be visited by the crawler. As you can see, children can be defined in a nested manner. Here is the implementation of our crawler. 

```ts
import {URL} from 'url';
import {mkdirSync, existsSync} from 'fs';
import * as puppeteer from 'puppeteer';

export class Crawer {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }
 
  crawl(site: any) {
    (async () => {
      // Wait for browser launching.
     const browser = await puppeteer.launch();
     // Wait for creating the new page.
     const page = await browser.newPage();
  
     await this.crawlInternal(page, `${this.baseUrl}/index.html`, site["children"], site["name"]);
  
     browser.close();
    })();
  }

  /**
   * Crawling the site recursively
   * selectors is a list of selectors of child pages.
   */
  async crawlInternal(page: any, path: string, selectors: [string], dirname: string) {
    // Create a directory storing the result PDFs.
    if (!existsSync(dirname)) {
      mkdirSync(dirname);
    }

    // Go to the target page.
    let url = new URL(path);
    await page.goto(path, {waitUntil: 'networkidle'});
    // Take a snapshot in PDF format.
    await page.pdf({path: 
      `${dirname}/${url.pathname.slice(1).replace("/", "-")}.pdf`, format: 'A4'});
    if (selectors.length == 0) {
      return;
    }
  
       // Traversing in an order of BFS.
    let items: [string] = await page.evaluate((sel) => {
      let ret = [];
       for (let item of document.querySelectorAll(sel)) {
        let href = item.getAttribute("href");
        ret.push(href);
       }
       return ret;
    }, selectors[0]["selector"]);
  
    for (let item of items) {
      console.log(`Capturing ${item}`);
      await this.crawlInternal(page, 
        `${item}`, selectors[0]["children"], `${dirname}/${selectors[0]["name"]}`)
    }
  }
}
```

Puppeteer APIs are basically called asynchronous manner. If you want to call the crawling synchronously, you need to write `await` keyword in each call. 
The crawler visits all pages with [depth first search algorithm](https://en.wikipedia.org/wiki/Depth-first_search). The crawler just checks every page specified
by `site.json` so that we don't need to worry about the infinite loop caused by the circular linkage between pages.

# site-snapshot

Actually, this crawler is published in npm with name **site-snapshot**. I created this tool to make PDFs of the pages our own web site.

<div class="iframely-embed"><div class="iframely-responsive" style="height: 168px; padding-bottom: 0;"><a href="https://github.com/Lewuathe/site-snapshot" data-iframely-url="//cdn.iframe.ly/eAl8ioZ"></a></div></div><script async src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>

The background I created the tool was described here.

[The end of website has not come](https://www.lewuathe.com/the-ending-of-website.html)

I hope you enjoy the web crawling with Puppeteer. Thanks!