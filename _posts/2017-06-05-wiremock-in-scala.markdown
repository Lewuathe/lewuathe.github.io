---
title: "WireMock in Scala"
layout: post
date: 2017-06-05 14:38:12 +0900
image: 'images/'
description:
tag: ["WireMock", "Scala", "ScalaTest"]
blog: true
author: "lewuathe"
---

Mock server which handles HTTP request is useful component for testing HTTP client library.
Since it emulates the handling logic of HTTP request artificially, we can verify our HTTP client without
relying external service.

If you write your application in Scala, I'll recommend to use WireMock for mock server. This is easy to use and
flexible. We are able to integrate it with [ScalaTest](http://www.scalatest.org/).

* [WireMock](http://wiremock.org/)

The usage is written [here](http://wiremock.org/docs/getting-started/). But it's the tutorial for Java.
I want to write the mock server code in Scala.


```scala
import org.scalatest.FlatSpec
import org.scalatest.BeforeAndAfterEach
import org.json4s.native.Serialization

class MyTest extends FlatSpec with BeforeAndAfterEach {
  private val port = 8080
  private val hostname = "localhost"
  // Run wiremock server on local machine with specified port.
  private val wireMockServer = new WireMockServer(wireMockConfig().port(port))

  override def beforeEach {
    wireMockServer.start()
  }

  override def afterEach {
    wireMockServer.stop()
  }

  val response = Map(
      "k1" -> "v1",
      "k2" -> "v2"
  )

  "Your Client" should {
    "send proper request" in {
      val path = s"/v1/some/api"
      // Configure mock server stub response
      // json4s is useful to constructing response string if the response is JSON
      wireMockServer.stubFor(
        get(urlPathEqualTo(path))
        .willReturn(aResponse()
        .withHeader("Content-Type", "application/json")
        .withBody(Serialization.write(response))
        .withStatus(200)))

      // Send request by using your HTTP client
      val ret = youClient.get()

      // Verify the request is valid
      wireMockServer.verify(
        getRequestedFor(urlPathEqualTo(path))
        .withHeader("Content-Type", "application/json"))
      }

      // Assert response body itself if necessary
    }
  }
}
```

That's all. WireMock provides `StringValuePattern` for filtering/matching HTTP request. (e.g. `equalTo`, `containing`)
By using the class, you can create stub/mock server flexibly.
