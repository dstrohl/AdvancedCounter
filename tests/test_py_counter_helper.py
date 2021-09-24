import decimal
from unittest import TestCase
from src.advanced_counter.adv_counter import NamedCounter, AdvCounter, \
    minmax, IncrementByDict, IncrementByValue, IncrementByList,\
    INCREMENT_LIST_ON_INDEX_RESET, \
    INCREMENT_LIST_ON_INDEX_NOTHING, INCREMENT_LIST_ON_INDEX_SET

from copy import copy

"""
ns_1 = ['name1', 3]
ns_2 = ['name2', 1]
ns_3 = ['name3', 0]
ns_4 = ['name4', 10]
na1 = 'name1'
na2 = 'name2'
na3 = 'name3'
na4 = 'name4'
nv1 = 3
nv2 = 1
nv3 = 0
nv4 = 10
nso_1 = [na1, nv1]
nso_2 = [na2, nv2]
nso_3 = [na3, nv3]
nso_4 = [na4, nv4]
n_defs = dict(
    n1=[na1, nv1],
    n2=[na2, nv2],
    n3=[na3, nv3],
    n4=[na4, nv4],
)

n_orders = dict(
    value=['n3', 'n2', 'n1', 'n4'],
    name=['n1', 'n2', 'n3', 'n4'],
    none=['n1', 'n3', 'n2', 'n4'],
)
"""

INC_BY_DICT_TEST = {
    't1': 1,
    't2': 2,
    't10': 10,
}

INC_BY_LIST_TEST = [1, 2, 10, 20]

class TestIncrementObjs(TestCase):

    def test_base(self):
        ti = IncrementByValue()
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(20), 20)

    def test_base_error(self):
        with self.assertRaises(TypeError):
            ti = IncrementByValue('foobar')

    def test_base_no_scan(self):
        ti = IncrementByValue('foobar', no_scan=True)
        self.assertEqual(ti(), 'foobar')
        self.assertEqual(ti(20), 20)

    def test_by_dict(self):
        ti = IncrementByDict(INC_BY_DICT_TEST)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti('t10'), 10)
        self.assertEqual(ti('foobar'), 'foobar')
        self.assertEqual(ti(222), 222)

    def test_by_dict_no_default(self):
        ti = IncrementByDict(INC_BY_DICT_TEST, default_value=None)
        self.assertEqual(ti('t10'), 10)
        with self.assertRaises(KeyError, msg=ti.dump()):
           self.assertEqual(ti(), 1, ti.dump())
        self.assertEqual(ti(222), 222)

    def test_by_dict_no_invalid(self):
        ti = IncrementByDict(INC_BY_DICT_TEST, invalid_value=None)
        self.assertEqual(ti('t10'), 10)
        self.assertEqual(ti(), 1, ti.dump())

        with self.assertRaises(KeyError):
            ti(222)

    def test_by_list_default(self):
        ti = IncrementByList(INC_BY_LIST_TEST, default_value=100)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(222), 100)

    def test_by_list_no_default_error(self):
        ti = IncrementByList(INC_BY_LIST_TEST)
        self.assertEqual(ti(1), 2)
        with self.assertRaises(IndexError):
           self.assertEqual(ti(200), 1)

    def test_by_list_standard(self):
        ti = IncrementByList(INC_BY_LIST_TEST)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(), 2)
        self.assertEqual(ti(), 10)
        self.assertEqual(ti(), 20)
        self.assertEqual(ti(), 20)
        with self.assertRaises(IndexError):
            ti(22)
        self.assertEqual(ti(1), 2)
        self.assertEqual(ti(2), 10)
        self.assertEqual(ti(0), 1)

    def test_by_list_standard_default(self):
        ti = IncrementByList(INC_BY_LIST_TEST, default_value=15)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(1), 2)
        self.assertEqual(ti(2), 10)
        self.assertEqual(ti(0), 1)
        self.assertEqual(ti(33), 15)

    def test_by_list_increment(self):
        ti = IncrementByList(INC_BY_LIST_TEST)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(3), 20)
        self.assertEqual(ti(), 10)

    def test_by_list_reset(self):
        ti = IncrementByList(INC_BY_LIST_TEST, increment_on_index=INCREMENT_LIST_ON_INDEX_RESET)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(), 2)
        self.assertEqual(ti(3), 20)
        self.assertEqual(ti(), 1)

    def test_by_list_set(self):
        ti = IncrementByList(INC_BY_LIST_TEST, increment_on_index=INCREMENT_LIST_ON_INDEX_SET)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(), 2)
        self.assertEqual(ti(0), 1)
        self.assertEqual(ti(), 2)

    def test_by_list_nothing(self):
        ti = IncrementByList(INC_BY_LIST_TEST, increment_on_index=INCREMENT_LIST_ON_INDEX_NOTHING)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(), 2)
        self.assertEqual(ti(0), 1)
        self.assertEqual(ti(), 10)

    def test_by_list_repeat(self):
        ti = IncrementByList(INC_BY_LIST_TEST, repeat_all=True)
        self.assertEqual(ti(), 1)
        self.assertEqual(ti(), 2)
        self.assertEqual(ti(), 10)
        self.assertEqual(ti(), 20)
        print(ti.dump())
        self.assertEqual(ti(), 1, ti.dump())
        self.assertEqual(ti(), 2)


