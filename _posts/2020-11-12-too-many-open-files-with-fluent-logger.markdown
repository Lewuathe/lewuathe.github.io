---
title: "Too Many Open Files with fluent-logger"
layout: post
date: 2020-11-12 08:36:10 +0900
image: 'assets/img/posts/2020-11-12-too-many-open-files-with-fluent-logger/catch.jpg'
description:
tag: ['Fluentd', 'Ruby', 'Web', 'Rails']
blog: true
author: "Kai Sasaki"
---

We tend to use [fluentd](https://www.fluentd.org/) (td-agent) to keep the access log of the service persistently. Fluentd is one of the most reliable and flexible middleware to collect various kinds of application logging. We can quickly broaden the target of logging by using many types of plugins maintained by the community.

As is often the case with the middleware libraries, we have found unexpected behavior of fluentd due to our lack of full knowledge of the library. Our Rails application often loses the application log!

This article will illustrate why that problem happens and caveats when we use fluent-logger in Rails application.

# Problem

Our Rails application has a controller that collects its access log.

```ruby
require 'fluent-logger'

class OurController < ApplicationController
  before_action :setup_fluent_logger
  before_action :access_log

  def setup_fluent_logger
    @log = Fluent::Logger::FluentLogger.new(
      nil,
      host: 'localhost',
      port: 24_224
    )
  end

  def access_log
    record = ...
    @log.post("test.access", record)
  end
end
```

Initially, I thought recreating the fluent-logger instance whenever it gets access is safe to dump the log. But that's not true at the end of the day. This controller fails to post logs when it gets many accesses from clients.

# Cause

To detect the cause, I have tried to write a script to reproduce the issue.

```ruby
require 'singleton'
require 'fluent-logger'

class OurController
  include Singleton

  def initialize
    @counter = 0
    setup_logger
  end

  def setup_logger
    @logger = Fluent::Logger::FluentLogger.new(
      nil,
      host: 'localhost',
      port: 24_224
    )
  end

  def post(v)
    @logger.post('debug.test', {
        a: @counter,
        v: v
    })
    @counter += 1
  end
end


puts "Start..."

def post(i)
  controller = OurController.instance
  controller.setup_logger
  controller.post(i)
end

thread_num = 256

# Multi Thread
threads = (0..thread_num).map do |i|
  Thread.new {
    post(i)
  }
end

threads.each do |t|
  puts "Waiting for #{t}"
  t.join
end
```

When I ran the program with `thread_num = 256`, it fails to dump the log due to connection failure to the local td-agent, but it did not with `thread_num = 200`. There is an implicit threshold between 200 and 256, I thought. Here is what I have found.

```
➜ launchctl limit
  cpu         unlimited      unlimited
  filesize    unlimited      unlimited
  data        unlimited      unlimited
  stack       8388608        67104768
  core        0              unlimited
  rss         unlimited      unlimited
  memlock     unlimited      unlimited
  maxproc     2784           4176
  maxfiles    256            unlimited
```

It hit the max number of file descriptors in the system. The `Too many open files` error was thrown by td-agent around the time.

```
2020-11-11 12:06:17 +0900 [warn]: #0 [forward_input] thread exited by unexpected error plugin=Fluent::Plugin::ForwardInput title=:event_loop error_class=Errno::EMFILE error="Too many open files - accept(2)"
#<Thread:0x00007fea449aa020@event_loop@/Users/sasaki/.rbenv/versions/2.5.4/lib/ruby/gems/2.5.0/gems/fluentd-1.11.5/lib/fluent/plugin_helper/thread.rb:70 run> terminated with exception (report_on_exception is true):
...
/Users/sasaki/.rbenv/versions/2.5.4/lib/ruby/2.5.0/socket.rb:1313:in `__accept_nonblock': Too many open files - accept(2) (Errno::EMFILE)
```

Initializing the fluent-logger object opens a new file descriptor, which caused the `Too many open files` error. It looks like an event library [Cool.io](https://github.com/tarcieri/cool.io) [creates a file descriptor](https://github.com/fluent/fluentd/blob/master/lib/fluent/plugin_helper/event_loop.rb#L93) when it starts the event loop.

```ruby
def start
  super
  # event loop does not run here, so mutex lock is not required
  thread_create :event_loop do
    begin
      default_watcher = DefaultWatcher.new
      event_loop_attach(default_watcher)
      @_event_loop_running = true
      @_event_loop.run(@_event_loop_run_timeout) # this method blocks
    ensure
      @_event_loop_running = false
    end
  end
end
```

Since we cannot have any privilege to modify the Cool.io codebase quickly, what we can do to the maximum is avoiding the recreation of fluent-logger instance. In this case, the `setup_fluent_logger` method looks as follows. Note that we use `||=` to initialize `@log` instead of `=` assignment.

```ruby
class OurController < ApplicationController
  def setup_fluent_logger
    @log ||= Fluent::Logger::FluentLogger.new(
      nil,
      host: 'localhost',
      port: 24_224
    )
  end
end
```

In general, we cannot guarantee the order of the call of the method of `before_action`. We should have made `@log` thread-safe. I would stress that that problem does not devote to fluentd or Rails itself. Our practice of programming causes that. I have gotten another lesson here.