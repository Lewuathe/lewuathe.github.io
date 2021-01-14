---
title: "POST API by Lambda with serverless framework"
layout: post
date: 2021-01-14 08:02:01 +0900
image: 'assets/img/posts/2021-01-14-post-api-by-lambda-with-serverless-framework/catch.jpg'
description:
tag: ['AWS', 'Serverless', 'Web', 'API']
blog: true
author: "Kai Sasaki"
---

[Serverless](https://aws.amazon.com/serverless/) is a kind of buzzword in recent years. It brings me a new concept of providing a web service without depending on the fixed amount of server machines (virtually), enabling us to build a more agile and flexible platform responding to changes faster.

[Serverless Framework](https://www.serverless.com/) is one of the most notable framework implementing the concept, "serverless". It supports a lot of major cloud service providers such as [AWS](https://aws.amazon.com/), [Azure](https://azure.microsoft.com/en-us/). We can launch a new web-based service with minimal code writing abruptly.

I have created a web API providing a POST endpoint with serverless backed by AWS Lambda and API Gateway. But I needed a little investigation to do so. Therefore, those who are facing the requirement to provide POST API with lambda will find this useful. Here is the guide I would want to have before starting to develop an API.

# serverless.yml

`serverless.yml` is a central place controlling all configuration of the infrastructure managed by the serverless application. It specifies the name of the provider, environment variables, and so on.

```yaml
service: myservice

plugins:
  # Necessary to purge previous version
  - serverless-prune-plugin
  # Install all dependencies specified by requirements.txt
  - serverless-python-requirements

provider:
  name: aws
  runtime: python3.7
  stage: ${opt:stage, 'development'}
  region: us-east-1
```

`custom` field provides variables that likely change depending on the environment the application runs.

```yaml
custom:
  stages:
    - development
    - production
  a_variable:
    development: variable_for_development
    production: variable_for_production
  pythonRequirements:
    dockerizePip: true
  prune:
    # Specify the number of retained previous versions
    automatic: true
    number: 10
```

# Function for POST

The function definition for the POST endpoint is easy to write.

```yaml
functions:
  post_endpoint:
    handler: handler.post_endpoint
    events:
      - http:
            path: myapp/post_endpoint
            method: post
    environment:
      # Set the stage specific variable
      A_VARIABLE: ${self:custom.a_variable.${self:provider.stage}}
```

Since the POST endpoint parses the HTTP request body, there is no need to specify the required parameters in the config.

# Handler Method

We can find the POST method in the handler code as follows.

```python
def post_endpoint(event, context):
    print("A POST endpoint")
    # Obtain the body in JSON format
    body = json.loads(event["body"])
```

We can extract any parameters from the body like `body['key']`. Note that the validation of the parameter is the responsibility of the handler. The required parameter for the app may be missing in the `body`. Please make sure to check the existence of the parameter beforehand.

```python
def get_or_none(key, body):
    if key in body:
        return body[key]
    else:
        return None

get_or_none('key', body)
```

Thanks!