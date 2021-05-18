---
title: "Easy API Response with Jb"
layout: post
date: 2021-05-18 15:00:07 +0900
image: 'assets/img/posts/2021-05-18-easy-api-response-with-jb/catch.jpg'
description:
tag: ['Ruby', 'Rails', 'API']
blog: true
author: "Kai Sasaki"
---

A well-structured web application codebase is extensible and maintainable. [MVC framework](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) is a software design pattern allowing us to achieve that goal. The framework decouples the component for interface, internal business logic, and data persistence layer so that we can easily modify each of them without affecting other building blocks.

We can say the same thing for the REST API application as well. While that type of application does not have a clear view presented to users, separating the logic to construct the API response from the internal business logic is still critical to develop the extensible and scalable web application.

This time, I found [**jb**](https://github.com/amatsuda/jb) is helpful for that purpose. It is a simple Ruby library, and we can quickly get it integrated with your Rails application. The library proved to be neat and handy in my own Rails application. If you want to get the sorted architecture for the Rails REST API application, jb should be your help.

# How to use [jb](https://github.com/amatsuda/jb)

The fun will start by putting the template file in the view directory with the extension `*.jb`.

```ruby
jp_users = if @users.jp.present?
               @users.jp.map do |r|
                 {
                   'region' => 'jp',
                   'first_name' => r.first_name,
                   'last_name' => r.last_name
                 }.compact
               end
             else
               []
             end
us_users = if @users.us.present?
               @users.us.uniq(:id).map do |r|
                 {
                   'region' => 'us',
                   'first_name' => r.first_name,
                   'last_name' => r.last_name,
                   'middle_name' => r.middle_name.present? ? 'N/A' : r.middle_name
                 }.compact
               end
             else
               []
             end

{
  'users' => jp_users + us_users
}
```

In the corresponding controller, all we need to do is retrieving users.

```ruby
def users
  @users = Users.all

  if exceed_max_screening_result(@users)
    render json: { 'message': 'Too many users' }, status: :bad_request
  else
    render formats: :json, status: :ok
  end
end
```

It renders the following response.

```json
{
  "users": [
    {
      "region": "jp",
      "first_name": "Kai",
      "last_name": "Sasaki"
    },
    {
      "region": "us",
      "first_name": "Joe",
      "last_name": "Biden",
      "middle_name": "Robinette"
    }
  ]
}
```

In the template file, we can use ActiveModels or modules available in the Rails application and the helper method used typically for rendering the view. As you have seen, We can encapsulate all complexities involving the response construction in the template file. That is a great advantage using jb as an API response builder.