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

[AWS CLI](https://aws.amazon.com/cli/) is a utility for manipulating your infrastructure on AWS. For example, it enables us to launch EC2 or check the state of the instances without leaving out your command line. But it is not easy to use it because the output is JSON as default. Though JSON is a format which is useful for the machine and also human, it is not good input for some command line tools. Let me take a look into an example.

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

Hmm, I cannot grasp how many instances are launched or check the instances which are running now at a glance. Even redirecting the format to ordinal UNIX command, we cannot solve the situation. UNIX command is good at manipulating or traversing the data per **line** not JSON.

But I found a good tool for manipulating JSON from the command line. [**JQ**](https://stedolan.github.io/jq/). JQ enables us to filter, map and count and so on against JSON data. For example 

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

Count the number of languages

```sh
$ cat sample.json | jq '.language | length'
3
```


So you can filter and map the running instance IDs which is tagged as web API server to csv like this.


```sh
$ aws ec2 describe-instances \
  --filter 'Name=tag:Name,Values=api' 'Name=instance-state-name,Values=running' | \
  jq -r '.Reservations[].Instances[] | [.InstanceId, .PrivateIpAddress, .Tags[].Value] | @csv'
```

After it's converted into csv or line based data, you can use UNIX command line tools as you like for checking statistics as usual.
Since JQ has a lot of useful options and functionalities, I want to be familiar with the tool more.
Please check [the official documentation](https://stedolan.github.io/jq/) for more detail.

Thanks.
