"""

This utility provides some advanced counting functions allowing for easier counting and incrementing.

"""
__author__ = 'strohl'
__version__ = '0.9'
__status__ = 'Testing'

import decimal
from collections import OrderedDict
from .helpers import make_list, minmax, slugify, _UNSET
import logging

log = logging.getLogger(__name__)

__all__ = ['NamedCounter', 'AdvCounter', 'IncrementByDict', 'IncrementByList', 'IncrementByValue',
           'INCREMENT_LIST_ON_INDEX_INCREMENT', 'INCREMENT_LIST_ON_INDEX_RESET', 'INCREMENT_LIST_ON_INDEX_NOTHING']


class IncrementByValue(object):
    """
    this is a helper class that can be used for more advanced increment by operations.
    See IncrementByDict and IncrementByList for examples.
    """
    counter = None
    name = 'base_increment_by'

    def __init__(self, value=1, no_scan=False):
        self.increment_by = value
        if not no_scan:
            self.scan_values(self.increment_by)

    def scan_values(self, value):
        if isinstance(value, str):
            if not (value.endswith('%') and value[:-1].isdecimal()):
                raise TypeError('Increment By value is a a string but not a percentage: %r' % value)
        elif not isinstance(value, (int, float, decimal.Decimal)):
            raise TypeError('Increment By value is an invalid type: %r' % value)

    def dump(self, sep='\n'):
        tmp_ret = [
            'IncrementByValue',
            'Default Value: %s' % self.increment_by]
        if sep is not None:
            return sep.join(tmp_ret)

    def __call__(self, increment_by=None):
        """
        This must return a value that is used for the increment by.
        :param increment_by:
        :return:
        """
        if increment_by is None:
            return self.increment_by
        return increment_by


class IncrementByDict(IncrementByValue):
    """
    This allows a dictionary like object to be used to return the increment by value.

    With this helper, you can save specific increment by values in a dictionary and use them based on the keys.

    So, with a dict like {'foobar': 5, 'snafu' -1}, you can do ac('foobar') and it will increment the counter by 5
    """

    def __init__(self, value, default_value=1, invalid_value='*', no_scan=False):
        """
        :param value: this is a dict or dict like object that will be used for the increment by
        :param default_value:  this is the value that is returned if an invalid key or no key is passed.
            if None. a KeyError will be raised if an invalid key is passed.
            This can also be handled by including a '_default_' key in the dict.
            Note that if a '_default_' key is present, the default value will be ignored.
        :param no_scan:  By default this will check the dict to make sure that all retunable objects are int, float,
            or Decimal and raise a TypeError if not, if "no_scan" is True, this scan will not happen (for large dictionaries)
        """
        value = value.copy()
        if '_default_' not in value and default_value is not None:
            value['_default_'] = default_value
        if '_invalid_' not in value and invalid_value is not None:
            value['_invalid_'] = invalid_value
        super(IncrementByDict, self).__init__(value, no_scan=no_scan)

    def dump(self, sep='\n'):
        tmp_ret = [
            'IncrementByDict',
            'Dict Value: %r' % self.increment_by]
        if sep is not None:
            return sep.join(tmp_ret)


    def scan_values(self, value):
        for f, v in value.items():
            if f == '_invalid_' and v == '*':
                continue
            super(IncrementByDict, self).scan_values(v)

    def __call__(self, increment_by=None):
        """
        This must return a value that is used for the increment by.
        :param increment_by:
        :return:
        """
        try:
            return self.increment_by[increment_by]
        except KeyError:
            if increment_by is None:
                try:
                    return self.increment_by['_default_']
                except KeyError:
                    raise KeyError('Invalid key %r passed and no default value set.' % increment_by)
            else:
                try:
                    tmp_ret = self.increment_by['_invalid_']
                    if tmp_ret == '*':
                        return increment_by
                    return tmp_ret
                except KeyError:
                    raise KeyError('Invalid key %r passed and no default value set.' % increment_by)


INCREMENT_LIST_ON_INDEX_INCREMENT = 'increment'
INCREMENT_LIST_ON_INDEX_RESET = 'reset'
INCREMENT_LIST_ON_INDEX_SET = 'set'
INCREMENT_LIST_ON_INDEX_NOTHING = 'nothing'

class IncrementByList(IncrementByValue):
    """
    This allows a list or list like object to be used to return the increment by counter.

    with this helper, you can set a series of values that will be returned each increment (or can be called using the list index)

    So, passing [1, 2, 12, 23, 34, 45] would allow the counter to increment by that value each time it was called.

    You can choose to repeat the list once it has been used, or simply to use the last value again each time.
    """
    def __init__(self,
                 value,
                 repeat_all=False,
                 default_value=None,
                 increment_on_index=INCREMENT_LIST_ON_INDEX_INCREMENT,
                 no_scan=False):
        """
        :param value: this is a list or list like object that will be used for the increment by
        :param repeat_all: if True (defaults to False), the list will repeat after using all of it's elements.
        :param increment_on_index: when a specific index value is passed to the increment var, do we still move the
            list index position forward?
            INCREMENT_LIST_ON_INDEX_INCREMENT = this option will move the index position forward even if a specific value is passed.
            INCREMENT_LIST_ON_INDEX_RESET = this option will move the index position to position 0
            INCREMENT_LIST_ON_INDEX_SET = this option will move the index position to the value passed
            INCREMENT_LIST_ON_INDEX_INCREMENT = this option will not move the index position forward.
        :param default_value:  this is the value that is returned if an invalid index position is called.
            if None. an IndexError will be raised if an invalid index is passed.
        :param no_scan:  By default this will check the list to make sure that all list objects are int, float,
            or Decimal and raise a TypeError if not, if "no_scan" is True, this scan will not happen (for large lists)
        """
        value = value.copy()
        self.default_value = default_value
        self.increment_on_index = increment_on_index
        self.repeat_all = repeat_all
        self.current_index = -1
        self.max_index = len(value) -1
        super(IncrementByList, self).__init__(value, no_scan=no_scan)

    def dump(self, sep='\n'):
        tmp_ret = [
            'IncrementByList',
            'List Values: %r' % self.increment_by,
            'Default Value: %r' % self.default_value,
            'Inc On Index: %r' % self.increment_on_index,
            'Repeat All: %r' % self.repeat_all,
            'Current Index: %r' % self.current_index,
            'Max Index: %r' % self.max_index]

        if sep is not None:
            return sep.join(tmp_ret)

    def scan_values(self, value):
        for v in value:
            super(IncrementByList, self).scan_values(v)

    def get_next_index(self):
        self.current_index += 1
        if self.current_index > self.max_index:
            if self.repeat_all:
                self.current_index = 0
            else:
                self.current_index = self.max_index
        return self.current_index

    def __call__(self, increment_by=None):
        """
        This must return a value that is used for the increment by.
        :param increment_by:
        :return:
        """
        if increment_by is None:
            increment_by = self.get_next_index()
        else:
            if increment_by > self.max_index or increment_by < 0:
                if self.default_value is not None:
                    return self.default_value
                raise IndexError('Invalid increment by value (%r) passed.' % increment_by)
            if self.increment_on_index == INCREMENT_LIST_ON_INDEX_INCREMENT:
                self.get_next_index()
            elif self.increment_on_index == INCREMENT_LIST_ON_INDEX_SET:
                self.current_index = increment_by
            elif self.increment_on_index == INCREMENT_LIST_ON_INDEX_RESET:
                self.current_index = -1

        try:
            return self.increment_by[increment_by]
        except IndexError:
            if self.default_value is not None:
                return self.default_value
            raise IndexError('Invalid increment by value of %s passed' % increment_by)


