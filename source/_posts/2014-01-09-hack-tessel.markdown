---
layout: post
title: "Hack Tessel!"
date: 2014-01-09 21:25
comments: true
categories: ["Tessel","node"]
author: Kai Sasaki
---
<meta property=”og:image” content=”http://lewuathe.com/images/posts/2014-01-09-tessel-first/bootstrap_tessel.jpg” />


Yesterday, I got a [tessel](http://tessel.io/). With twists and turns, I overcome some obstacles for hacking this tiny but not little possibility board. So writing this post.

First and unfortunately, these client modules are only used for beta testers now. 
So these are not opend yet. Please be understanding of this point.

## Environment

* MacOSX 10.9.1
* git 1.8.3.4 (Apple Git-47) 
* java 1.7.0_45
* node v0.10.16 (with nvm)

## Install drivers for OSX

```
$ brew install libusb
$ brew install pkg-config
```

In order to connect tessel with USB, these drivers are needed.
After installing the drivers, you can use `tessel` command. This command is used for 
connecting tessel server or pushing your codes, etc. So your development cycle of tessel
will be work around this command. It's very important.

```
$ tessel
Tessel CLI
Usage:
   tessel <filename>
   tessel list
   tessel logs
   tessel push <filename> [-r <ip[:port>]] [-s] [-b <file>] [-a [options]]
          -r wireless pushing of code (inactive at the moment)
          -s saves the file that is getting passed to Tessel as builtin.tar.gz
          -b pushes a binary
          -a passes arguments to tessel scripts
   tessel wifi <ssid> <pass> <security (wep/wap/wap2, wap2 by default)>
   tessel wifi <ssid>
          connects to a wifi network without a password
   tessel wifi
          see current wifi status
   tessel stop
   tessel dfu-restore <firmware.bin>
          upload new firmware when in DFU mode

```

## Connecting

After installing these prerequisites, you can connect tessel to your PC with USB cable.
For confirming the connection between tessel and my MAC, `verbose` subcommand is useful.

```
% tessel verbose
TESSEL? No Tessel found, waiting...
```

Umm?. I cannot connect. No matter how long I wait, there are no sign of connecting.
So here is answer.

![Boostrap](/images/posts/2014-01-09-tessel-first/bootstrap_tessel.jpg)

I have to wait for the LED lamps off. I cannot understand why these waiting is necessary now, but anyway after the LEDs are off, I can connect to the tessel board. Great!


```
% tessel verbose
TESSEL! Connected to /dev/cu.usbmodem1421.
H { date: 'Jan  3 2014', time: '17:50:43' }
l Tessel, by Technical Machine <http://technical.io>
l Firmware version: e1b13fc
l Runtime version: 7d86665
l Build time: Jan  3 2014 17:50:43
l Board version: 2
l Board serial: 428-0-4026571312-1578983944
d
l Run 'tessel push <path to code>' from the command line to push code.
w Connecting to last available network...
w CC3000 firmware version: 1.24
W { cc3000firmware: '1.24' }
w CC3000 firmware version: 1.24
W { cc3000firmware: '1.24' }
w Couldn't connect to saved network.
w
W { connected: 0, ip: null }
L 1
d Ready.
```

## Demo

Tessel has LED lamps as default. So I run sample code which can blink these LED.
It's below.

```
var tessel = require('tessel');

// high means flashing
var led1 = tessel.led(1).output().high();
// low means going off
var led2 = tessel.led(2).output().low();

var i = 0;
setInterval(function () {
  console.log(i++);
  // Switching on and off this function
  led1.toggle();
  led2.toggle();
}, 100);
```

And pushing it.

```
$ tessel push index.js
```

<iframe width="420" height="315" src="//www.youtube.com/embed/aKLGnU9wsTo" frameborder="0" allowfullscreen></iframe>

**BLINK!!!**

## More module

There are many [modules](http://tessel.io/modules) with tessel. For humidity, SDCard, Wifi, GPS, Serve etc.
So I want to try these modules more, and expand the possibility of embedded JavaScript.

