Usage of NamedCounter
=====================

In addition to the AdvCounter class, there is a NamedCounter class that allows maintaining
and interacting with multiple counters.

Basic Usage
-----------
When you create the NamedCounter, you can also create some initial named counters.

Example::

    >>> nc = NamedCounter('c1', 'c2', 'c3')

Also, when you instantiate the named counter, you can also set defaults for the sub-counters created under it::

    >>> nc = NamedCounter('c1', 'c2', 'c3', min_counter=1, max_counter=100)


Accessing Counters
------------------
There are four ways to access the counters,
if you create a NamedCounter with three counters, like::

    >>> nc = NamedCounter('c1', 'c2', 'c3')

By attribute::

    >>> nc.c1 += 10
    10

By item::

    >>> nc['c1'].sub(5)
    5

By the get method::

    >>> nc.get('c1').add(4)
    9

By passthrough (which will directly pass values through to one or more counters.)::

    >>> nc.add('c1', 3)
        12

Note that the passthrough options support add/sub/mult/div/set/clear/set_max, and will take a single
counter key or multiple keys.  if multiple keys are provided, the return will be a dictionary of keys/new values.
A '*' can be passed for the key all counters will be impacted.

Examples::

    >>> nc = NamedCounter('c1', 'c2', 'c3')
    >>> nc.add('c1', 4)
    4

    >>> nc.add(['c3', 'c3'], 10)
    {'c2': 10, 'c3': 10}

    >>> nc.sub('*', 2)
    {'c1': 3, 'c2': 9, 'c3': 9}


Locked v. Unlocked
------------------
If the NamedCounter is unlocked, when an unknown key is passed a new counter will automatically be created.
the locked status is controlled by:

- If you create the named counter with counters initially, the NamedCounter object will be locked.
- If you create the NamedCounter without counters, it is unlocked
- You can change the value of NamedCounter.locked at any time
- Locking the NamedCounter does not impact directly calling the .new() method.

Keys and Names
--------------
Each counter is created using a key, you can also pass a name value that will be used in reporting
for a more verbose name if desired.  A description can also be passed to the new counters created to provide deeper
descriptions

The key value is slugified initially to allow it to be used as an attribute of the NamedCounter,
this means taht if you pass a key of 'my counter', it will be saved as my_counter.
If you pass a name that cannot be converted to an apropirate key, you can still access it by
using the .get() or getting by item [].


Adding new counters
-------------------
counters can be added during instantiation in several ways:

By name only: NamedCounter('key1', 'key2', 'key3')
* These will be created using the default settings for AdvCounter (or using whatever parameters passed)

By keyword:  NamedCounter(key1=100, key2={'max_counter'=100, 'name'='my name # 2'}, key3=AdvCounter())
* If a number is passed (int, float, or Decimal) the counter will be created using that as the current value
* if a dictionary is passed, the AdvCounter will be created using that dictionary (this is one way of adding a name and description to the counter)
* if an existing AdvCounter instance is passed, it will be added to the NamedCounter instance.

In addition, counters can be added after initialization using the AdvCounter.new() method.


Removing Counters
-----------------
You can remove counters using the AdvCounter.remove('key') command

Reporting from Counters
-----------------------
You can generate a string block that contains the current status of the counters, including custom
headers and footers, and formatting of each of counters.  This can allow for faster reporting on the status
of a set of counters at the end of a process.



API
---

.. autoclass:: advanced_counter.NamedCounter
    :member-order: groupwise
    :members:
