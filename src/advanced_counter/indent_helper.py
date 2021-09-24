from src.advanced_counter.adv_counter import AdvCounter
from src.advanced_counter.helpers import _UNSET, not_none

def indent_text(text_in, *args, indent=0, indent_size=0, char=' ', ind_first_line=True, sep='\n', defer=False):
    """
    A helper function to indent text strings.

    :param text: The text to be indented
    :param args:  If args are passed, this will be combined into the text string using the "%" formatting approach.
    :param ind_first_line:  If False, the first line of the text will not be indented.
    :param sep: If None, the text lines will be returned as a list (for further processing)
    :param indent: The number of indents
    :param indent_size: The number of characters per indent
    :param char: The character used to indent the text
    :param defer: If True, this will return a DeferredIndent object instead of a string (or list).
    :return:
    """
    if defer:
        return DeferredIndent(
            text_in,
            *args,
            indent=indent,
            indent_size=indent_size,
            char=char,
            ind_first_line=ind_first_line,
            sep=sep,
        )

    if isinstance(text_in, (list, tuple)):
        text_in = '\n'.join(text_in)

    text_in = str(text_in)
    if args:
        text_in = text_in % args

    text_in = text_in.splitlines(keepends=False)

    indent_text = char * indent * indent_size

    for index, line in enumerate(text_in):
        if index == 0:
            if ind_first_line:
                text_in[index] = indent_text + line
        else:
            text_in[index] = indent_text + line
    if sep is not None:
        text_in = sep.join(text_in)
    return text_in


class DeferredIndent(object):
    """
    This is a helper function to allow deferred processing for things like logging where you may not want to
    process every line immediately (or at all).
    """

    def __init__(self, text_in, *args, indent=0, indent_size=0, char=' ', ind_first_line=True, sep='\n'):
        self.text = text_in
        self.args = args
        self.indent = indent
        self.indent_size = indent_size
        self.char = char
        self.ind_first_line = ind_first_line
        self.sep = sep

    def __str__(self):
        return indent_text(self.text, *self.args, indent=self.indent, indent_size=self.indent_size, char=self.char,
                           ind_first_line=self.ind_first_line, sep=self.sep)


class IndentHelper(AdvCounter):
    """
    This helper class provides a changable indent level that can be used to create indents for for output files
    such as a log.

    This is based on the AdvCounter object and shares much of the same math approaches.

    The main difference is that the main math methods (add/sub/mult/div/set) can be chained.  In other
    words, you can do something like the following:

    >>> ih = IndentHelper()
    >>> ih.add(3).sub(3).set(29)
    IndentHelper(29)

    """
    math_return = 'self'
    def __init__(self, initial_indent=0, spaces=4, max_size=20, char=' ', **kwargs):
        self.char = char
        self.spaces = spaces
        self.names = kwargs.copy()
        self.contexts = []
        self.index_memory = []
        super(IndentHelper, self).__init__(value=initial_indent, max_counter=max_size, min_counter=0)

    def _get_increment(self, value=None, force=False, operation='add'):
        if isinstance(value, str):
            value = self.names[value]
        elif value is None:
            value = 1
        return value

    def __add__(self, other):
        if isinstance(other, str):
            return str(self) + other
        return super(IndentHelper, self).__add__(other)

    def set(self, other=None, ret=math_return):
        """
        You can set the current indent level to a specified level, or if you pass a string you can set the
        current level to the memorized level.
        :param other:
        :param ret:
        :return:
        """
        return self._do_math(other, 'set', ret=ret)

    def push(self, name=None, size=None):
        """
        Allows setting a memorized indent level, or if no size is passed, will remember the current indent level.
        :param name: if None, this will save the current indent (or size) to a queue to be popped later
        :param size:
        :return:
        """
        size = size or self.value
        if name is None:
            self.index_memory.append(size)
        else:
            self.names[name] = size
        return self

    def pop(self, name=None, set=True):
        """
        Will remove the designated memorized indent level and set the current level to it.
        :param name: If None, will pop the level from the queue, if no levels are in the queue, nothing will happen.
        :param set: if False, the designated memory will be removed, but the current level will not be changed.
        :return:
        """
        if name is None:
            if self.index_memory:
                size = self.index_memory.pop()
                self.set(size)
        else:
            if set:
                self.set(name)
            del self.names[name]
        return self

    def delete(self, name):
        del self.names[name]
        return self

    def clear(self):
        self.names.clear()
        super(IndentHelper, self).clear()

    def print(self, *text_in):
        print(self.i, *text_in)

    def indent_text(self, text, *args, ind_first_line=True, sep='\n', indent=None, indent_size=None, char=None, defer=False):
        """
        Will return the text passed with each line indented by the current indent level.

        :param text: The text to be indented
        :param args:  If args are passed, this will be combined into the text string using the "%" formatting approach.
        :param ind_first_line:  If False, the first line of the text will not be indented.
        :param sep: If None, the text lines will be returned as a list (for further processing)
        :param indent: This can override the current indent level
        :param indent_size: This can override the defined indent size
        :param char: This can override the defined indent character
        :param defer: If True, this will return a DeferredIndent object instead of a string (or list).
        :return:
        """
        indent_size = not_none(indent_size, self.spaces)
        indent = not_none(indent, self.value)
        char = not_none(char, self.char)

        return indent_text(text,
                           *args,
                           ind_first_line=ind_first_line,
                           indent=indent,
                           indent_size=indent_size,
                           char=char,
                           sep=sep,
                           defer=defer
                           )

    @property
    def indent(self):
        """
        returns the indent level.
        :return:
        """
        return self.value

    def ind(self, indent=None, size=None, char=None):
        char = char or self.char
        indent = indent or self.value
        size = size or self.spaces
        return char * size * indent

    @property
    def i(self):
        """
        returns the indent string.
        :return:
        """
        return self.char * self.spaces * self.value

    def __str__(self):
        return self.i

    def __enter__(self):
        self.contexts.append(self.value)
        self.add()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set(self.contexts.pop())
        return False

    def __call__(self, add=_UNSET, ret=math_return, **kwargs):
        if isinstance(add, str):
            kwargs['set'] = add
        return super(IndentHelper, self).__call__(add=add, ret=ret, **kwargs)

    def __contains__(self, item):
        return item in self.names

    def __repr__(self):
        return 'IndentHelper: size: %s, saves: %r' % (self.value, self.names)

    def __len__(self):
        return self.spaces * self.value
