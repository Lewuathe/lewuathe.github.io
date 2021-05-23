---
title: "Essential ways to make your Rails faster"
layout: post
date: 2021-05-23 08:10:56 +0900
image: 'assets/img/posts/2021-05-23-ways-to-make-your-rails-faster/catch.jpg'
description:
tag: ['Rails', 'Web']
blog: true
author: "Kai Sasaki"
---

There is no reason to keep the application slow. If we have room to improve the performance of our application without any drawback, we should do. It makes our users happier, and your application becomes attractive and prevents people from leaving for alternatives due to the performance issue.

But what should we do? Ideally, we should carefully measure the profile of the application runtime and detect the bottleneck to be improved. [As Donald Knuth said](https://stackify.com/premature-optimization-evil/#:~:text=What%20is%20premature%20optimization%3F,is%20credited%20to%20Donald%20Knuth.), the premature optimization is the root of all evil. We must not do any optimization blindly. That is the fundamental principle.

But I understand the situation; we may want to quickly know the essential tips to apply to every kind of web application. That is the general method simply applicable regardless of the type of application. This is the list of a few tips every Rails developer should know to keep your application performant. Please keep them in your mind every time your write your Rails application.

# Data Schema

Before we begin the journey, let's define our database schema first as our example.

```sql
CREATE TABLE `states` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cities` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `state_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_cities_on_state_id` (`state_id`),
  CONSTRAINT `fk_rails_cc74ecd368` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `offices` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `city_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `zip_code` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_offices_on_city_id` (`city_id`),
  CONSTRAINT `fk_rails_52308f6f48` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Our company has several offices across states in the country. An office locates in a city in a state. Hence we have associates between `offices` and `cities`, `cities` and `states`. Let's consider the case we want to generates the list of all office entities with the city and state name where it locates.

# Avoid N+1 Query

We can naively do so as follows.

```ruby
Office.all.each do |office|
  puts office.city.name
end
```

This code exactly does we want. But it's slow because it issues redundant queries to the backend database system. `Offices.all` get the list of all office entities by running 1 SQL. Let's say we get 100 offices here. Unfortunately, 100 queries to get each city entity follows. In total, we need to run 100 + 1 queries. If we put a code like `office.city.state.name`, the number exponentially grows, as you can imagine. That's a problem with the N+1 query.

But no worries, we have a quick way to fix that. `include`


```ruby
Office.include(:city).all.each do |office|
  puts office.city.name
end
```

This code issues a query to get all city entities associated with the office, not iterating one by one. That means we only run 1+1 queries even as a whole.

```sql
SELECT cities.* FROM cities
  WHERE (cities.id IN (1,2,3,4,5,6,7,8,9,10))
```

# Use pluck (and join)

Another performance problem likely to occur is the slowdown due to fetching many columns. If we have an entity having many attributes, getting these columns is time-consuming, and instantiation of [`ActiveRecord`](https://guides.rubyonrails.org/active_record_basics.html) matters. We can want to pick up only the specific columns without instantiating ActiveRecord for every record when we only print the result (e.g., generate CSV).

[`pluck`](https://apidock.com/rails/ActiveRecord/Calculations/pluck) enables us to issue a SQL fetching only specified columns from the underlying table. We can avoid `SELECT *` like query in short. We also need to use `join` instead of `include` to specify the column in the external tables (i.e., `cities`). The following code only issues 1 query to join every necessary table with the selected columns. It's a pretty bare minimum query to accomplish what we want.

```ruby
columns = [
  'offices.name',
  'cities.name'
]
Office.joins(:city).pluck(*columns).each do |office|
  puts office.city.name
end
```

# References

- [What is the N+1 query problem?](https://dev.to/junko911/rails-n-1-queries-and-eager-loading-10eh#:~:text=What%20is%20the%20N%2B1,the%20result%20of%20that%20data.)
- [Why Premature Optimization Is the Root of All Evil?](https://stackify.com/premature-optimization-evil/#:~:text=What%20is%20premature%20optimization%3F,is%20credited%20to%20Donald%20Knuth.)
- [ActiveRecord#include](https://api.rubyonrails.org/v6.1.3.2/classes/ActiveRecord/QueryMethods.html#method-i-includes)
- [ActiveRecord#joins](https://api.rubyonrails.org/v6.1.3.2/classes/ActiveRecord/QueryMethods.html#method-i-joins)