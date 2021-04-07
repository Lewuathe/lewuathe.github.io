---
title: "When to use describe/context/it in RSpec"
layout: post
date: 2021-04-07 13:52:35 +0900
image: 'assets/img/posts/2021-04-07-when-to-use-describe-context-it-in-rspec/catch.jpg'
description:
tag: ['Rails', 'Ruby', 'RSpec', 'Test']
blog: true
author: "Kai Sasaki"
---

The well-structured test suite helps check the necessary cases are covered at a glance. Developers looking into the code, later on, can quickly grasp which case they should add or modify. The famous unit testing framework provides us a way to organize the test cases in that manner.

[RSpec](https://rspec.info/) is a de facto standard testing framework used in many Ruby projects. Although I have used RSpec in some projects, I did not fully understand how to `describe`, `context`, and `it` keyword correctly. These keywords are used just for representing the meaningless nested structure in my case. But that does not sound nice. Using these keywords properly leads us to inject an understandable form to the unit test written in RSpec. This article summarizes what we should think in writing RSpec test cases in terms of `describe`, `context`, and `it` use.

# `describe`: Target Object

Let's assume we have the following `FizzBuzz` class to be tested.

```ruby
class FizzBuzz
  def self.run(n)
    if n % 3 == 0 && n % 5 == 0
      "FizzBuzz"
    elsif n % 3 == 0
      "Fizz"
    elsif n % 5 == 0
      "Buzz"
    else
      n
    end
  end
end
```

We want to ensure that FizzBuzz works as expected with RSpec. The target object is an instance of FizzBuzz.

```ruby
describe FizzBuzz do
  # Test cases
end
```

# `context`: Precondition

`context` is a place to hold the condition that should be satisfied before running the test. It can be a type of input or precondition imposed on the target class. We put the type of input passed to the `run` method of FizzBuzz.

```ruby
describe FizzBuzz do
  context '3-multiple' do
    # Test here
  end

  context '5-multiple' do
    # Test here
  end

  context '15-multiple' do
    # Test here
  end

  context 'other' do
    # Test here
  end
end
```

# `it`: Expectation

We describe the expected output from the method or object in `it` (or `example`).


```ruby
describe FizzBuzz do
  context '3-multiple' do
    it 'Get Fuzz' do
      expect(FuzzBuzz.run(3)).to eq('Fuzz')
      expect(FuzzBuzz.run(6)).to eq('Fuzz')
    end
  end

  context '5-multiple' do
    it 'Get Buzz' do
      expect(FuzzBuzz.run(5)).to eq('Buzz')
      expect(FuzzBuzz.run(10)).to eq('Buzz')
    end
  end

  context '15-multiple' do
    it 'Get FizzBuzz' do
      expect(FuzzBuzz.run(15)).to eq('FizzBuzz')
      expect(FuzzBuzz.run(30)).to eq('FizzBuzz')
    end
  end

  context 'other' do
    it 'Get original number' do
      expect(FuzzBuzz.run(4)).to eq(4)
      expect(FuzzBuzz.run(8)).to eq(8)
    end
  end
end
```

This guideline is so helpful to me for writing the well-structured test in RSpec. The background information behind the scene is explicit with this structure.