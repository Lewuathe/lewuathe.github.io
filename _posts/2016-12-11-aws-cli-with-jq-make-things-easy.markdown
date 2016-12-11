---
title: "AWS CLI with jq make things easy"
layout: post
date: 2016-12-11 10:29:45 +0900
image: 'images/'
description:
tag: ['AWS', 'jq']
blog: true
jemoji:
author: "lewuathe"
---

AWS CLI is a utility for manipulating your infrastructure on AWS. It enables us to launch EC2 or check instances 
without leaving out your command line. But it is not easy to use because the output is JSON as default. Though JSON is a format
which is useful for machine and also human, it is not suitable as an output of command line tools. Let me see.

```
{
    "Reservations": [
        {
            "OwnerId": "12345678",
            "ReservationId": "r-12345678",
            "Groups": [],
            "Instances": [
              {
                "PublicDnsName": 
                ...
              }
            ],

        }
    ],
    ...
}
```

Hmm, I cannot grasp how many instaces are launched or check the instances which is running now. Even redirecting the format to 
ordinal UNIX command, we cannot solve the situation. UNIX command is good at manipulating the data per **line** not JSON.

But I found a good tool for manipulating JSON from command line. [JQ](https://stedolan.github.io/jq/). JQ enables us to 
filter, map and count etc agaist JSON data. For example 

```
$ cat sample.json
{
    "id": "123456",
    "name": "Kai Sasaki",
    "address": "Tokyo",
    "language": [
        "Japanese",
        "English",
        "Java"
    ]
}
```

You can filter "id" with

```sh
$ cat sample.json | jq '.id'
"123456"
```

Count the number of language

```sh
$ cat sample.json | jq '.language | length'
3
```


So you can filter and map the running instance IDs which is tagged as web api server to csv like this.


```sh
$ aws ec2 describe-instances \
  --filter 'Name=tag:Name,Values=api' 'Name=instance-state-name,Values=running' | \
  jq -r '.Reservations[].Instances[] | [.InstanceId, .PrivateIpAddress, .Tags[].Value] | @csv'
```

After converted csv or line based data, you can use UNIX command line tools as you like for checking statistics.
Since JQ has a lot of useful options and functionalities, I want to be familiar with tool more.
Please check [the official documentation](https://stedolan.github.io/jq/) for more detail.

Thanks.