class TestMinMax(TestCase):
    def test_minmax(self):
        TESTS = [
            # (test_num, value, min, max, rollover, exp_val),

            # no min/max
            (1, 100, None, None, False, 100),
            # no min
            (10, 100, None, 100, False, 100),
            (11, 101, None, 100, False, 100),
            (12, -10, None, 100, False, -10),
            # no max
            (20, 100, 10, None, False, 100),
            (21, 10, 10, None, False, 10),
            (22, 9, 10, None, False, 10),
            (23, -100, 10, None, False, 10),
            # min max no rollover
            (30, 100, 10, 100, False, 100),
            (31, 101, 10, 100, False, 100),
            (32, 10, 10, 100, False, 10),
            (33, 1, 10, 100, False, 10),
            (34, 40, 10, 100, False, 40),
            # min max rollover no need
            (40, 100, 10, 100, True, 100),
            (41, 10, 10, 100, True, 10),
            (42, 40, 10, 100, True, 40),
            # minmax rollover min
            (50, 9, 10, 99, True, 99),
            (51, 0, 10, 99, True, 90),
            (52, -10, 0, 99, True, 90),
            (53, -210, 0, 99, True, 90),
            (54, -10, 1, 100, True, 90),
            (55, -210, 1, 100, True, 90),
            # minmax rollover max
            (60, 101, 10, 99, True, 11),
            (61, 110, 10, 99, True, 20),
            (62, 101, 0, 99, True, 1),
            (63, 314, 0, 99, True, 14),
            (64, 114, 1, 100, True, 14),
            (65, 314, 1, 100, True, 14),
        ]

        for test_num, value, min_val, max_val, rollover, exp_val in TESTS:
            with self.subTest(test_num=test_num):
                act_val = minmax(value, min_val, max_val, rollover=rollover)
                self.assertEqual(act_val, exp_val)


