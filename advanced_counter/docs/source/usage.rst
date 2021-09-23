Usage of Advanced Counter
=========================

For details of the methods and parameters, see the api documentation.

Basic Usage
-----------
The basic usage of the counter includes instantiating it, then calling it as needed to update the counter.

There are 5 main methods used to update the counter.
- add: Add something to the counter
- sub: subtract something from the counter
- mult: multiply the counter by something
- div: divide the counter by something
- set: set the counter to something

in each case, by default, if you do not pass a value to the method, we will
use the default value of 1.

Note: this can be modified by using different increment By helpers,
see the advanced section for more information.

In addition, you can use In-Place math for the 3 main math methods.

* add: use +=
* sub: use -=
* mult: use \*=
* div: use /=

Examples::

    # no parameters will setup a counter starting at 0 and incrementing by 1.
    >>> ac = AdvCounter()
    >>> ac.value
    0
    >>> ac.add()
    1
    >>> ac()
    2
    >>> ac.mult(5)
    10
    >>> ac.sub(2)
    0
    >>> ac += 200
    200
    >>> ac /= 50
    4
    >>> ac.set(5)
    5

    # AdvCounter will return a new instance when used in normal math operations
    >>> ac + 200
    AdvCounter(205)

Using Min / Max options
-----------------------
If desired, you can also set minimum and maximum counter values.

By default, a minimum or maximum will keep the counter from exceeding that value.
you can set the rollover option during instantiation to change this behavior to
rollover / rollunder if the counter exceeds the value.

Examples without rollover::

    >>> ac = AdvCounter(min_counter=1, max_counter=10)
    >>> int(ac)
    0
    >>> ac += 100
    10
    >>> ac.set(0)
    1

    Examples with rollover:
    >>> ac = AdvCounter(min_counter=1, max_counter=10, rollover=True)
    >>> int(ac)
    0
    >>> ac += 15
    5
    >>> ac.set(0)  # note that the set operation does not rollover but will still only set
                     the value to within the min/max values.
    1


Percentage Operations
---------------------
If a min_counter AND max_counter is set, you can also do percentage operations.
This allows you to trace the percentage finished or add/subtrace based on percentages.

You can get the percentage from the counter using the perc and perc_str properties.

Example::

    >>> ac = AdvCounter(value=15, min_counter=1, max_counter=100)
    >>> ac.perc
    0.15
    >>> ac.perc_str
    '15%'

If you pass a string ending with a '%' You can also perform percentage math on the counter.

Note that the math methods work slightly different with percentages.
add/sub/set: We will calculate the increment by based on the percentage of max_count, then add/sub or set that value.
mult/div: We will calculate the increment by value based on multiplying or dividing the current value against the percentage.

Examples::

    >>> ac = AdvCounter(value=10, min_counter=1, max_counter=100)
    >>> ac('50%')
    60
    >>> ac.sub('10%')
    50
    >>> ac *= '50%'
    25
    >>> ac /= '50%'
    50
    >>> ac.set('75%')
    75

Standard Methods
----------------


In addition, AdvCounter has several standard python methods defined:

Examples::

    >>> ac = AdvCounter()
    >>> for i, c in enumerate(ac):
    >>>      print(str(c)
    >>>      if i == 5:
    >>>           break
    1
    2
    3
    4
    5
    >>>

    # len(AdvCounter()) returns the number of times that the instance was called
    >>> len(ac)
    5

    # bool(AdvCounter()) returns true if the instance was ever called
    >>> bool(ac)
    True

    # str(AdvCounter()) returns a string representation of the current value
    >>>  str(ac)
    '205'

    # int(AdvCounter()) returns the current value as an integer
    >>> int(ac)
    205

    # float(AdvCounter()) returns the current value as a float
    >>> float(ac)
    205.0

    # copy(AdvCounter()) returns a new instance with the same settings.
    >>> copy(ac)
    AdvCounter(205)



.. warning::
    In most cases iterating the counter will not stop as the counters are intended to continue indefinitely,
    so your loop must have a break option built in.

Calling
-------

you can also directly call the instance and control math using parameters.

Examples::

    >>> ac = AdvCounter()
    >>> ac(10)  # adds to the counter
    10
    >>> ac(sub=10)  # subtracts from the counter
    0
    >>> ac(set=100, add=4)  # sets the value to 100, then adds 4.
    104

Operations are performed using the following order:

1. set
2. multiplication
3. division
4. addition
5. subtraction



API
---

.. autoclass:: advanced_counter.AdvCounter
    :member-order: groupwise
    :members:
