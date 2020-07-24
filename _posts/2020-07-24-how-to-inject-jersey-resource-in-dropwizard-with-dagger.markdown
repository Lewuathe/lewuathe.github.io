---
title: "How to inject Jersey Resource in Dropwizard with Dagger"
layout: post
date: 2020-07-24 21:36:03 +0900
image: 'assets/img/posts/2020-07-24-how-to-inject-jersey-resource-in-dropwizard-with-dagger/catch.jpg'
description:
tag: ['Web', 'Java', 'Dagger', 'Jersey']
blog: true
author: "Kai Sasaki"
---

Dependency Inject (DI) is one of the most notable practices to create reliable and high-quality software. This effort enables us to keep the extensibility without losing readability and testability. You may have encountered a situation where you would want to replace any objects in the software flexibly like me. Many frameworks or libraries are allowing us to make use of the dependency injection in our software project. In my case, I would like to use [Dagger](https://dagger.dev/) in our web application using [Dropwizard](https://www.dropwizard.io/). But I was ignorant of what Dagger was and how to use it in our Dropwizard project. Hence, this article is for writing down the process to get started with Dagger in your web application using Dropwizard.

## What is Dagger

First of all, what is Dagger? Dagger is a Java-based dependency injection library originally invented by [Square](https://squareup.com). For now, it's mainly maintained by Google as an open-source project.


![Dagger](/assets/img/posts/2020-07-24-how-to-inject-jersey-resource-in-dropwizard-with-dagger/dagger.png)

You might hear about [Guice](https://github.com/google/guice) before, which is also maintained by Google. It has a more extended history than Dagger. Despite that, Dagger has a more significant number of stars in [its GitHub repository](https://github.com/google/dagger). Why is Dagger more popular than Guice? There are several reasons from my perspective.

* Dagger is compiling time DI library, while Guice's injection happens at runtime
* Guice often causes challenging error to solve relating to its reflection usage
* Dagger provides more simple APIs to use
* Dagger has notable use cases due to the adoption in the Android development

Therefore, I try to use Dagger in our web application this time.

## How to integrate Dagger in Dropwizard project

What I'm going to do is integrate Dagger in a Dropwizard project to inject Jersey resources flexibly. Before going deeper into this goal, we need to be familiar with some Dagger terminologies.

* `Module`: Has associations between the interface and actual injected objects.
* `Component`: Constructs a whole graph resolving the dependencies of injected objects

Unlike Guice, what I've found is that we needed to construct one more class called `Component`. The component is a sort of highest level class managing all objects injected by Dagger. Therefore, all objects should be injected from the component.

In our case, we will create `WebResourceModule` for the module and `WebappComponent` for the component.

The client of the injected class can use the `javax.inject.Inject` annotation. Constructor injection or field injection is recommended in Dagger.

```java
@Path("/users")
class UserResource {
  @Inject
  public UserResource(UserConfig userConfig) {
    // Used for the user resource specific configuration
    this.config = config;
  }
}
```

We are going to inject `UserConfig` as we like by using Dagger.

The dagger library can be imported with the following code in `build.gradle`.

```gradle
dependencies {
  implementation 'com.google.dagger:dagger:2.28.1'
  annotationProcessor 'com.google.dagger:dagger-compiler:2.28.1'
}
```

## Module and Component

First, we define the module to illustrate how to construct the target `UserConfig` class.

```java
import dagger.Module;
import dagger.Provides;

@Module
public class WebResourceModule {
    private final UserConfig;

    public WebResourceModule(Configuration configuration) {
        this.userConfig = configuration.getUserConfig();
    }

    @Provides
    UserConfig provideUserConfig() {
      return this.userConfig;
    }
}
```

`@Provides` annotation lets the compiler know how to construct the class at the compile time. Therefore, all classes in the application use the `UserConfig` constructed by the method, `provideUserConfig`. Next, we can create a module class for building the whole dependency graph.

```java
import dagger.Component;

@Component(modules = {WebResourceModule.class})
public interface WebappComponent {
    UserResource getUserResource();
}
```

The argument of `@Component` annotation specifies the modules knowing how to construct the injected objects. All `WebappComponent` interface needs to provide is the method to build the object we finally want to get. In this case, the web resource which will be registered into the Dropwizard later. That's all that we must do with Dagger.

But here comes one question. Who creates the instance of `WebappComponent`? The answer is Dagger. Dagger generates a class prefixed by `Dagger`. In this case, `DaggerWebappComponent` will be created to construct the `UserResource` from it. Additionally, it provides us a way to bind a module at runtime.

## Dropwizard Application

In the Dropwizard, we will get the component class to get the `UserResource` and register it as a jersey resource.

```java
public class Application extends io.dropwizard.Application<Configuration> {

  public static void main(String[] args) throws Exception {
    new Application().run(args);
  }

  @Override
  public void run(@NotNull Configuration configuration, Environment environment) {
    // Bind the module to inject the user configuration
    // All objects dependent on the UserConfig can change the behavior without rewriting them.
    WebappComponent component = DaggerWebappComponent.builder()
                        .webResourceModule(
                                new WebResourceModule(configuration)
                        .build();

    environment.jersey().register(component.getUserResource();
  }
}
```

`DaggerWebappComponent` has a builder interface to bind the module at runtime. By changing the module here, we can change the behavior. For the test purpose, we can write a component like this.

```java
WebappComponent testComponent = DaggerWebappComponent.builder()
                    .webResourceModule(
                            new TestWebResourceModule(configuration)
                    .build();

UserResource testUserResource = testComponent.getUserResource();
```

It obviously helps us write more testable code.

## Wrap Up

As we saw now, using a Dagger looks easy. Dagger enabled me to write more maintainable code without learning many things. Its simple APIs significantly reduce the trouble and burden to employ the DI framework in our software projects. Let's try to use Dagger in your Dropwizard project as well!

