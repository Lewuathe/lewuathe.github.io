---
title: "Access Management of Elasticsearch Service with Python"
layout: post
date: 2019-09-10 20:30:30 +0900
image: 'assets/img/posts/2019-09-10-access-management-of-elasticsearch-service-with-python/catch.jpg'
description:
tag: ['IAM', 'AWS', 'Elasticsearch']
blog: true
author: "Kai Sasaki"
---

AWS provides a service to host the Elasticsearch. It is a fully managed service; thus, we do not need to take care of the detail of Elasticsearch by ourselves.
The easiness of launching the Elasticsearch cluster is not the only reason to use the service. It makes it much easier to manage the access policy by using the IAM based access management mechanism. IAM role is the underlying construct to do the access management and permission control in the AWS environment. Elasticsearch service is seamlessly integrated with the feature. Those of who already start using AWS should consider it the option when you want to create a full-text search feature in the service.

Here I'd like to explain how to configure IAM based access management with Elasticsearch service and show the code to access the cluster by using Python library.

# Launch Cluster

When you build the cluster with Elasticsearch service, you can select the template according to your requirement. To access the cluster, please make sure to select the `Public access`. `VPC access` makes the situation a little complicated.

![network-configuration](assets/img/posts/2019-09-10-access-management-of-elasticsearch-service-with-python/network-configuration.png)

![access-policy](assets/img/posts/2019-09-10-access-management-of-elasticsearch-service-with-python/access-policy.png)

Let's take the first template to allow the specific IAM role to access to our cluster. You will see the policy written in JSON as follows.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "<Your ARN>"
        ]
      },
      "Action": [
        "es:*"
      ],
      "Resource": "arn:aws:es:ap-northeast-1:XXXXXXXXX:domain/your-cluster-domain/*"
    }
  ]
}
```

It illustrates the policy which allows `<Your ARN>` to access the cluster for any APIs. Since you may want to access any endpoint to control the Elasticsearch cluster fully, the wildcard is used to specify the resource to be accessed. Okay, the cluster is prepared with this access policy configuration.

# Session Credential in Python library

The cluster can be accessed from anywhere as long as you have the correct IAM credential. You can use **boto3** to get the proper credential for Python.
(BTW, I found the name of `boto` derived from [Dolphin living in Amazon](https://github.com/boto/boto3/issues/1023). Interesting :))

```
$ pip install boto3
```

Elasticsearch service launched the cluster with HTTPS connection as default. It is necessary to set up the client accordingly.

```python
host = 'XXXXXXXXXX'
credentials = Session().get_credentials()
aws_auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    "ap-northeast-1",
    "es",
    session_token=credentials.token,
)

client = Elasticsearch(
            hosts=[{"host": host, "port": 443}],
            use_ssl=True,
            verify_certs=True,
            http_auth=aws_auth,
            connection_class=RequestsHttpConnection,
        )

client.cluster.health()
```

Of course, the IAM role set in the environment must be the one you allowed previously. Now you should be able to access the cluster safely.

Thanks.


Image by <a href="https://pixabay.com/users/qimono-1962238/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2114046">Arek Socha</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2114046">Pixabay</a>