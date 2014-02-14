---
layout: post
title: "Making Jenkins widget plugin"
date: 2013-12-13 21:14
comments: true
categories: ["Jenkins", "Widget", "plugin"]
author: Kai Sasaki
---

This article was written for [Jenkins Advent Calendar](http://qiita.com/advent-calendar/2013/jenkinsci) 14th day.

## Making Jenkins plugin

Have you ever made Jenkins plugin? This is about my experience developing Jenkins plugin.
I have not written Java ever, and of course didn't know how to make maven projects. So while writing plugin codes, 
I went this way and that, googling and trying code snippets. Then I felt that there were not enough documents for 
first Jenkins plugin developers. This post however I only made widget plugin, I would be glad that this article will be useful
to the same developers as me.

## Getting started

First, it is needed to download skelton of Jenkins plugin by using maven plugin. I used maven-3.0.5, and OSX machine.
Write below xml in `~/.m2/settings.xml`

```
<settings>
  <pluginGroups>
    <pluginGroup>org.jenkins-ci.tools</pluginGroup>
  </pluginGroups>

  <profiles>
    <!-- Give access to Jenkins plugins -->
    <profile>
      <id>jenkins</id>
      <activation>
        <activeByDefault>true</activeByDefault> <!-- change this to false, if you don't like to have it on per default -->
      </activation>
      <repositories>
        <repository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </pluginRepository>
      </pluginRepositories>
    </profile>
  </profiles>
  <mirrors>
    <mirror>
      <id>repo.jenkins-ci.org</id>
      <url>http://repo.jenkins-ci.org/public/</url>
      <mirrorOf>m.g.o-public</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

Create skelton.

```
$ mvn hpi:create
```

Project name and artifactId will be asked as below.

```
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Building Maven Stub Project (No POM) 1
[INFO] ------------------------------------------------------------------------
[INFO]
[INFO] --- maven-hpi-plugin:1.106:create (default-cli) @ standalone-pom ---
Enter the groupId of your plugin [org.jenkins-ci.plugins]: com.lewuathe.plugins
Enter the artifactId of your plugin (normally without '-plugin' suffix): mytest
```

Then under current directory, `mytest` project might be made. The directory tree looks like.

```
% tree mytest
mytest
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── lewuathe
        │           └── plugins
        │               └── mytest
        │                   └── HelloWorldBuilder.java
        └── resources
            ├── com
            │   └── lewuathe
            │       └── plugins
            │           └── mytest
            │               └── HelloWorldBuilder
            │                   ├── config.jelly
            │                   ├── global.jelly
            │                   ├── help-name.html
            │                   └── help-useFrench.html
            └── index.jelly

13 directories, 7 files
```

This sample project uses Builder extension point of Jenkins plugin. [Builder extension](https://wiki.jenkins-ci.org/display/JENKINS/Extension+points#Extensionpoints-hudson.tasks.Builder) point is executed inside of the build process. If you have any process run on the way of building, you have to write the class which extends Builder. But in this article, I introduce Widget plugin. If you want to know what kind of extension points exist, please search on [this page](https://wiki.jenkins-ci.org/display/JENKINS/Extension+points)

Before explaining about Widget plugin, let me say how to run this plugins.

```
$ mvn hpi:run
```

With above command, maven can download packages on which this plugin project depends and run Jenkins test server on 8080 port.

```
# Access below host!
http://localhost:8080/jenkins/
```

You can look at Jenkins server! There is all you have to do before developing your own Jenkins plugin. Let's get started.

## Write Widget plugin

My Jenkins plugin is put on [this repository](https://github.com/jenkinsci/hckrnews-plugin). With this plugin you can see hacker news top time-line on Jenkins dashboard.
From [there](https://wiki.jenkins-ci.org/display/JENKINS/Hckrnews+Plugin), it can be downloaded.
Screen shot was taken as below.

![screenshot](/images/posts/2013-12-13-jenkins-widget-plugin/hckrnews-screenshot.png)

By examing this plugin's source code, I want to list up the points I had trouble in completing this plugin.

## Correspondence of Jelly file and Java class

In Jenkins, [Stapler](http://stapler.kohsuke.org/what-is.html) is used in order to map URL and Java objects.

> Stapler is a library that "staples" your application objects to URLs, making it easier to write web applications. The core idea of Stapler is to automatically assign URLs for your objects, creating an intuitive URL hierarchy.

At first, I cannot grasp what that means and practically which objects are mapped to jelly files. In conclusion, this is the correspond directory files.
Please look at `src/main/java` and `src/main/resources` directory of your project. It looks the same structure, doesn't it? So, in these directory, the correnspondence between Java class and jelly filesis made.
For example on hckrnews-plugin source tree, `java/com/lewuathe/plugins/hckrnews/HckrnewsWidget.java` corresponds to `com/lewuathe/plugins/hckrnews/HckrnewsWidget/`. 
The former is what model or controller, and the latter is view in the context of MVC.

```
├── java
│   └── com
│       └── lewuathe
│           └── plugins
│               └── hckrnews
│                   └── HckrnewsWidget.java  // <-- This is controller
└── resources
    ├── com
    │   └── lewuathe
    │       └── plugins
    │           └── hckrnews
    │               └── HckrnewsWidget
    │                   └── index.jelly     // <-- This is view which corresponds to above controller, HckrnewsWidget.java
    └── index.jelly
```

## Calling view method

In `HckrnewsWidget.java`, news static class in child class of Widget extension points is written.

```java
@Extension
public class HckrnewsWidget extends Widget {
// ....
    public static class News {
        private String title;
        private String url;
        private String points;
        private String postedBy;

        public String getTitle() { return this.title; }
        public String getUrl() { return this.url; }
        public String getPoints() { return this.points; }
        public String getPostedBy() { return this.postedBy; }
    }
// ....
}
```

Ordinary getter of News object. So it comes to index.jelly file. 

```
<j:jelly xmlns:j="jelly:core" xmlns:st="jelly:stapler" xmlns:d="jelly:define" xmlns:l="/lib/layout" xmlns:t="/lib/hudson" xmlns:f="/lib/form" xmlns:i="jelly:fmt">
<l:pane width="3" title="Hacker News Top">
<tr>
  <th class="pane">Title</th>
  <th class="pane">Points</th>
  <th class="pane">Posted by</th>
</tr>
<j:forEach var="news" items="${it.newslist}">
  <tr>
    <td align="left" class="pane" style="width:10px;"><a href="${news.url}">${news.title}</a></td>
    <td class="pane" align="right">${news.points}</td>
    <td class="pane" align="right">${news.postedBy}</td>
  </tr>
</j:forEach>
</l:pane>
Last Updated: ${it.lastupdatedstr}
</j:jelly>
```

The detail of Jelly syntax is not explained in this time. In this template file, `it` refers to the correspondence object in logic of stapler, 
in other words that's `HckrnewsWidget.java`. So when you writes as `it.newslist`, this calls 

```java
@Extension
public class HckrnewsWidget extends Widget {
//...
    public List<News> getNewslist() {
            return this.newsList;
    }
//...
}
```

Then `index.jelly` can get newslist. But you should take care of the casing of method name. If you write `getNewsList`, it can be called. Types are below.

* getNewslist : it.newslist is called
* getNewsList : it.newList is called
* getNewslist : it.newsList is *not* called

So it looks like auto casting to a captal letter is only applied to the first letter. It is necessary to arrange the type of posteror letters.

## Making Wiki

It might be rare case which only I experienced. Jenkins wiki page can not be created automatically.
Of course, it is taken for granted that writing down your wiki url on pom.xml.

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
//...
  <url>http://wiki.jenkins-ci.org/display/JENKINS/Hckrnews+Plugin</url>
//...
</project>
```

But this is not the trigger of creating Jenkins wiki page :( You have to make your own page yourself. 
I misunderstood about making wiki pages on this point. After you make your own wiki page, let's add a tag.

![add-tag](/images/posts/2013-12-13-jenkins-widget-plugin/add-tag.png)

After you add tag, your wiki page will be listed on [this page](https://wiki.jenkins-ci.org/display/JENKINS/Plugins). It will be easier to search for users.

# After all

This experience taught me many things about plugin development, Jenkins extension points and of course **Java** !!
Conversly if you have no experience of Java, you can also make your own Jenkins plugin about two weeks. 
And I want to keep making Jenkins plugins when idea comes to me. 

Last but not least, write your test codes in your plugin. With maven, you can run JUnit very easily.
If there are no test codes in the plugin of continuous integration tool, Jenkins, it sounds like mistaking the means for the end, doesn't it?

Viva great continuous integration! Thank you.