class AdvCounter(object):

    value = 0
    increment_type = 'dict'
    increment_length = None
    increment_index = None
    call_count = 0
    call_countdown = 0
    _call_every = 0
    _init_call_every = 0
    field_names = None
    math_return = 'value'

    def __init__(self,
                 value=None,
                 min_counter=None,
                 max_counter=None,
                 rollover=False,
                 increment_by=1,
                 call_every=None,
                 call_every_func=None,
                 perc_decimal=0,
                 no_scan=False,
                 ):
        """

        :param value: The initial value for this counter.

        :param min_counter: if set, the value will never go below this setting (defaults to None)

        :param max_counter: if set, the value will never go above this value (defaults to None)

        :param call_every_func: a function can be passed that will be called for every x calls of the counter. (this includes add, sub, etc...)

            This function must take the signature of func(counter_obj).

        :param call_every: an integer that is used to determine when the call_every function will be called.
            if this is not set, and a call_every_func is passed, this will be based on the max_counter setting.

            * 0-10 records, every record
            * 11-100 records, every 10 records%
            * 101-500 records, every 20 records
            * 500-1000 records every 100 records%
            * 1001-5000 records, every 500 records
            * 5001+ records, every 1000 records%
            * if no max_counter setting, will call every 100 records

        :param rollover: If true, will start over at the min_counter once the max_counter is reached, and vice versa (for reverse)

            .. note::
                Rollover only happens with addition/subtraction of values, it will not happen with setting a value, multiplying or dividing it.
                in those cases, the value will be set to the max (or min) value.

        :param increment_by: any of the following: (defaults to 1)

             * int, float, Decimal: will add that value to each iteration by default.
             * list will use the IncrementByList helper
             * dict will use the IncrementByDict helper
             * passing an instance of an IncrementBy... helper will use that specific helper.

        :param no_scan: will skip scanning the increment_by values (for large lists and dicts, this can save init time)
            note this is only used when the IncrementBy instance is instantiated, passing an instance of an IncrementBy
            helper will not run the scan again.

        """

        self.rollover = rollover
        self.call_every = call_every
        self._init_call_every = call_every
        self.call_every_func = call_every_func
        self.perc_decimal = perc_decimal
        self.perc_format = "{:." + str(perc_decimal) + "%}"

        if isinstance(increment_by, (list, tuple)):
            self.increment_by = IncrementByList(increment_by, no_scan=no_scan)
        elif isinstance(increment_by, dict):
            self.increment_by = IncrementByDict(increment_by, no_scan=no_scan)
        elif not issubclass(increment_by.__class__, IncrementByValue):
            self.increment_by = IncrementByValue(increment_by, no_scan=False)
        else:
            self.increment_by = increment_by

        if min_counter is not None and max_counter is not None:
            if min_counter > max_counter:
                raise AttributeError('Min counter is larger than max counter.')
        if rollover and (min_counter is None or max_counter is None):
            raise AttributeError('Rollover only works of both min and max counters are set.')

        self.set_max(max_counter, min_counter)
        if value is None:
            value = self.min_counter or 0
        self._set(value, skip_count=True)

    def __copy__(self):
        tmp_ret = self.__class__(
            value=self.value,
            min_counter=self.min_counter,
            max_counter=self.max_counter,
            rollover=self.rollover,
            increment_by=self.increment_by,
            call_every=self.call_every,
            call_every_func=self.call_every_func,
            perc_decimal=self.perc_decimal,
            no_scan=True,
        )
        tmp_ret.call_countdown = self.call_countdown
        tmp_ret.call_count = self.call_count

        return tmp_ret

    copy = __copy__

    def set_max(self, max_counter=_UNSET, min_counter=_UNSET):
        """
        This will set the min and max counters, and reset the call_every values if needed.
        It will also update the value to be within the min/max values.

        :param max_counter: The desired maximum value for the counter
        :param min_counter: The desired minimum value for the counter
        """
        if max_counter is not _UNSET:
            self.min_counter = min_counter
        if min_counter is not _UNSET:
            self.max_counter = max_counter
        self._has_min_max = self.min_counter is not None and self.max_counter is not None

        if self.call_every_func is not None:
            if self._init_call_every is None:
                """
                0-10 records, every record
                11-100 records, every 10 records%
                101-500 records, every 20 records
                500-1000 records every 100 records%
                1001-5000 records, every 500 records
                5001+ records, every 1000 records%
                if no max_count setting, will call every 100 records
                """
                if self.max_counter is None:
                    self._call_every = 100
                elif self.max_counter <= 10:
                    self._call_every = 1
                elif self.max_counter <= 100:
                    self._call_every = 10
                elif self.max_counter <= 500:
                    self._call_every = 20
                elif self.max_counter <= 1000:
                    self._call_every = 100
                elif self.max_counter <= 5000:
                    self._call_every = 500
                else:
                    self._call_every = 1000
            else:
                if isinstance(self._init_call_every, str):
                    self.call_every = self._init_call_every
                    if self.call_every[-1] == '%':
                        if not self._has_min_max:
                            raise AttributeError('Unable to set a percentage for the call every, requires a min/max counter setting')
                        self.call_every = self.call_every[:-1]
                        self.call_every = decimal.Decimal(self.call_every) / 100
                        self.call_every = int(self.max_counter / self.call_every)

                self._call_every = self.call_every
            # log.debug('Setting the call every function to call every %s' % self.call_counter)
        self.call_countdown = self._call_every
        self._set(self.value, skip_count=True)

    def _get_increment(self, value=None, force=False, operation='add'):
        if not force:
            value = self.increment_by(value)
        is_perc = False

        if isinstance(value, str):
            if value[-1] == '%':
                is_perc = True
                value = value[:-1]
                value = decimal.Decimal(value)
            value = value / 100

        if is_perc and operation in ['add', 'sub', 'set']:
            value *= self.max_counter

        return value

    @property
    def perc(self):
        """
        This returns the percent that the current value is between the min and max counter settings.

        :return: this returns a decimal.Decimal value of the percentage. (i.e. it will return 0.20 for 20%)
        :raises AttributeError: If the min/max counters are not both set to a value.
        """
        if self.max_counter is None or self.min_counter is None:
            raise AttributeError('perc is only valid for counters with min and max_counter set.')
        perc_range = self.max_counter - self.min_counter
        my_range = self.value - self.min_counter
        return decimal.Decimal(my_range / perc_range)

    @property
    def perc_str(self):
        """
        :return: this returns a string percentage. (i.e. '20%')
        :raises AttributeError: If the min/max counters are not both set to a value.
        """
        return self.perc_format.format(self.perc)

    def _set(self, value=None, skip_call_every=False, skip_count=False):
        value = minmax(value, min_val=self.min_counter, max_val=self.max_counter, rollover=self.rollover)
        self.value = value
        if not skip_count:
            self.call_count += 1
            self.call_countdown -= 1
            if self.call_countdown <= 0:
                self.call_countdown = self._call_every
                if self.call_every_func is not None and not skip_call_every:
                    self.call_every_func(self)

    def clear(self):
        """
        Resets the value to the minimum counter or 0 if no minimum is set.
        """
        self.value = self.min_counter or 0
        self.call_count = 0
        self.call_countdown = self._call_every

    def __iadd__(self, other):
        return self._do_math(other, 'add', ret='self')

    def __isub__(self, other):
        return self._do_math(other, 'sub', ret='self')

    def __imul__(self, other):
        return self._do_math(other, 'mult', ret='self')

    def __idiv__(self, other):
        return self._do_math(other, 'div', ret='self')
    __itruediv__ = __idiv__

    def __add__(self, other):
        return self._do_math(other, 'add', ret='copy')

    def __sub__(self, other):
        return self._do_math(other, 'sub', ret='copy')

    def __mul__(self, other):
        return self._do_math(other, 'mult', ret='copy')

    def __truediv__(self, other):
        return self._do_math(other, 'div', ret='copy')

    def add(self, other=None):
        """
        Adds "value" to the counter.  if a list or dict incrementBy handler is used (see advanced usage), this will add the returned value from that.
        If a string percentage is passed ('44%', must include the percentage sign), this will add the percentage of the MAX_COUNTER value to the current counter.
        This can also be performed using the += operator.

        :return: This returns the current counter after the operation
        """
        return self._do_math(other, 'add', ret=self.math_return)

    def sub(self, other=None):
        """
        Subtracts"value" to the counter.  if a list or dict incrementBy handler is used (see advanced usage), this will subtract the returned value from that.
        If a string percentage is passed ('44%', must include the percentage sign), this will subtract the percentage of the MAX_COUNTER value to the current counter.

        This can also be performed using the -= operator.

        :return: Returns the current counter after the operation
        """
        return self._do_math(other, 'sub', ret=self.math_return)

    def mult(self, other=None):
        """
        multiplies the current counter by "value".  if a list or dict incrementBy handler is used (see advanced usage),
        this will multiply by the returned value from that.
        If a string percentage is passed ('44%', must include the percentage sign), this will multiply the current
        counter value by the percentage and set the counter to that value.

        This can also be performed using the \*= operator.

        :return: This returns the current counter after the operation
        """
        return self._do_math(other, 'mult', ret=self.math_return)

    def div(self, other=None):
        """
        Divides the current counter by "value".  if a list or dict incrementBy handler is used (see advanced usage), this will divide by the returned value from that.
        If a string percentage is passed ('44%', must include the percentage sign), this will divide the current
        counter value by the percentage and set the counter to that value.

        This can also be performed using the /= operator.

        :return: This returns the current counter after the operation
        """
        return self._do_math(other, 'div', ret=self.math_return)

    def set(self, other=None, ret=math_return, force=False):
        """
        Sets the current value to "value".  if a list or dict incrementBy handler is used (see advanced usage),
        this will set the counter to returned value from that.
        If a string percentage is passed ('44%', must include the percentage sign), this will set the percentage of the
        MAX_COUNTER value to the current counter.

        :param force:  If True, this will not look up the value from the increment by handler and will instead use the
            passed value.
        :return: This returns the current counter after the operation
        """
        return self._do_math(other, 'set', ret=ret, force=force)

    def _do_math(self, value=None, operation='add', ret=math_return, force=False):
        """
        :param value: the value to work on
        :param operation: can be ['add', 'sub', 'mult', 'div', 'set']
        :param ret:  can be ['self', 'copy', 'value']
        :param force: Will skip doing a lookup via the incrementBy helper and use the value directly.
        :return:
        """
        value = self._get_other(value)
        if ret == 'copy':
            tmp_ret = self.copy()
        else:
            tmp_ret = self

        value = tmp_ret._get_increment(value, force, operation=operation)

        if operation == 'add':
             value += tmp_ret.value

        elif operation == 'sub':
            value = tmp_ret.value - value

        elif operation == 'mult':
            value *= tmp_ret.value

        elif operation == 'div':
            value = tmp_ret.value / value

        elif operation != 'set':
            raise AttributeError('Invalid Operation: %r' % operation)

        tmp_ret._set(value)

        if ret == 'value':
            return tmp_ret.value
        return tmp_ret

    def __call__(self, add=_UNSET, ret=math_return, **kwargs):
        """
        :param value: the value to work on
        :param operation: can be ['add', 'sub', 'mult', 'div', 'set']
        :param ret:  can be ['self', 'copy', 'value']
        :return:
        """
        if ret == 'copy':
            tmp_ret = self.copy()
        else:
            tmp_ret = self

        def dm(op):
            tmp_ret._do_math(kwargs[op], op, ret='value')

        if add is not _UNSET:
            kwargs['add'] = add
        elif not kwargs:
            kwargs['add'] = None

        for op1 in ['set', 'mult', 'div', 'add', 'sub']:
            if op1 in kwargs:
                dm(op1)

        if ret == 'value':
            return tmp_ret.value
        return tmp_ret

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        tmp_ret = str(self)

        if self.min_counter is not None and self.max_counter is not None:
            tmp_ret += ' (%s <-> %s)' % (self.min_counter, self.max_counter)
        elif self.min_counter is None:
            tmp_ret += ' (%s <-> [any])' % self.min_counter
        elif self.max_counter is None:
            tmp_ret += ' ([any] <-> %s)' % self.max_counter

        if self.rollover:
            tmp_ret += ' [rollover]'

        return tmp_ret

    def __bool__(self):
        return bool(self.value)

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def __iter__(self):
        """
        Care should be used when using this as an iterator as it will continue to provide values forever, so any loops
        should have a break or max looping strategy built in.

        :return:
        """
        while True:
            self.add()
            yield self.value

    def _get_other(self, other):
        if issubclass(other.__class__, AdvCounter):
            return other.value
        else:
            return other

    def __compare__(self, other):
        compare_with = self.value
        other = self._get_other(other)
        if other == compare_with:
            return 0
        elif other > compare_with:
            return -1
        else:
            return 1

    def __eq__(self, other):
        return self.__compare__(other) == 0

    def __lt__(self, other):
        return self.__compare__(other) == -1

    def __le__(self, other):
        return self.__compare__(other) < 1

    def __gt__(self, other):
        return self.__compare__(other) == 1

    def __ge__(self, other):
        return self.__compare__(other) > -1

    def __len__(self):
        return self.call_count


