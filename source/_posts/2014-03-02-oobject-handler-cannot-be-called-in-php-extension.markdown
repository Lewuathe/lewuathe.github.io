---
layout: post
title: "Object handler cannot be called in php extension"
date: 2014-03-02 00:38:00 +0900
comments: true
categories: ["PHP", "Extension", "Problem"]
author: Kai Sasaki
---

I have a problem.

[object handler cannot be called in php extension](http://stackoverflow.com/questions/22113672/object-handler-cannot-be-called-in-php-extension)

I am developing PHP extension. However, I am not sufficient familiar with PHP extension. 
So in this time, I have no answer how to solve this problem by myself.

<!-- more -->


I cannot call destructor of my class written in C++(in below code, `foo` is that. In my inspection, I know PHP_MINIT_FUNCTION was called definitely. Inside of PHP_MINIT_FUNCTION, set code for create_object might not be done properly. When deleting foo, foo_free_strage should be called, but not called.

```php
static zend_class_entry* foo_ce;
static zend_object_handlers foo_object_handlers;

void foo_free_storage(void *object TSRMLS_DC)
{
  std::cout << "php_foo destracter" << std::endl;
  foo_object* obj = (foo_object*)object;
  delete obj->foo_pointer;

  efree(obj);
}

zend_object_value foo_create_handler(zend_class_entry *type TSRMLS_DC)
{
  std::cout << "php_foo handler" << std::endl;
  zval *tmp;
  zend_object_value retval;

  foo_object *obj = (foo_object *)emalloc(sizeof(foo_object));
  memset(obj, 0, sizeof(foo_object));
  obj->std.ce = type;

  retval.handle = zend_objects_store_put(obj, NULL, foo_free_storage, NULL TSRMLS    _CC);
  retval.handlers = &foo_object_handlers;

  return retval;
}


// Initialization
PHP_MINIT_FUNCTION(bar){
  zend_class_entry ce;
  INIT_CLASS_ENTRY(ce, "Foo", foo_functions);
  foo_ce = zend_register_internal_class(&ce TSRMLS_CC);
  foo_ce->create_object = foo_create_handler;
  memcpy(&foo_object_handlers, zend_get_std_object_handlers(), sizeof(zend_object    _handlers));
  foo_object_handlers.clone_obj = NULL;
  return SUCCESS;
}
```

My development enviromnment is as listed below.

* CentOS [x86_64]
* gcc 4.4.7

Could someone lets me know the solution of this problem?
If someone has any advice to me, please inform [@Lewuathe](https://twitter.com/Lewuathe).

Thank you.