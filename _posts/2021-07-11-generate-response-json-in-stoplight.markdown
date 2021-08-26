---
title: "Generate JSON response in Stoplight"
layout: post
date: 2021-07-11 07:46:40 +0900
image: 'assets/img/posts/2021-07-11-generate-response-json-in-stoplight/catch.jpg'
description:
tag: ['Web', 'OpenAPI', 'HTTP']
blog: true
author: "Kai Sasaki"
---

Well-written documentation of a web API is an indispensable resource to learn its usage for users. It should be comprehensive and concise, covering all endpoints with supporting parameters and response format. [OpenAPI](https://www.openapis.org/) allows us to provide the documentation in a standard manner to use various tools to enhance documentation generation.

But it's still not fun. OpenAPI requires us to write response formats by hand, which is very time-consuming and error-prone. I need to use my brain and hand to document the correct YAML entry alongside looking at the actual response.

Today, I've found [Stoplight](https://stoplight.io/) provides an auto-generation functionality for the response model. Stoplight automatically generates valid YAML or JSON corresponding to the given response format. For example, let's say our endpoint will return the following JSON response in case of 200 status code.

```JSON
{
    "request_id": 1234,
    "users": [
        {"name": "Alice", "age": 12},
        {"name": "Bob", "age": 14}
    ]
}
```

It contains a unique ID for the request and user entries matching with the request query. Afterward, we can generate the model schema by just clicking the `Generate` button as follows.

![Auto Generate](/assets/img/posts/2021-07-11-generate-response-json-in-stoplight/auto-generate.png)

We see the model schema like this.

![Model](/assets/img/posts/2021-07-11-generate-response-json-in-stoplight/model.png)

The example value and type of each entry are also properly configured.

It's by far more agile and manageable to complete the model schema than putting each item one by one. I should have known this helpful functionality earlier. :)