class NamedCounter(object):
    counters = None
    counter_lookup = None
    def_counter_kwargs = None
    locked = False
    counter_count = 0
    name = None

    def __init__(self,
                 *args,
                 min_counter=None,
                 max_counter=None,
                 rollover=False,
                 increment_by=1,
                 locked=None,
                 name=None,
                 **kwargs):
        """
        :param args:
        :param min_counter:
        :param max_counter:
        :param rollover:
        :param increment_by:
        :param locked:
        :param as_perc:
        :param kwargs:
        """

        self.def_counter_kwargs = dict(
            value=min_counter,
            min_counter=min_counter,
            max_counter=max_counter,
            rollover=rollover,
            increment_by=increment_by,
        )
        self.name = name
        self.counters = OrderedDict()
        self.counter_lookup = {}
        for arg in args:
            self.new(arg)

        for key, value in kwargs.items():

            if isinstance(value, dict):
                self.new(key, **value)
            elif isinstance(value, str):
                self.new(key, name=value)
            else:
                self.new(key, value=value)

        if locked is None:
            locked = bool(args) or bool(kwargs)
        self.locked = locked

    def new(self, key, value=None, name=None, overwrite=False, description='', **kwargs):
        """
        add new counter, this can be called in various ways:

            * .new([key, value])
            * .new(key, value)
            * .new(CounterObj)
            * .new(key, value, name=xxx, <other counter args>)
            * .new(key)

        @param key: a key that is used to access this counter. this should be a string that can be used as a method name.
        @param name: defaults to the key, but allows setting a more verbose name for use in reports.
        @param value: the initial value to set the counter to. if this is am AdvCounter object, it will just be copied in.
        @param overwrite: By default the function will raise an AttributeError if the key is already used.  overwrite will overwrite the existing counter object.
        @param kwargs: any keyword arguments to be used by this counter.
        @return: Returns the created counter.
        """

        if issubclass(value.__class__, AdvCounter):
            counter = value
        else:
            tmp_kwargs = self.def_counter_kwargs.copy()
            tmp_kwargs.update(kwargs)
            if value is not None:
                tmp_kwargs['value'] = value

            counter = AdvCounter(**tmp_kwargs)

        if name is None:
            name = key

        counter.name = name
        counter.key = slugify(key)
        counter.description = description

        if counter.key in self and not overwrite:
            raise AttributeError('Key %r already exists in NamedCounter' % counter.key)
        self.counter_count += 1

        self.counters[counter.key] = counter
        self.counter_lookup[counter.key] = counter
        self.counter_lookup[counter.name] = counter
        return counter


    # *****************************************************************************
    # counter access methods (ways to get to a specific counter)
    # *****************************************************************************
    def get(self, key):
        if key not in self:
            if self.locked:
                raise KeyError('cannot add %s, counter locked with fields: %r' % (key, list(self.counters.keys())))
            return self.new(key)
        else:
            return self.counter_lookup[key]


    def __getitem__(self, item):
        return self.get(item)

    def __getattr__(self, item):
        try:
            return self.get(item)
        except KeyError:
            raise AttributeError('%s not an attribute' % item)

    # *****************************************************************************
    # reporting methods (ways of getting information out on multiple counters)
    # *****************************************************************************

    def dump(self, sep='\n'):
        tmp_ret = []
        for x in self.counters.values():
            tmp_ret.append(repr(x))

        if sep is None:
            return tmp_ret
        else:
            return sep.join(tmp_ret)

    def report(self,
               header='',
               footer='',
               justify_name='>',
               line_indent=None,
               counters=None,
               line_format=None,
               desc_line_format='    {indent}{description}',
               sep='\n',
               **kwargs):
        """
        @param header: Text that is placed at the beginning of the counters.
        if there is a name attribute, this defaults to "{name}",
        otherwise it defaults to empty.

        @param footer: Text placed after the counters are returned.

        .. note::
            headers and footers can include formatting keys including:

                * {num_counters}: this will return the nnumber of counters in the set.
                * {sum}, {min}, {max} : Note that these compute the sum, min, and max values of all counters
                * {indent}: see the line_format indent.  mainly used to indent the footer to the level of the lines.

        @param line_format: this will format each line.  available keys for this format string include:

            * {name}, {description}, {key}
            * {value}, {min_counter}, {max_counter},
            * {perc_complete}  :Note that {perc_complete} is only available if the max_counter is passed. otherwise it will ignored.
              The percentage returned already includes the '%' character.
            * {indent} :note that {indent} will indent the line based on the number passed in the "line_indent" parameter

        @param desc_line_format: if included, and if a counter has a description, this will be used on the line right after
        the counter line.  If the counter does not have a description, no line will be printed.
        If None, the description line will not be printed (though the {description} tag can ge used in the line format).
        @param counters: if None, all counters are passed, otherwise this list of counters is returned.

        @param justify_name: one of the following:

            * None: will not justify the name field
            * '<': will justify left based on the length of the longest name
            * '>': will justify right based on the length of the longest name (the default)

        @param line_indent:  this number is converted to a space string, which is then passed to the lines as "indent"
        (otherwise an "indent" string is passed with no contents)

        .. note::
            a None will indent 4 characters IF a header is included.

        @param line_format:

            * default with min/max counters = "{indent}{name} : {value} ({perc})"
            * default without min/max counters = "{indent}{name} : {value}"

        @param kwargs: These are passed to the formatting for the lines as well as the header/footer.
        @return: a string report formatted as specified.
        """
        if counters is None:
            counters = self.counters.keys()
        else:
            counters = make_list(counters)

        tmp_pad_size = 0
        all_value_min = 0
        all_value_max = 0
        all_value_sum = 0

        if not header and self.name:
            header = '{name}'

        if justify_name is not None or header or footer:
            for c in counters:
                c_rec = self.counters[c]
                val = c_rec.value
                tmp_pad_size = max(tmp_pad_size, len(c_rec.name))
                all_value_max = max(val, all_value_max)
                all_value_min = min(val, all_value_min)
                all_value_sum += c_rec.value

        if line_indent is None:
            if header or footer:
                line_indent = 4
            else:
                line_indent = 0

        indent = ''
        if line_indent:
            indent = ' ' * line_indent

        tmp_hf_dict = dict(
            num_counters=len(counters),
            name=self.name,
            sum=all_value_sum,
            min=all_value_min,
            max=all_value_max,
            indent=indent,
            **kwargs,
        )
        tmp_hf_dict.update(self.counters)

        tmp_ret = []

        if header:
            if '{' in header:
                tmp_ret.append(header.format(**tmp_hf_dict))
            else:
                tmp_ret.append(header)

        for c in counters:
            c_rec = self.counters[c]

            lf = line_format
            if c_rec._has_min_max:
                perc = c_rec.perc_str
                if lf is None:
                    lf = '{indent}{name} : {value} ({perc_complete})'
            else:
                perc = ''
                if lf is None:
                    lf = '{indent}{name} : {value}'

            name = c_rec.name
            if '{name}' in lf:
                if justify_name == '<':
                    name = name.ljust(tmp_pad_size)
                elif justify_name == '>':
                    name = name.rjust(tmp_pad_size)

            tmp_line_formatting_dict = dict(
                indent=indent,
                description=c_rec.description,
                name=name,
                key=c_rec.key,
                value=c_rec.value,
                min_counter=c_rec.min_counter,
                max_counter=c_rec.max_counter,
                perc_complete=perc,
                **kwargs,
            )

            tmp_ret.append(lf.format(**tmp_line_formatting_dict))
            if c_rec.description and desc_line_format:
                tmp_ret.append(desc_line_format.format(**tmp_line_formatting_dict))

        if footer:
            if '{' in footer:
                tmp_ret.append(footer.format(**tmp_hf_dict))
            else:
                tmp_ret.append(footer)

        if sep is not None:
            return sep.join(tmp_ret)
        return tmp_ret

    def keys(self):
        return self.counters.keys()

    def values(self):
        for rec in self.counters.values():
            yield rec.value
    __iter__ = values

    def items(self):
        for name, rec in self.counters.items():
            yield name, rec.value

    def remove(self, *keys):
        if not keys:
            keys = list(self.counters.keys())
        for key in keys:
            item = self.get(key)
            del self.counters[item.key]
            self.counter_lookup.pop(item.key, None)
            self.counter_lookup.pop(item.name, None)
            self.counter_count -= 1

    def __contains__(self, item):
        return item in self.counter_lookup

    # *****************************************************************************
    # pass through methods (will pass the args through to the underlying counter)
    # *****************************************************************************

    def _set_counter_attr(self, keys, attr, value=None, force_dict=False):
        tmp_ret = {}
        if keys == '*':
            keys = self.counters.keys()
        for key in make_list(keys):
            tmp_item = self.get(key)
            tmp_attr = getattr(tmp_item, attr)
            if value is not None:
                tmp_ret[key] = tmp_attr(value)
            else:
                tmp_ret[key] = tmp_attr()
        if not force_dict:
            if len(tmp_ret) == 1:
                tmp_ret = tmp_ret.popitem()[1]
        return tmp_ret

    def sub(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'sub', value=value, force_dict=force_dict)

    def add(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'add', value=value, force_dict=force_dict)

    def mult(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'mult', value=value, force_dict=force_dict)

    def div(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'div', value=value, force_dict=force_dict)

    def set(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'set', value=value, force_dict=force_dict)

    def clear(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'clear', value=value, force_dict=force_dict)

    def set_max(self, keys, value=None, force_dict=False):
        return self._set_counter_attr(keys, 'set_max', value=value, force_dict=force_dict)

    __call__ = add

    # *****************************************************************************
    # standard python magic methods
    # *****************************************************************************

    def __len__(self):
        return self.counter_count

    def __repr__(self):
        return 'NamedCounter: %s objects' % len(self)

    def __str__(self):
        return self.report()

    def __bool__(self):
        return bool(self.counters)
