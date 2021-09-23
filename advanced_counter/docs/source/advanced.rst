Advanced Usage
==============

IncrementBy Helpers
-------------------
AdvCounter can handle more complicated incrementing approaches if needed, we provide two such helpers
for this, IncrementByDict and IncrementByList, but you can sub-class any of the IncrementBy... classes and create
your own if you with for something more complex.

Default (IncrementByValue)
++++++++++++++++++++++++++
The default, and most basic incrementBy helper will simply allow setting a default value (by default 1)
which will be used anytime no values are passed to the add/sub/mult/div methods.

.. note::
    Values passed to the increment_by parameter in instantiating the class will use the IncrementByValue helper.

By Dict (IncrementByDict)
+++++++++++++++++++++++++
An increment by dict helper allows passing a dictionary of values to the system, which
can be called using the keys in the dict passed as parameters to the add/sub/mult/div/set methods.

Default value:

    * A '_default_' key can be included that will be used when no key is passed.
    * If no "_default_" key is included, a KeyError will be raised if no key value is passed.

Invalid Value:

    * An '_invalid_' key can be included that will be used when an invalid key is passed.
    * If no "_invalid_" key is included, a KeyError will be raised if an invalid key is passed.
    * If a '*' is used for the '_invalid_' key value, the passed value will be passed through.

.. note::
    A dictionary can be passed as part of the increment_by parameter when creating an AdvCounter object
    (or as a default setting for a NamedCounter)

Example::

    >>> ac = AdvCounter(increment_by={'half': 2, 'pi': 3.14, '_default_': 2, '_invalid_': '*'})
    >>> ac.value
    0
    >>> ac()
    2
    >>> ac.mult('pi')
    6.28
    >>> ac.add(10)
    16.28
    >>> ac.div('half')
    8.14


By List (IncrementByList)
+++++++++++++++++++++++++

An increment by list helper allows passing of a list of values, which will be used in order.

By default, the last value in the list will continue to be used after all list elements have been used.

Example::

    >>> backoff_seconds = AdvCounter(increment_by=[1, 2, 10, 120])
    >>> backoff_seconds.value
    0
    >>> backoff_seconds() # adds 1
    1
    >>> backoff_seconds() # adds 2
    3
    >>> backoff_seconds.set() # sets to 10
    10
    >>> backoff_seconds.add() # adds 120
    130
    >>> backoff_seconds.add() # adds 120
    250

You can also access the individual increments by using the list index.

Example::

    >>> backoff_seconds = AdvCounter(increment_by=[1, 2, 10, 120])
    >>> backoff_seconds.value
    0
    >>> backoff_seconds(2) # adds 10
    10
    >>> backoff_seconds.sub(0) # subtracts 1
    9
    >>> backoff_seconds.set(3) # sets to 130
    120

The following options would require instantiating am IncrementByList object first, then passing it to the
increment_by parameter when creating the AdvCounter object.

There is a question of what happens with the index point when a value is passed.
There are 4 approaches to this,

* INCREMENT_LIST_ON_INDEX_INCREMENT = this option will move the index position forward even if a specific value is passed.
* INCREMENT_LIST_ON_INDEX_RESET = this option will move the index position to position 0 in the list.
* INCREMENT_LIST_ON_INDEX_SET = this option will move the index position to the value passed.
* INCREMENT_LIST_ON_INDEX_INCREMENT = this option will not move the index position forward.

These can be imported and used in the increment_on_index parameter in the IncrmentByList object.

As noted earlier, by default, the IncrementByList helper will continue to return the last item in the list after the
rest of the list is used.  if you instantiate the IncrementByList helper using the repeat_all=True argument, the list will
loop around and start at the beginning.

If an invalid index position is passed, by default AdvCounter will raise an IndexError, however if you set the
"default=<num>" parameter the system will return that value if an invalid index position is passed.

.. note::
    A list can be passed as part of the increment_by parameter when creating an AdvCounter object
    (or as a default setting for a NamedCounter)


Custom Helpers
++++++++++++++

Custom increment by helpers are called passing any values that are passed to the add/sub/mult/div/set functions.
you can create a custom helper as a function or class that can be called and returns a value that can be used to
add/subtract/multuply or divide.


Call Function Every...
----------------------

There is the ability to set a function that will be called every x times that the counter is changed.  This allows
a percentage done or status parameter, or updating the screen without having to do it every call.

Function parameters
+++++++++++++++++++

The function is called and the counter itself is passed, allowing the called function to access the counter size
and any other settings.

Call Every Parameters
+++++++++++++++++++++

There are two parameters used for this feature,

* call_every=<number>: This defines how often the parameter is called.  for example, if this is set to 100, the function
  will be called every 100 times that the AdvCounter is called.  If this is a string ending with a "%", and if
  the min/max couner arguments are passed, this will the function based on the percentage complete.
* call_every_func=<function>: This defined the function that is called.

Call Every Defaults
+++++++++++++++++++
If no call_every number is passed, but a call_every_func is passed, a default call_every will be selected based on
the max_counter setting.

max counter of:
    * 0-10, call_every=1
    * 11-100, call_every=10
    * 101-500, call_every=20
    * 500-1000, call_every=100
    * 1001-5000, call_every=500
    * 5001+, call_every=1000
    * None,  call_every=100

