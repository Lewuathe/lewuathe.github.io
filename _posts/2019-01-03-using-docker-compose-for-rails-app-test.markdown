---
title: "Using docker-compose for Rails app test"
layout: post
date: 2019-01-03 22:29:13 +0900
image: 'assets/img/posts/2019-01-03-using-docker-compose-for-rails-app-test/catch.jpg'
description:
tag: ["Docker", "Rails", "Ruby", "Test", "Software"]
blog: true
author: "lewuathe"
---

[BuffettCode](https://www.buffett-code.com/) that is one of my hobby projects is built by Ruby on Rails (RoR). 
Ruby on Rails is so useful that we can accelerate prototyping the initial work quickly. Though it was the first time for me to use RoR in a service used by other people, I am still confident that it's not wrong to choose RoR as our web application framework.

But we have found one problem after a while. Testing. I do not mean a unit test. We had several times when we want to run RoR application server in our local machine and check everything running correctly including DB schema and migration. It's a kind of thing existing between a unit test and integration test. We found [docker-compose](https://docs.docker.com/compose/) a suitable tool for stuff like that. This is the article to make testing of RoR easy by using docker-compose. 

# Table Of Contents

1. Database in local machine
2. Running RoR app with docker-compose
3. Tips?
   - Environment Variables
   - Online Modification
4. Recap

# Database in local machine

The first and biggest problem we need to solve is a database. Running database in the local machine is not easy as we expected because it highly depends on the machine you use. You may want to use PostgreSQL preinstalled in your macOS or you may want to use the latest one installed via Homebrew. That kind of thing may affect the application behavior and cause the problem when your app will run in the machine that belongs to other members. We want to make sure all members use the same database system when they check the correctness of the application. 

That leads the fact we need to create and run a Docker container for a database system which is PostgreSQL in our case as well as Rails app. Fortunately, the lightweight PostgreSQL docker image ([postgres:10.4-alpine](https://hub.docker.com/_/postgres)) is available so that we can create a whole set of application.

# Running Rails app with docker-compose

docker-compose is a simple tool to orchestrate multiple Docker containers. That enables us to write some dependencies between containers. We can define containers as services in docker-compose. Services in docker-compose can be defined in a file called `docker-compose.yml`.
Our docker-compose service of Rails app along with PostgreSQL can be defined as follows.

```
version: '3'

services:
  rail:
    build: ./
    volumes:
      - .:/rails-app
    env_file:
      - .env
    ports:
      - "3000:3000"
    restart: "no"
    links:
      - postgres
    command: bundle exec rails s
  postgres:
    image: postgres:10.4-alpine
    volumes:
      - db:/var/lib/postgresql/data
    env_file:
      - .env
    ports:
      - "5432:5432"
    restart: "no"
```

We defined two services named `rails` and `postgres`. The important part here is `links` directive. `links` gives docker-compose the information about dependencies between services. `rails` service depends on `postgres` service in this case so docker-compose will try to launch `postgres` service first. We need to write initial command to run the rails server in `rails` service. Then you can access your rails application through localhost:3000.

# Tips

You may need to pass some configuration to rails application in a docker container. (e.g. rails environment, credentials) It's possible to pass this information as an environment variable.  `env_file` specifies the file name contains environment variables supposed to be passed to Docker container. 

```
RAILS_ENV=development
DATABASE_URL=postgres://postgres:password@postgres:5432
PG_USER=postgres
PG_PASS=password
```

The good thing using environment variables to pass the custom configurations is that we can easily change the configuration. Famous CI services such as CircleCI, TravisCI supports custom environment variables. All we need to do is just copying and pasting `.env` file. 
We do not need to modify code when we start running CI. 

There is another thing we take care of. Since docker-compose is used for testing, we want to make the cycle of check and modify shorter. It's desirable the docker container is updated if we update the code base. It's possible by using volume mounted on the host machine.

```
services:
  rail:
  ...
    volumes:
      - .:/rails-app
  ...
```

This description mounts the current directory in host machine to `/rails-app` in a docker container. The code visible from docker container is exactly same to the one in the host machine. So as far as rails server supports live reloading, you will see the latest application even in a docker container. That does not cause the disadvantage introduced by using docker container. 

# Recap

So overall using docker-compose bring us significant benefit in terms of the test of Rails application. Since we have multiple Rails applications in our system, we test these applications in this common pattern. Please try this test pattern if you are using Rails application in your system.

Thank you!