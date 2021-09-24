AdvancedCounter
===============

This utility class provides some helpers for more advanced counting needs.

This was intended to help with the many times that I was trying to maintain multiple counters in
an application, then needed to do various things with those counters such as pass them to/from
other modules, reporting on counters at the end of a process, etc.

This is also the base module for a number of other functions that have similar needs

Some of the abilities that this provides are:

* Increment counters by a set value each time.
* Increment counters by more complex approaches.
* fixed min/max options for counters, as well as rollover/rollunder when the counter exceeds the min/max.
* tracks percentages and can handle percentage math against the counter.
* Multi-counter helper that maintains multiple named counters and can return a final report on the counters.
* Call a function every x times the counter is called (updating a status message).

Also included is a sub-class of AdvCounter called IndentHelper that provides some functions for handling running indents

Documentatation is at: https://advancedcounter.readthedocs.io/en/latest/
Source is at: https://github.com/dstrohl/AdvancedCounter
This can be installed via pypi and pip with

    >>> pip install AdvancedCounter