class TestCounterObj(TestCase):

    def test_add(self):
        tc = AdvCounter()
        self.assertEqual(0, int(tc))
        tc += 10
        self.assertEqual(10, int(tc))
        tc.add()
        self.assertEqual(11, int(tc))
        tc()
        self.assertEqual(12, int(tc))
        tc(3)
        self.assertEqual(15, int(tc))

    def test_add_perc(self):
        tc = AdvCounter(10, min_counter=1, max_counter=100)
        self.assertEqual(10, int(tc))
        tc += '50%'
        self.assertEqual(60, int(tc))

    def test_sub_perc(self):
        tc = AdvCounter(90, min_counter=1, max_counter=100)
        self.assertEqual(90, int(tc))
        tc -= '50%'
        self.assertEqual(40, int(tc))

    def test_mult_perc(self):
        tc = AdvCounter(10, min_counter=1, max_counter=100)
        self.assertEqual(10, int(tc))
        tc *= '50%'
        self.assertEqual(5, int(tc))

    def test_div_perc(self):
        tc = AdvCounter(10, min_counter=1, max_counter=100)
        self.assertEqual(10, int(tc))
        tc /= '50%'
        self.assertEqual(20, int(tc))

    def test_set_perc(self):
        tc = AdvCounter(10, min_counter=1, max_counter=100)
        self.assertEqual(10, int(tc))
        tc.set('50%')
        self.assertEqual(50, int(tc))

    def test_sub(self):
        tc = AdvCounter(value=20)
        self.assertEqual(20, int(tc))
        tc -= 10
        self.assertEqual(10, int(tc))
        tc.sub()
        self.assertEqual(9, int(tc))
        tc(-11)
        self.assertEqual(-2, int(tc))
        tc(-10)
        self.assertEqual(-12, int(tc))

    def test_set(self):
        tc = AdvCounter(value=20)
        self.assertEqual(20, int(tc))
        tc.set(1)
        self.assertEqual(1, int(tc))
        tc.set(10)
        self.assertEqual(10, int(tc))

    def test_perc_no_max(self):
        tc = AdvCounter(value=20)
        self.assertEqual(20, int(tc))
        with self.assertRaises(AttributeError):
            f = tc.perc

    def test_perc_w_max(self):
        tc = AdvCounter(value=20, min_counter=0, max_counter=100)
        self.assertEqual(20, int(tc))
        self.assertEqual(decimal.Decimal('0.200000000000000011102230246251565404236316680908203125'), tc.perc)

    def test_perc_w_min_max(self):
        tc = AdvCounter(value=30, min_counter=10, max_counter=110)
        self.assertEqual(30, int(tc))
        self.assertAlmostEqual(0.20, tc.perc, 2)
        tc += 30
        self.assertEqual(60, int(tc))
        self.assertAlmostEqual(0.50, tc.perc, 2)

    def test_min(self):
        tc = AdvCounter(value=20, min_counter=5)
        self.assertEqual(20, int(tc))
        tc -= 10
        self.assertEqual(10, int(tc))
        tc.sub(5)
        self.assertEqual(5, int(tc))
        tc(-1)
        self.assertEqual(5, int(tc))
        tc(-10)
        self.assertEqual(5, int(tc))
        tc.set(1)
        self.assertEqual(5, int(tc))

    def test_max(self):
        tc = AdvCounter(max_counter=20)
        self.assertEqual(0, int(tc))
        tc += 10
        self.assertEqual(10, int(tc))
        tc.add(20)
        self.assertEqual(20, int(tc))
        tc()
        self.assertEqual(20, int(tc))
        tc(2)
        self.assertEqual(20, int(tc))
        tc.set(23)
        self.assertEqual(20, int(tc))

    def test_minmax(self):
        tc = AdvCounter(value=20, min_counter=5, max_counter=20)
        self.assertEqual(20, int(tc))
        tc -= 10
        self.assertEqual(10, int(tc))
        tc.sub(5)
        self.assertEqual(5, int(tc))
        tc(-1)
        self.assertEqual(5, int(tc))
        tc(-10)
        self.assertEqual(5, int(tc))
        tc.set(1)
        self.assertEqual(5, int(tc))

        tc.set(200)
        self.assertEqual(20, int(tc))
        tc.add(20)
        self.assertEqual(20, int(tc))
        tc()
        self.assertEqual(20, int(tc))
        tc(2)
        self.assertEqual(20, int(tc))
        tc.set(23)
        self.assertEqual(20, int(tc))

    def test_minmax_rollover(self):
        tc = AdvCounter(value=20, min_counter=5, max_counter=20, rollover=True)
        self.assertEqual(20, int(tc))
        tc -= 10
        self.assertEqual(10, int(tc))
        tc.sub(5)
        self.assertEqual(5, int(tc))
        tc(-1)
        self.assertEqual(20, int(tc))
        tc(-30)
        self.assertEqual(6, int(tc))
        tc.set(1)
        self.assertEqual(17, int(tc))
        tc += 10
        self.assertEqual(11, int(tc))
        tc += 10
        self.assertEqual(5, int(tc))

    def test_clear(self):
        tc = AdvCounter()
        self.assertEqual(0, int(tc))
        tc += 10
        self.assertEqual(10, int(tc))
        tc.add()
        self.assertEqual(11, int(tc))
        tc(-5)
        self.assertEqual(6, int(tc))
        self.assertEqual(tc.call_count, 3)
        tc.clear()

        self.assertEqual(tc.call_count, 0)

        tc(3)
        self.assertEqual(3, int(tc))
        tc -= 8
        self.assertEqual(-5, int(tc))

    def test_clear_2(self):
        tc = AdvCounter(10, min_counter=5)
        tc += 10
        self.assertEqual(20, int(tc))
        tc.clear()
        self.assertEqual(5, int(tc))

    def test_eq(self):
        tc = AdvCounter(value=10)
        self.assertTrue(tc > 5)
        self.assertTrue(tc >= 10)
        self.assertTrue(tc < 15)
        self.assertTrue(tc <= 10)
        self.assertTrue(tc == 10)
        self.assertTrue(tc != 100)

        self.assertFalse(tc > 15)
        self.assertFalse(tc >= 15)
        self.assertFalse(tc < 5)
        self.assertFalse(tc <= 5)
        self.assertFalse(tc == 100)
        self.assertFalse(tc != 10)

    def test_eq_to_ctr_obj(self):
        tc = AdvCounter(value=10)
        tc5 = AdvCounter(value=5)
        tc10 = AdvCounter(value=10)
        tc15 = AdvCounter(value=15)

        self.assertTrue(tc > tc5)
        self.assertTrue(tc >= tc10)
        self.assertTrue(tc < tc15)
        self.assertTrue(tc <= tc10)
        self.assertTrue(tc == tc10)
        self.assertTrue(tc != 100.0)

        self.assertFalse(tc > tc15)
        self.assertFalse(tc >= tc15)
        self.assertFalse(tc < tc5)
        self.assertFalse(tc <= tc5)
        self.assertFalse(tc == 100.0)
        self.assertFalse(tc != tc10)

    def test_bool(self):
        tc = AdvCounter()
        self.assertFalse(tc)
        tc += 1
        self.assertTrue(tc)
        tc -= 1
        self.assertFalse(tc)

    def test_mult(self):
        tc = AdvCounter(value=1)
        self.assertEqual(1, int(tc))
        tc *= 10
        self.assertEqual(10, int(tc))
        tc.mult(2)
        self.assertEqual(20, int(tc))

    def test_div(self):
        tc = AdvCounter(value=10)
        self.assertEqual(10, int(tc))
        tc /= 2
        self.assertEqual(5, int(tc))

        tc.div(2)
        self.assertEqual(2, int(tc))

    def test_copy(self):
        tc = AdvCounter(value=10)
        tc2 = tc.copy()
        tc3 = copy(tc)
        tc2 += 1
        tc3 += 4
        self.assertEqual(10, int(tc))
        self.assertEqual(11, int(tc2))
        self.assertEqual(14, int(tc3))

    def test_on_every_func(self):
        vals = []
        exp_vals = []
        def add_val(ctr):
            vals.append(int(ctr))

        def run_test(run_size, exp_out_count, max_counter=None, call_every=None, exp_countdown=None):
            vals.clear()
            exp_vals.clear()

            tmp_cur_val = 0
            ce = call_every or 100
            for r in range(exp_out_count):
                tmp_cur_val += ce
                exp_vals.append(tmp_cur_val)

            tc = AdvCounter(call_every_func=add_val, max_counter=max_counter, call_every=call_every)
            self.assertEqual(tc._call_every, exp_countdown)
            counter = 0
            countdown = exp_countdown
            for r in range(run_size):
                counter += 1
                tc()
                countdown -= 1
                if countdown == 0:
                    countdown = exp_countdown
                self.assertEqual(countdown, tc.call_countdown, 'iteration number: %s' % counter)
            self.assertEqual(counter, run_size)
            self.assertEqual(run_size, tc.call_count)
            self.assertEqual(run_size, len(tc))
            self.assertEqual(len(vals), exp_out_count, repr(vals))
            # self.assertEqual(exp_vals, vals)

        TESTS = [
            # (test_num, run_Size, exp_out_count, max_counter, call_every, exp_countdown),
            (10, 1000, 10, None, None, 100),
            (20, 10000, 10, 100000, None, 1000),
            (30, 4000, 40, 6000, 100, 100),
        ]
        for test_num, run_size, exp_out_count, max_counter, call_every, exp_countdown in TESTS:
            with self.subTest(test_num=test_num):
                run_test(run_size, exp_out_count, max_counter, call_every, exp_countdown)

    def test_increment_dict(self):
        tc = AdvCounter(increment_by=INC_BY_DICT_TEST)
        self.assertEqual(int(tc), 0)
        self.assertEqual(tc(), 1)
        self.assertEqual(tc(), 2)
        self.assertEqual(tc(), 3)
        self.assertEqual(tc('t1'), 4)
        self.assertEqual(tc('t2'), 6)
        self.assertEqual(tc('t10'), 16)


    def test_increment_list(self):
        tc = AdvCounter(increment_by=INC_BY_LIST_TEST)
        self.assertEqual(int(tc), 0)
        self.assertEqual(tc(), 1)
        self.assertEqual(tc(), 3)
        self.assertEqual(tc(), 13)
        self.assertEqual(tc(1), 15)
        self.assertEqual(tc(2), 25)
        self.assertEqual(tc(0), 26)

    def test_iter(self):
        tmp_ret = []
        exp_ret = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        tc = AdvCounter()
        for c, l in enumerate(tc):
            tmp_ret.append(l)
            if c == 14:
                break

        self.assertEqual(tmp_ret, exp_ret)

    def test_call(self):
        tc = AdvCounter(value=1)
        self.assertEqual(1, int(tc))
        tc()
        self.assertEqual(2, int(tc))
        tc(1)
        self.assertEqual(3, int(tc))
        tc(mult=2, add=1)
        self.assertEqual(7, int(tc))
        tc(set=10, add=3, mult=2)
        self.assertEqual(23, int(tc))


