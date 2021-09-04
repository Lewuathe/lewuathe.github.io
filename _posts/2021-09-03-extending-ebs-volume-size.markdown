---
title: "Extending EBS volume size"
layout: post
date: 2021-09-03 21:06:00 +0900
image: 'assets/img/posts/2021-09-03-extending-ebs-volume-size/catch.jpg'
description:
tag: ['EBS', 'AWS']
blog: true
author: "Kai Sasaki"
---

If you maintain the long-running EC2 instance, you may have encountered the situation where you find the initial EBS storage volume insufficient. It may be caused by the log volume increasing rapidly than expected. Or you may put many resources in the instance manually.

Either way, we need to remove the unnecessary files or recreate the instance if possible. If it's not the case, the only way we can do this is to **extend the EBS volume**.

This article aims to convey how to increase the EBS volume size at runtime with no downtime of EC2 instances.

## Modify EBS volume

The first step is to modify the EBS volume attached to the target instance whose volume we want to increase. After selecting the volume, click the `Modify Volume` from the actions pane.

![Modify EBS](./assets/img/posts/2021-09-03-extending-ebs-volume-size/modify-ebs.png)

We can set an arbitrary number of volume sizes from there. But, unfortunately, it takes a while to complete the optimization. So let's wait for a few minutes.

![Increase EBS](./assets/img/posts/2021-09-03-extending-ebs-volume-size/increase.png)

But even after the optimization completion, the thing has not been done. We need to reconfigure the partition and file-system on the volume.

## Extending Linux File System

We must use the file-system specific command to extend the file system to a larger size. Although the command is dependent on the file system you use, we assume `ext4` here.

First, we check the name of the root file system on your instance.

```
$ df -hT
Filesystem      Type  Size  Used Avail Use% Mounted on
/dev/xvda1      ext4  8.0G  1.9G  6.2G  24% /
```

1.9G capacity is already occupied in `/dev/xvda1`. Now let's say we already increase the EBS volume size for this root device to 16G from 8G. The system does not correctly recognize the latest volume size.

It's necessary to extend the partition manually to let the system know the latest volume size. The `lsblk` command shows the partition information.

```
$ lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0  16G  0 disk
└─xvda1 202:1    0   8G  0 part /
```

The root volume `/dev/xvda` has 16G capacity, and one partition `/dev/xvda1` occupied 8G out of that. Therefore, we can increase the size of the partition by running the following command.

```
$ sudo growpart /dev/xvda 1
$ lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0  16G  0 disk
└─xvda1 202:1    0  16G  0 part /
```

We also need to extend the file system on that volume. `resize2fs` is available to extend the `ext4`.

```
$ sudo resize2fs /dev/xvda1
$ df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/xvda1        16G  1.9G  14G  12% /
```

Now we get all things done!

## Reference
- [Request modifications to your EBS volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/requesting-ebs-volume-modifications.html)
- [Extend a Linux file system after resizing a volume](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html)