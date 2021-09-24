__author__ = 'dstrohl'

from unittest import TestCase
from src.advanced_counter.indent_helper import IndentHelper


class TestIndentHelper(TestCase):

    def test_normal(self):
        ih = IndentHelper()
        self.assertEqual('', ih.i)

    def test_add(self):
        ih = IndentHelper()
        ih.add(1)
        self.assertEqual('    ', ih.i)
        self.assertEqual('            ', ih(2).i)

    def test_sub(self):
        ih = IndentHelper(4)
        ih.sub(1)
        self.assertEqual(3, ih.indent)
        self.assertEqual(3, int(ih))
        self.assertEqual('            ', str(ih))

    def test_iadd(self):
        ih = IndentHelper()
        ih += 1
        self.assertEqual('    ', ih.i)
        self.assertEqual('            ', ih(2).i)

    def test_isub(self):
        ih = IndentHelper(4)
        ih -= 1
        self.assertEqual(3, ih.indent)
        self.assertEqual(3, int(ih))
        self.assertEqual('            ', str(ih))

    def test_chain(self):
        ih = IndentHelper()
        ih(10).add(5).sub(3)
        self.assertEqual(ih.indent, 12)
        ih.set(10).add(5)
        self.assertEqual(ih.indent, 15)

    def test_set(self):
        ih = IndentHelper()
        ih(10)
        self.assertEqual(10, ih.indent)
        self.assertEqual(10, ih)
        self.assertEqual(5, ih.set(5).indent)
        self.assertEqual(5, ih)
        ih(set=2)
        self.assertEqual('        ', str(ih))

    def test_context(self):
        ih = IndentHelper(4)
        with ih:
            self.assertEqual(5, ih.indent)
        self.assertEqual(4, ih.indent)

    def test_multi_context(self):
        ih = IndentHelper(4)
        with ih:
            self.assertEqual(5, ih.indent)
            ih.set(10)
            self.assertEqual(10, ih.indent)
            with ih:
                self.assertEqual(11, ih.indent)
            self.assertEqual(10, ih.indent)
            ih.set(10000)
            self.assertEqual(20, ih.indent)
            with ih:
                self.assertEqual(20, ih.indent)
                ih.set(1)
                with ih:
                    self.assertEqual(2, ih.indent)
                self.assertEqual(1, ih.indent)

            self.assertEqual(20, ih.indent)

        self.assertEqual(4, ih.indent)

    def test_context_fail(self):
        ih = IndentHelper(4)
        with self.assertRaises(AttributeError):
            with ih:
                self.assertEqual(5, ih.indent)
                raise AttributeError('test')
        self.assertEqual(4, ih.indent)

    def test_set_name(self):
        ih = IndentHelper(4)
        self.assertEqual(4, ih)
        ih.push('foo')
        self.assertEqual(4, ih)
        ih += 2
        self.assertEqual(6, ih)
        ih.set('foo')
        self.assertEqual(4, ih)
        self.assertIn('foo', ih)

    def test_pop_name(self):
        ih = IndentHelper(4)
        self.assertEqual(4, ih)
        ih.push('foo')
        self.assertEqual(4, ih)
        ih += 2
        self.assertEqual(6, ih)
        ih.pop('foo')
        self.assertEqual(4, ih)
        self.assertNotIn('foo', ih)

    def test_del_name(self):
        ih = IndentHelper(4, foo=6)
        self.assertEqual(4, ih)
        ih.set('foo')
        self.assertEqual(6, ih)
        self.assertIn('foo', ih)
        ih -= 10
        self.assertEqual(0, ih)
        ih.delete('foo')
        self.assertEqual(0, ih)
        self.assertNotIn('foo', ih)

    def test_clear(self):
        ih = IndentHelper(4, foo=6)
        self.assertEqual(4, ih)
        self.assertIn('foo', ih)
        ih.clear()
        self.assertEqual(0, ih)
        self.assertNotIn('foo', ih)

    def test_indent_char(self):
        ih = IndentHelper(char='.')
        ih()
        self.assertEqual(ih, 1)
        self.assertEqual(str(ih), '....')

    def test_add_str(self):
        ih = IndentHelper(1, foo=6)
        self.assertEqual(str(ih), '    ')
        tmp_ret = ih + 'foobar'
        self.assertEqual(tmp_ret, '    foobar')

    def test_textwrap_no_first_line(self):
        ih = IndentHelper(1, foo=6)
        self.assertEqual(str(ih), '    ')
        tmp_ret = ih.indent_text('foobar\nblah')
        self.assertEqual(tmp_ret, '    foobar\n    blah')

    def test_textwrap_with_first_line(self):
        ih = IndentHelper(1, foo=6)
        self.assertEqual(str(ih), '    ')
        tmp_ret = ih.indent_text('foobar\nblah', ind_first_line=False)
        self.assertEqual(tmp_ret, 'foobar\n    blah')
