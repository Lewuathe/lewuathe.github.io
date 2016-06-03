---
layout: post
title: "Deleting unused files in Chef cookbook"
date: 2016-06-03 23:28:13 +0900
comments: true
categories: ["Chef"]
author: Kai Sasaki
---

When you use Chef cookbook, a lot of files might be installed in you machine, configuration, script and so on.
Chef provides very useful resource for putting a file called `template`. You can put any type of text file with this resource.

[Template Resource](https://docs.chef.io/templates.html)

But `template` does not manage a file when it is unused. How can we delete a file once installed?
Since there is no way provided by Chef, we have to implement. So here I want to introduce a small pattern to achieve
this purpose here. The problem we want to solve here is this.

* We have a dynamic list of files to be installed
* We have to change the list anytime even some of them are deleted
* Deleted files from the list must be also deleted from the machine

<!-- more -->

We can assume the case that the list is kept by data_bags or consul. Chef `template` cannot handle this type of dynamic
list flexibly itself. So this is what I've written to achieve this.

```ruby
def installed_config_files
  begin
    Dir.glob("/path/to/*.conf")
  rescue
    return []
  end
end
```

This is defined in libraries or somewhere. `installed_config_files` is used in each recipe.

```ruby
installed_config_files.each do |conf|
  # Check the installed file should be kept or not
  if !config_files.include?(conf) then
    file conf do
      action :delete
    end
  end
end

config_files.each do |conf|
  template conf do
    source somewhere
    action :create
  end
end
```

With this snippet, you can make sure only the filed defined `config_files` are installed in the target machine.
Chef provides great power to our non-operation intensive engineers. I realized again that I can do operations which can be
repeatable, persistent and writable. I want to be more familiar with Chef usage further.

Thank you.