na1 = 'name1'
na2 = 'name2'
na3 = 'name3'
na4 = 'name4'
nv1 = 3
nv2 = 1
nv3 = 0
nv4 = 10
n_dict = {na1: nv1, na2: nv2, na3: nv3, na4: nv4}


class TestNamedCounter(TestCase):

    tc = NamedCounter()
    maxDiff = None

    def setUp(self):
        self.setup_tc()

    def setup_tc(self, **kwargs):
        tmp_kwargs = n_dict.copy()
        tmp_kwargs.update(kwargs)
        self.tc = NamedCounter(**tmp_kwargs)

    def check_tc(self, **kwargs):
        for key, value in kwargs.items():
            with self.subTest(key=key):
                self.assertEqual(value, self.tc[key].value)

    def test_no_args(self):
        tc = NamedCounter()
        self.assertFalse(tc)
        self.assertEqual(0, len(tc))

    def test_get_vals(self):
        self.assertEqual(self.tc.name1.value, 3)
        self.assertEqual(self.tc['name1'].value, 3)
        self.assertEqual(self.tc.get('name1').value, 3)

    def test_init_args(self):
        tc_obj = AdvCounter(3)
        tc = NamedCounter('t1', t3=tc_obj, t4=4, t5={'value': 5, 'max_counter': 10}, max_counter=30)
        self.assertTrue(tc)
        self.assertEqual(4, len(tc), msg=tc.report())
        self.assertEqual(0, tc.t1)
        self.assertEqual(3, tc['t3'])
        self.assertEqual(4, tc.get('t4'))
        self.assertEqual(5, tc.t5)
        self.assertEqual(30, tc.t1.max_counter, repr(tc.t1))
        self.assertEqual(None, tc.t3.max_counter, repr(tc.t3))
        self.assertEqual(30, tc.t4.max_counter, repr(tc.t4))
        self.assertEqual(10, tc.t5.max_counter, repr(tc.t5))

    def test_dupe_name(self):
        with self.assertRaises(AttributeError):
            self.tc.new(na1)

    def test_dupe_name_force(self):
        self.assertEqual(self.tc.get(na1), 3)
        self.tc.new(na1, value=10, overwrite=True)
        self.assertEqual(int(self.tc.name1), 10, msg='foobar: ' + repr(self.tc.name1))

    def test_bad_name(self):
        tc = NamedCounter('t1', 't2', locked=True)
        self.assertEqual(2, len(tc))
        with self.assertRaises(KeyError):
            test = tc['t3']
        with self.assertRaises(AttributeError):
            test = tc.t3

    def test_remove(self):
        tc = NamedCounter('t1', 't2', locked=False)
        self.assertEqual(2, len(tc))
        self.assertEqual(0, tc.t1)
        self.assertIn('t1', tc)
        self.assertIn('t2', tc)
        tc.remove('t1')
        self.assertEqual(1, len(tc))
        self.assertEqual(0, tc.t2)
        self.assertIn('t2', tc)
        self.assertNotIn('t1', tc)

    def test_remove_locked(self):
        tc = NamedCounter('t1', 't2')
        self.assertEqual(2, len(tc))
        self.assertEqual(0, tc.t1)
        self.assertIn('t1', tc)
        self.assertIn('t2', tc)
        tc.remove('t1')
        self.assertEqual(1, len(tc))
        self.assertEqual(0, tc.t2)
        self.assertIn('t2', tc)
        self.assertNotIn('t1', tc)

    def test_clear(self):
        tc = NamedCounter('t1', 't2')
        tc.t1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc))
        tc.clear('*')
        self.assertEqual([0, 0], list(tc))

    def test_clear_all(self):
        tc = NamedCounter('t1', 't2')
        tc.t1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc))
        tc.clear('*')
        self.assertEqual([0, 0], list(tc))
        self.assertEqual(2, len(tc))

    def test_keys(self):
        tc = NamedCounter('t1', 't2')
        tc.t1 += 10
        tc.t2 += 20
        self.assertEqual(['t1', 't2'], list(tc.keys()))

    def test_values(self):
        tc = NamedCounter('t1', 't2')
        tc.t1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc.values()))

    def test_call(self):
        tc = NamedCounter('t1', 't2')
        tc.t1 += 10
        tc.t2 += 20
        tc('t1', 5)
        self.assertEqual([15, 20], list(tc.values()))

    def test_str(self):
        tc = NamedCounter('test 1', 't2')
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc.values()))
        exp_out = 'test 1 : 10\n' \
                  '    t2 : 20'
        self.assertEqual(exp_out, str(tc))

    def test_reports(self):
        tc = NamedCounter('test 1', 't2')
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc.values()))
        exp_out = 'test 1 : 10\n' \
                  '    t2 : 20'
        self.assertEqual(exp_out, tc.report())

    def test_reports_perc(self):
        tc = NamedCounter('test 1', 't2', max_counter=50, min_counter=0)
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc.values()))
        exp_out = 'test 1 : 10 (20%)\n' \
                  '    t2 : 20 (40%)'
        self.assertEqual(exp_out, tc.report())

    def test_report_header(self):
        tc = NamedCounter('test 1', 't2', min_counter=1, max_counter=50)
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([11, 21], list(tc.values()), tc.report())
        exp_out = 'header-test 21 32\n' \
                  '    test 1 : 11 (20%)\n' \
                  '        t2 : 21 (41%)'
        self.assertEqual(exp_out, tc.report(header='header-test {t2.value} {sum}'))

    def test_report_justify_left(self):
        tc = NamedCounter('test 1', 't2', max_counter=50)
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc.values()))
        exp_out = 'header-test 20 30\n' \
                  '    test 1 : 10\n' \
                  '    t2     : 20\n' \
                  'footer-test 2'
        self.assertEqual(exp_out, tc.report(header='header-test {t2.value} {sum}', justify_name='<',
                                            footer='footer-test {num_counters}', line_indent=4))

    def test_report_justify_right(self):
        tc = NamedCounter('test 1', 't2', max_counter=50)
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20], list(tc.values()))
        exp_out = 'header-test 20 30\n' \
                  '    test 1 : 10\n' \
                  '        t2 : 20\n' \
                  'footer-test 2'
        self.assertEqual(exp_out, tc.report(header='header-test {t2.value} {sum}', justify_name='>',
                                            footer='footer-test {num_counters}', line_indent=4))

    def test_report_limit_counters(self):
        tc = NamedCounter('test 1', 't2', 't3', 't4', max_counter=50)
        tc.test_1 += 10
        tc.t2 += 20
        self.assertEqual([10, 20, 0, 0], list(tc.values()))
        exp_out = 'header-test 20 20\n' \
                  '    t3 : 0\n' \
                  '    t2 : 20\n' \
                  '    t4 : 0\n' \
                  'footer-test 3'
        self.assertEqual(exp_out, tc.report(header='header-test {t2.value} {sum}', justify_name='>',
                                            counters=['t3', 't2', 't4'],
                                            footer='footer-test {num_counters}', line_indent=4))

    def print_list_comp(self, expected, actual):
        tmp_ret = ['\n\nExpected:',
                   '---------']

        for x in expected:
            tmp_ret.append(repr(x))

        tmp_ret.append('\nActual:')
        tmp_ret.append('-------')

        for x in actual:
            tmp_ret.append(repr(x))

        return '\n'.join(tmp_ret)

    def test_contains(self):
        self.assertTrue('name1' in self.tc)
        self.assertFalse('name5' in self.tc)

    def test_locked_initial_with_names(self):
        tc = NamedCounter('test 1', 't2', 't3', 't4', max_counter=50)
        self.assertTrue(tc.locked)

        tc = NamedCounter()
        self.assertFalse(tc.locked)

    def test_non_slugified(self):
        tc = NamedCounter('1 test 1', 't2', 't3', 't4', max_counter=50)
        self.assertEqual(tc['1 test 1'].value, 0)

    def test_name_report(self):
        tc = NamedCounter('1 test 1', 't2', 't3', 't4', max_counter=50, name='my counters')
        exp_out = "my counters\n" \
        "    1 test 1 : 0\n" \
        "          t2 : 0\n" \
        "          t3 : 0\n" \
        "          t4 : 0"
        act_out = tc.report()
        self.assertEqual(exp_out, act_out)

    def test_reporting_description(self):
        tc = NamedCounter('t1', t5={'name': 'test2', 'description': 'this is a test', 'value': 5, 'max_counter': 10}, max_counter=30, name='my counters')
        exp_out = "my counters\n" \
        "       t1 : 0\n" \
        "    test2 : 5\n" \
        "        this is a test"
        act_out = tc.report()
        self.assertEqual(exp_out, act_out)


