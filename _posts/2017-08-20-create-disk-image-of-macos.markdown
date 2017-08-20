---
title: "Create disk image of macOS"
layout: post
date: 2017-08-20 08:52:43 +0900
image: 'images/'
description:
tag: ["macOS"]
blog: true
author: "lewuathe"
---

I had several times to install Linux (Ubuntu) on my laptop. The other day, I tried to install Ubuntu on my [Mac Book](https://www.apple.com/macbook/) because that's the only free laptop I had.

But I failed to create proper partition in that internal SSD and deleted macOS accidentally. So I had to re-install macOS from nothing. That means I cannot obtain even the help of recovery mode. I had to create installer media of macOS and re-install from that device. But how can I do that?

Apple provides me the detailed instruction [here](https://support.apple.com/en-us/HT201372). This instruction requires you to prepare another macOS machine. If you have at least two macOS machines, you can recover.

# Create install media

macOS installer already provides the utility to create installer media. If you don't have installer, please download the one from App Store first.

After you downloaded, the utility is stored here in case of Sierra.

```
/Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia
```

Please insert your USB flash memory device (or CD if you have) and run the command.

```
$ sudo /Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia \
    --volume /Volumes/YourUSBVolume \
    --applicationpath /Applications/Install\ macOS\ Sierra.app
```

You need to take care of the target volume to be written. Please confirm the name `/Volumes/YourUSBVolume` specifies your USB device name.
This utility will take several minutes.

If your USB device is used for other cases, it is necessary to format the device first. You can do that by using *Disk Utility*.

![Disk util](images/posts/2017-08-20-create-disk-image-of-macos/disk_util.png)

# Install

After you completed to create installer media, you just need to install. Please insert that installer media device into your target machine. Then restart the machine keep pressing *Option* key. The dialog that asks you to select the boot device from which you machine launches.

That'all! Please proceed the process according to the wizard!


# Reference

* [Create a bootable installer for macOS](https://support.apple.com/en-us/HT201372)
