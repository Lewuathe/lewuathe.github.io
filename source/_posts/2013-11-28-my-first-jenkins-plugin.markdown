---
layout: post
title: "My first Jenkins plugin"
date: 2013-11-28 21:15
comments: true
categories: ["Jenkins", "plugin", "Java", "Maven"]
author: Kai Sasaki
---

Released my first Jenkins plugin

https://github.com/jenkinsci/hckrnews-plugin

![Screen shot](/images/posts/2013-11-28-hckrnews-plugin/screen-shot.png)

With this plugin, you can read hacker news top time line sitting in front of CI server.
So you can read top topics about technology and so on at the same time building your project. Does it sound good?

## How to publish Jenkins plugin?

### Make GitHub repository

Normal Maven project needs only src/ and pom.xml. Jenkins plugin project is not exception. 
Write right .gitignore, and ignore target/ and work/ directory. These are not necessary.

### Create new jenkins-ci account

Visit [here](https://jenkins-ci.org/account/). Create your new account.

### Write settings.xml your account information

Your account name, and password got from above process should be written in `~/.m2/settings.xml` like below.

```
<settings>
 ・・・
  <servers>
    <server>
      <id>maven.jenkins-ci.org</id>
      <username>XXXXXX</username>
      <password>XXXXXX</password>
    </server>
  </servers>
  ・・・
</settings>
```

### Application for forking repository

Send an email to community [mailing list](https://groups.google.com/forum/#!forum/jenkinsci-ja) in Japan. If you want to send other community, search [here](http://jenkins-ci.org/content/mailing-lists)
Soon your repository is forked to original jenkinsci organization.

### Modify pom.xml

Add some line. SCM repository url should be written in your project `pom.xml`

```
<scm>
    <connection>scm:git:ssh://github.com/jenkinsci/XXXXXXXX.git</connection>
    <developerConnection>scm:git:ssh://git@github.com/jenkinsci/XXXXXXXX.git</developerConnection>
    <url>https://github.com/jenkinsci/XXXXXXXX.git</url>
</scm>
```

### Release!

Type below command.

```
$ mvn release:prepare release:perform
```

One this your should pay attention to is not to add `-Dusername` and `-Dpassword` options. These are not used for GitHub but jenkinsci.org
Congratulations!!

### Future

In fact, I make this plugin with no experience of writing Java, of course maven.
Therefore I have to study these tool and Java grammar. In addition to this, I learned how to write some design patterns with coding in accordance with OO programming. 

I also wrote some test codes with JUnit in maven. TDD is the method with which I want to develop. In this time, first I wrote unit test code and second logic code. This is fun for me because my code's quality seems to be kept easily. I want to keep writing test code first. This is the best practice for my developing.

This plugin has only simple functions, however, this experience is sufficient value as software engineer. 
In the future, I will seize the moment and make more my own plugins.

Ultimately, please use this plugin. It brings to you a new continuous integration life.

Thank you.
