---
title: "1Password Shell Plugin Now Supports TreasureData Toolbelt"
layout: post
date: 2023-03-24 11:25:41 +0900
image: 'assets/img/posts/2023-03-24-1password-shell-plugin-now-supports-treasuredata-toolbelt/catch.jpg'
description:
tag: ['TreasureData', 'Security', 'CLI']
blog: true
author: "Kai Sasaki"
---

# 1Password Shell Plugin Update Adds Support for TreasureData Toolbelt

1Password will release an update to its shell plugin that adds support for the TreasureData Toolbelt. The TreasureData Toolbelt is a command-line interface (CLI) tool that allows users to interact with the TreasureData platform.

<iframe width="560" height="315" src="https://www.youtube.com/embed/7aT4K1AMfGI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

I have submitted a pull request to support [this](https://github.com/1Password/shell-plugins/pull/176) and it's merged into master branch.

You can use this plugin with 1Password CLI [2.16.0](https://app-updates.agilebits.com/product_history/CLI2) or later.

To use the 1Password plugin with the TreasureData Toolbelt, you must first set up the toolbelt in your environment. This involves [creating a TreasureData account](https://www.treasuredata.com/), [obtaining an API key](https://docs.treasuredata.com/display/public/PD/Getting+Your+API+Keys), and installing the toolbelt. Once the toolbelt is set up, you can build and test the TreasureData plugin locally using the instructions provided in the documentation.

```
$ make treasuredata/validate
$ make treasuredata/build
```

To import your TreasureData credentials into 1Password, you must first initialize the plugin and test the importer using the config file located at `~/.td/td.conf`. The plugin will create an entry in 1Password that includes the user and api key fields. Once the credentials are saved in 1Password, you can use them to authenticate with TreasureData when running commands.

To ensure that the credentials are being properly stored and accessed at runtime, the provisioner included in the plugin will inject the `TD_API_KEY` environment variable when running TreasureData commands. This ensures that the toolbelt can refer to the necessary credential at runtime. To test the provisioner, run a td command and ensure that the credentials are being properly retrieved. This injection is opted out when we use the option such as `-c` or `-k` which precedes every other configuration.

Overall, the 1Password shell plugin update adds a new level of convenience and security to interacting with the TreasureData platform. With the plugin, users can easily store and access their credentials in 1Password, eliminating the need to store them in plain text or remember them.