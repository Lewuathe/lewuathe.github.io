---
title: "The end of website has not come"
layout: post
date: 2017-09-11 09:11:31 +0900
image: 'images/'
description:
tag: ["Node", "JavaScript", "TypeScript"]
blog: true
author: "lewuathe"
---

After a long time, I wrote a module on [npm](https://www.npmjs.com/).

* [site-snapshot](https://www.npmjs.com/package/site-snapshot)

## Background

My father asked me to record his friend website in PDF. Since he died, there is no way to access
his website and source code. But my father wanted to keep the website for his family. The reason why
we need to record them in PDF format is here.

* His family are not good at computer. Keeping webpage source code in HTML, CSS is not desirable.
* PDF can be easily read and printed by his family.

His website is not so large. There are 20~30 pages in total. But I wanted to write a code to crawl webpage
and take a screenshot in PDF by using [Puppetteer](https://github.com/GoogleChrome/puppeteer) recently released
by Google. Then site-snapshot was created.

## Usage

Usage of site-snapshot is simple. First you need to write a path to be crawled in JSON format. We call it `site.json`.

```JSON
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

`site.json` is a tree whose element has

* `name` : The name of the page
* `children` : The child elements to be crawled next
* `selector` : jQuery formatted selector of the child element to be crawled.

![tree](images/posts/2017-09-11-the-ending-of-website/tree.png)

site-snapshot first takes a picture of `index` page, then searching child elements based on given selector.
You can specifies the pages to be taken in `site.json`. After all, the pages are stored in the directory
in the same structure to `site.json`.

```
$ tree index
index
├── index.html.pdf
└── menu
    ├── menu-about.pdf
    ├── menu-contact.pdf
    └── menu-writing.pdf

1 directory, 4 files
```

You can use site-snapshot by `siteshot` CLI.

```
$ siteshot --help

  Usage: siteshot [options]


  Options:

    -V, --version              output the version number
    -s, --sitefile [sitefile]  The path to site.json file
    -h, --help
```

## Never ending website

20~30 years has passed since internet had been widely used. There are amazingly a lot of website around the world.
Some are actively maintained, the others are ruined. Some are be able to reached from Google first page, the others are not. Some are popular, others are not. But all websites have their own history and maintainers. The end of the history
won't come even after the maintainer has died. Because there are readers on that website. Even if the server is stopped,
the website will keep living in PDF or in your heart.

I hope I can write such a website. 
