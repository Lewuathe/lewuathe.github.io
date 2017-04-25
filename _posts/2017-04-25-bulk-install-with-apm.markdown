---
title: "Bulk install with APM"
layout: post
date: 2017-04-25 17:12:28 +0900
image: 'images/'
description:
tag: ["APM", "Atom"]
blog: true
author: "lewuathe"
---

There are a lot of packages of [Atom](https://atom.io/) text editor. You can customize your Atom by using official packages or third party packages. But how do you manage the list of packages?

There is a way which looks similar to [requirements file of pip](https://pip.pypa.io/en/stable/user_guide/#requirements-files). First you can dump all APM packages you installed.

```
$ apm list --installed --bare
atom-beautify@0.29.23
atom-ctags@5.0.0
atom-material-syntax@1.0.2
atom-material-syntax-dark@0.2.7
atom-material-ui@1.3.9
autocomplete-java@1.2.5
...

$ apm list --installed --bare > installed.txt
```

Then you can restore with this file from clean installed Atom.

```
$ apm install --packages-file installed.txt
```

Very easy. So you only need to update the file every time when you update the package or install new package. Then you can restore the latest Atom environment with one comment. 
