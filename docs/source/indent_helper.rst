Indent Helper
=============

This helper class provides a changable indent level that can be used to create indents for for output files
such as a log.


The intent is to be able to provide indent levels so instead of looking like::

    starting the process
    entering loop
    doing something
    entering sub-loop
    doing something else
    trying to fix something
    saving the record
    exiting the sub loop
    entering sub-loop
    doing something else
    saving the record
    exiting the sub loop
    entering sub-loop
    doing something else
    error saving the record
    exiting the sub loop
    checking the status
    exiting the main loop
    finishing the procees

The output could look more like this::

    starting the process
        entering loop
            doing something
                entering sub-loop
                    doing something else
                    trying to fix something
                    saving the record
                exiting the sub loop
                entering sub-loop
                    doing something else
                    saving the record
                exiting the sub loop
                entering sub-loop
                    doing something else
                    error saving the record
                exiting the sub loop
            checking the status
        exiting the main loop
    finishing the procees




the code to do the above could look similar to::


    def do_something(record_list):
        ih = IndentHelper()
        ih.push('main level')
        print(ih + 'starting the process')
        ih += 1
        for rec in record list:
            print('%s entering loop' % ih)
            ih.add(1)
            for field in rec:
                ih.print('doing something')

                print(ih.indent_text('checking the status something')
                with ih:
                    print(ih + 'entering sub loop')
                    with ih:
                    print (f'{ih}doing something else')
                    try:
                        print (f'{ih}doing something else')
                        print (f'{ih}saving the recird')
                    except:
                        print (f'{ih}error saving the record')

                    print(ih + 'exiting sub loop')
            ih.sub()
            print('checking the status')
            print('%s exiting main loop' % ih)
        ih.pop('main_level')
        print(ih + 'finishing the process')

As you can see, there are several ways of performing the same operation, these are detailed below.

This is based on the AdvCounter object and shares much of the same math approaches.

The main difference is that the main math methods (add/sub/mult/div/set) can be chained.  In other
words, you can do something like the following::

    >>> ih = IndentHelper()
    >>> ih.add(3).sub(3).set(29)
    IndentHelper(29)



Setup
-----

When instantiating the IndentHelper class, you have a few parameters that you can pass

:initial_indent: This is the initial indent level to start with,  (defaults to 0)
:spaces: This is the size of each indent (defaults to 4)
:max_size: This is the max number of indents (defaults to 20)
:char: this is the character used to indent (defaults to ' ')
:kwargs: any additional kwargs are used to setup named indent levels (see changing levels, named levels below)

Changing levels
---------------

you have several ways of changing the current level

Adding / Subtracting / Setting the level
++++++++++++++++++++++++++++++++++++++++

You can directly change the level by adding/subtracting/or setting the level

Example::

    >>> ih = IndentHelper()
    >>> ih.add()  # if you do not pass a value, 1 level is added or subtracted
    >>> ih += 1
    >>> ih.sub(2)
    >>> ih -= 1
    >>> ih.set(0)

    # you can also chain them together to reset the level, then add or subtract from that.
    >>> ih.set(0).add()

    # as with the AdvCounter class, you can also just call the instance
    >>> ih()  # will add 1)
    >>> ih(sub=1)  # will subtract 1

.. note::
    The multiplication and division  functions from AdvCounter are still present in this sub-class, however
    we do not see a major use for them in this use case, so have not documented them.


Named levels
++++++++++++

You can setup specific levels with names that can be used/recalled as needed.  Normally this would be used to
setup a base level before going into a function so that if for some reason the function errors out or misses reducing the
level, your indents will not get out of sync.

Example::

    >>> ih += 3
    >>> ih.push('before doing something')
    >>> int(ih)
    3
    >>> ih += 2
    >>> ih += 1
    >>> ih -= 2  # We missed reducing the indent 1 level here!
    >>> int(ih)
    4
    >>> ih.pop('before doing something')  # This also removed the 'before doing something' key from the memory
    >>> int(ih)
    3

    # This can also be retrieved without removing the key by passing the name to the set method.
    >>> ih.set('before doing something').  # Though this would actually error since it was removed by the pop above.


Saved Levels
++++++++++++

If you use push/pop without any keys, the system will save the current level to a queue and pop the last level from the
queue, this way you dont necessarily have to name everything.

Example::

    >>> int(ih)
    4
    >>> ih.push()
    >>> ih += 2
    >>> ih.push()
    >>> ih()
    >>> int(ih)
    7

    >>> ih.pop()
    >>> int(ih)
    6

    >>> ih.pop()
    >>> int(ih)
    4


Context manager
+++++++++++++++

An even easier way if handling this without having to worry about push/pop is to use IndentHelper as a context manager.

For example:

.. code-block:: python

    from advanced_counter import IndentHelper

    def test_indent():
        ih = IndentHelper()
        ih.print('line 1')
        with ih:
            ih.print('line 2')
            ih().print('line3')
        ih.print('line4')



would result in::

    >>> test_indent()
    line 1
        line 2
            line 3
    line 4

Getting output
--------------

There are also several ways of getting output from the instance.

Examples::

    >>> ih(2)
    # the following will return the indent as a string
    >>> str(ih)
    >>> ih.i
    '        '

    # this means that it can be used in formatting methods:

    >>> 'before indent %s foobar' % ih
    >>> f'before indent {ih} foobar'
    >>> 'before indent {} foobar'.format(ih)
    'before indent          foobar'

    # the following will combine the indent with a passed string
    >>> ih + 'foobar'
    >>> ih.print('foobar')
    >>> ih.indent_text('foobar')   # see the api docs for more options with indent_text
    '        foobar'

    # the following returns the current indent depth
    >>> ih.indent
    >>> ih.value
    2



Other operations
----------------

In addition to the above, there are a few standard python methods that are supported

Examples::

    # to check to see if there is a saved name:
    >>> ih.push('test1')
    >>> 'test' in ih
    True

    # to see the current lenght of the indent string (i.e. the current indent * number of characters)
    >>> ih.set(3)
    >>> len(ih)
    12

    # To see if the indent was ever changed:
    >>> bool(ih)
    True

Other Helpers
-------------

Also included are two helper items

indent_text
+++++++++++
This is a function that can indent text in various forms.  similar to pythons textwrap.indent, but allowing passing of
the indent size and character instead of just an indent string.

(see api docs below for more information)

DeferredIndent
++++++++++++++

This is a class that will defer processing the indent until a later time, saving processing time if it is not needed.
This is similar to examples in the python logging cookbook.

(see api docs below for more information)


API
---

.. autoclass:: advanced_counter.IndentHelper
    :member-order: groupwise
    :members:

.. autofunction:: advanced_counter.indent_helper.indent_text

.. autoclass:: advanced_counter.indent_helper.DeferredIndent