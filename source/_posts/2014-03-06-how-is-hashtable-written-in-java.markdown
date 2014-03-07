---
layout: post
title: "How is HashMap written in Java"
date: 2014-03-06 22:22:04 +0900
comments: true
categories: ["Java", "HashTable"]
author: Kai Sasaki
---

Here recently, I have a chance to read Java core API, expecially *HashMap*.
Usually, I use HashMap paying no attention to, but this code reading brought many things to me.
I can understand that how HashMap is written in Java and more this is very simple than I expected.
So in this post, I'd like to introduce some ideas and code used in `java.util.HashMap`.

<!-- more -->

## Constructor

```java
public class HashMap<K,V> extends AbstractMap<K,V>
        implements Map<K,V>, Cloneable, Serializable {

    public HashMap() {
	    // DEFAULT_INITIAL_CAPACITY is 16
		// DEFAULT_LOAD_FACTOR is 0.75f
	    this(DEFAULT_INITIAL_CAPACITY, DEFAULT_LOAD_FACTOR);
	}
}
```

This is `HashMap` constructor. `DEFAULT_INITIAL_CAPACITY` is the default size of array. This value is set as below.
`DEFAULT_LOAD_FACTOR` is the ratio of the number of put items to maximum capacity of hash table. Default value is 0.75f.

```java
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
```

Only 16 items can be retained in HashMap. What happen if this size become insufficient for your use?
In every code of adding item, this line was added.

```java
if ((size >= threshold) && (null != table[bucketIndex])) {
    resize(2 * table.length);
    hash = (null != key) ? hash(key) : 0;
    bucketIndex = indexFor(hash, table.length);
}
```

Threshold means the next size to which this table will resized. So if there are more items than an array can keep,
array is resized by `resize` and hash value is calculated based on the new table size. `resize` is defined as below.

```java
void resize(int newCapacity) {
    Entry[] oldTable = table;
    int oldCapacity = oldTable.length;
    if (oldCapacity == MAXIMUM_CAPACITY) {
	    // Setting next size to max
        threshold = Integer.MAX_VALUE;
        return;
    }

    Entry[] newTable = new Entry[newCapacity];
	// move all items to new hash table
    transfer(newTable, initHashSeedAsNeeded(newCapacity));
    table = newTable;
    threshold = (int)Math.min(newCapacity * loadFactor, MAXIMUM_CAPACITY + 1);
}
```

Create new table, and transfer all items to new table. It is simple, isn't it?
So keep going to `put`. the core algorithm of this method is hashing key.

## Put

Put code is written as below.

```java
public V put(K key, V value) {
    if (table == EMPTY_TABLE) {
        inflateTable(threshold);
    }
    if (key == null)
       return putForNullKey(value);
	// Get hash value of this key object
    int hash = hash(key);
	// Get index in the hash table, so called bucket
    int i = indexFor(hash, table.length);
    for (Entry<K,V> e = table[i]; e != null; e = e.next) {
	   // Search the item that has same key object
       Object k;
       if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
          V oldValue = e.value;
          e.value = value;
          e.recordAccess(this);
          return oldValue;
       }
    }

    // If there no item that match the given key, create new entry.
    modCount++;
    addEntry(hash, key, value, i);
    return null;
}
```

If table is not created yet, make it by using `inflateTable`. Then hasing with `hash`. `hash` is defined as below.

```java
final int hash(Object k) {
    int h = hashSeed;
    if (0 != h && k instanceof String) {
       return sun.misc.Hashing.stringHash32((String) k);
    }

    h ^= k.hashCode();

    // This function ensures that hashCodes that differ only by
    // constant multiples at each bit position have a bounded
    // number of collisions (approximately 8 at default load factor).
    h ^= (h >>> 20) ^ (h >>> 12);
    return h ^ (h >>> 7) ^ (h >>> 4);
}
```

If the key object is `String`, `sum.misc.Hashing.stringHash32` is used as hashing algorithm. In the other case, make use of `Object.hashCode()`.
This method is declared in `Object` class. So all objects in Java should implements this method or defined already super classes.
In both cases, `k.hashCode()` can be called safely. In order to make sure that hash value is unique in hash table, some bit calculations
are operated on `h`. So now, you can get hash value correspond to key object.

Please pay attention to the data structure used for storing items. This is implemented as chaining pattern.
Back to `put` method.

```java
int hash = hash(key);
int i = indexFor(hash, table.length);
for (Entry<K,V> e = table[i]; e != null; e = e.next) {
    Object k;
    if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
       V oldValue = e.value;
       e.value = value;
       e.recordAccess(this);
       return oldValue;
    }
}

modCount++;
addEntry(hash, key, value, i);
return null;
```

After getting index for hash value with `indexFor(hash, table.length)`, take a chain from correspond bucket item.
`table[i]` is the first item of this linked list. In the case of existing the value which has same key, update value.
If there are overlapped items in this table, linked list has multiple items. To reduce calculation cost, new item is prepend to this list in `addEntry`

```java
void addEntry(int hash, K key, V value, int bucketIndex) {
    if ((size >= threshold) && (null != table[bucketIndex])) {
        resize(2 * table.length);
        hash = (null != key) ? hash(key) : 0;
        bucketIndex = indexFor(hash, table.length);
    }
    createEntry(hash, key, value, bucketIndex);
}
```

`createEntry` prepends this put value.

```java
void createEntry(int hash, K key, V value, int bucketIndex) {
    Entry<K,V> e = table[bucketIndex];
	// hash: hash value that belongs to new entry
	// key: key object that belongs to new entry
	// value: content value that belongs to new entry
	// e: next node that is append to new entry item
    table[bucketIndex] = new Entry<>(hash, key, value, e);
    size++;
}
```

`Entry` constructor receives its hash value, key value, content value and next node for linked list.
So in this line, new object which is put on the hash table is prepend to the line of linked list.
It will be the first object of the list.

## Get

When you want to get target item that is correspond to your key, how is it works?

Now, `getEntry` is called.

```java
final Entry<K,V> getEntry(Object key) {
    if (size == 0) {
       return null;
    }

    int hash = (key == null) ? 0 : hash(key);
    for (Entry<K,V> e = table[indexFor(hash, table.length)];
	    // Search through linked list
        e != null; e = e.next) {
        Object k;
        if (e.hash == hash && ((k = e.key) == key || (key != null && key.equals(k))))
            return e;
    }
    return null;
}
```

Under given key, this code do linear search through linear list in the bucket item. Inside the list,
returns the item which matches a given key object. This is simpler than I expected, but thanks to this code
I can understand how `HashMap` works in Java programming language.

This code reading is so fun to me that I want to keep this activity as possible.

Thank you.
