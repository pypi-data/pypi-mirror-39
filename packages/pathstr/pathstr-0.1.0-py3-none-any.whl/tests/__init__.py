from unittest import TestCase

from pathstr import Path


class PathTests(TestCase):

    def test_build_from_single_string(self):
        path = Path('path/to/nothing')

        self.assertEqual(path.segments, ('path', 'to', 'nothing'))

    def test_build_from_multi_string(self):
        path = Path('path', 'to', 'nothing')

        self.assertEqual(path.segments, ('path', 'to', 'nothing'))

    def test_build_from_single_path(self):
        path = Path('path', 'to', 'nothing')

        path_final = Path(path)

        self.assertEqual(path_final.segments, ('path', 'to', 'nothing'))

    def test_build_from_multi_path(self):
        path_1 = Path('path', 'to')
        path_2 = Path('nothing')

        path_final = Path(path_1, path_2)

        self.assertEqual(path_final.segments, ('path', 'to', 'nothing'))

    def test_build_from_multi_mixed_1(self):
        path = Path('path', 'to')

        path_final = Path(path, 'nothing')

        self.assertEqual(path_final.segments, ('path', 'to', 'nothing'))

    def test_build_from_multi_mixed_2(self):
        path = Path('nothing')

        path_final = Path('path', 'to', path)

        self.assertEqual(path_final.segments, ('path', 'to', 'nothing'))

    def test_build_exception(self):
        with self.assertRaises(ValueError):
            Path(3)

    def test_to_string(self):
        path = Path('path', 'to', 'nothing')

        self.assertEqual(str(path), 'path/to/nothing')

    def test_length(self):
        path = Path('path', 'to', 'nothing')

        self.assertEqual(len(path), 3)

    def test_equal(self):
        self.assertEqual(Path('path/to/nothing'), Path('path', 'to', 'nothing'))

    def test_equal_string(self):
        self.assertEqual('path/to/nothing', Path('path', 'to', 'nothing'))

    def test_not_equal_integer(self):
        self.assertNotEqual(Path('path', 'to', 'nothing'), 3)

    def test_in(self):
        self.assertIn(Path('path/to/nothing'), Path('path', 'to'))

    def test_in_string(self):
        self.assertIn('path/to/nothing', Path('path', 'to'))

    def test_in_integer(self):
        self.assertNotIn(3, Path('path', 'to'))

    def test_startswith(self):
        self.assertTrue(Path('path/to/nothing').startswith(Path('path', 'to')))

    def test_startswith_string(self):
        self.assertTrue(Path('path/to/nothing').startswith('path/to'))

    def test_endswith(self):
        self.assertTrue(Path('path/to/nothing').endswith(Path('to', 'nothing')))

    def test_endswith_string(self):
        self.assertTrue(Path('path/to/nothing').endswith('to/nothing'))

    def _test_push_method_single_string(self, method, result):
        path_1 = Path('path', 'to')

        path_final = getattr(path_1, method)('nothing')

        self.assertEqual(path_final.segments, result)

        # Immutability

        self.assertNotEqual(id(path_1), id(path_final))

    def _test_push_method_multi_string(self, method, result):
        path_1 = Path('path')

        path_final = getattr(path_1, method)('to', 'nothing')

        self.assertEqual(path_final.segments, result)

        # Immutability

        self.assertNotEqual(id(path_1), id(path_final))

    def _test_push_method_single_path(self, method, result):
        path_1 = Path('path', 'to')
        path_final = getattr(path_1, method)(Path('nothing'))

        self.assertEqual(path_final.segments, result)

        # Immutability

        self.assertNotEqual(id(path_1), id(path_final))

    def _test_push_method_multi_path(self, method, result):
        path_1 = Path('path')

        path_final = getattr(path_1, method)(Path('to'), Path('nothing'))

        self.assertEqual(path_final.segments, result)

        # Immutability

        self.assertNotEqual(id(path_1), id(path_final))

    def _test_push_method_multi_mixed_1(self, method, result):
        path_1 = Path('path')

        path_final = getattr(path_1, method)(Path('to'), 'nothing')

        self.assertEqual(path_final.segments, result)

        # Immutability

        self.assertNotEqual(id(path_1), id(path_final))

    def _test_push_method_multi_mixed_2(self, method, result):
        path_1 = Path()

        path_final = getattr(path_1, method)('path', Path('to'), 'nothing')

        self.assertEqual(path_final.segments, result)

        # Immutability

        self.assertNotEqual(id(path_1), id(path_final))

    def _test_push_method_invalid_value(self, method):
        path = Path('path')

        with self.assertRaises(ValueError):
            getattr(path, method)(3)

    def test_rpush_single_string(self):
        self._test_push_method_single_string(method='rpush',
                                             result=('path', 'to', 'nothing'))

    def test_rpush_multi_string(self):
        self._test_push_method_multi_string(method='rpush',
                                            result=('path', 'to', 'nothing'))

    def test_rpush_single_path(self):
        self._test_push_method_single_path(method='rpush',
                                           result=('path', 'to', 'nothing'))

    def test_rpush_multi_path(self):
        self._test_push_method_multi_path(method='rpush',
                                          result=('path', 'to', 'nothing'))

    def test_rpush_multi_mixed_1(self):
        self._test_push_method_multi_mixed_1(method='rpush',
                                             result=('path', 'to', 'nothing'))

    def test_rpush_multi_mixed_2(self):
        self._test_push_method_multi_mixed_2(method='rpush',
                                             result=('path', 'to', 'nothing'))

    def test_rpush_invalid_value(self):
        self._test_push_method_invalid_value(method='rpush')

    def test_lpush_single_string(self):
        self._test_push_method_single_string(method='lpush',
                                             result=('nothing', 'path', 'to'))

    def test_lpush_multi_string(self):
        self._test_push_method_multi_string(method='lpush',
                                            result=('to', 'nothing', 'path'))

    def test_lpush_single_path(self):
        self._test_push_method_single_path(method='lpush',
                                           result=('nothing', 'path', 'to'))

    def test_lpush_multi_path(self):
        self._test_push_method_multi_path(method='lpush',
                                          result=('to', 'nothing', 'path'))

    def test_lpush_multi_mixed_1(self):
        self._test_push_method_multi_mixed_1(method='lpush',
                                             result=('to', 'nothing', 'path'))

    def test_lpush_multi_mixed_2(self):
        self._test_push_method_multi_mixed_2(method='lpush',
                                             result=('path', 'to', 'nothing'))

    def test_lpush_invalid_value(self):
        self._test_push_method_invalid_value(method='rpush')

    def _test_pop_method(self, method, result_1, result_2):
        path = Path('path/to/nothing')

        path_1, path_2 = getattr(path, method)(2)

        self.assertEqual(path_1.segments, result_1)
        self.assertEqual(path_2.segments, result_2)

        # Immutability

        self.assertNotEqual(id(path), id(path_1))
        self.assertNotEqual(id(path), id(path_2))

    def _test_pop_method_lower_0(self, method, result_1, result_2):
        path = Path('path/to/nothing')

        path_1, path_2 = getattr(path, method)(-2)

        self.assertEqual(path_1.segments, result_1)
        self.assertEqual(path_2.segments, result_2)

    def _test_pop_method_greater_length(self, method, result_1, result_2):
        path = Path('path/to/nothing')

        path_1, path_2 = getattr(path, method)(23)

        self.assertEqual(path_1.segments, result_1)
        self.assertEqual(path_2.segments, result_2)

    def _test_pop_method_invalid_value(self, method):
        path = Path('path/to/nothing')

        with self.assertRaises(ValueError):
            getattr(path, method)('error')

    def test_rpop(self):
        self._test_pop_method(method='rpop',
                              result_1=('path',),
                              result_2=('to', 'nothing'))

    def test_rpop_lower_0(self):
        self._test_pop_method_lower_0(method='rpop',
                                      result_1=('path', 'to', 'nothing'),
                                      result_2=())

    def test_rpop_greater_length(self):
        self._test_pop_method_greater_length(method='rpop',
                                             result_1=(),
                                             result_2=('path', 'to', 'nothing'))

    def test_rpop_invalid_value(self):
        self._test_pop_method_invalid_value(method='rpop')

    def test_lpop(self):
        self._test_pop_method(method='lpop',
                              result_1=('path', 'to'),
                              result_2=('nothing',))

    def test_lpop_lower_0(self):
        self._test_pop_method_lower_0(method='lpop',
                                      result_1=(),
                                      result_2=('path', 'to', 'nothing'))

    def test_lpop_greater_length(self):
        self._test_pop_method_greater_length(method='lpop',
                                             result_1=('path', 'to', 'nothing'),
                                             result_2=())

    def test_lpop_invalid_value(self):
        self._test_pop_method_invalid_value(method='lpop')

    def test_iter_parents(self):
        results = [
            Path('path'),
            Path('path/to'),
            Path('path/to/nothing')
        ]

        for idx, result in enumerate(Path('path/to/nothing').iter_parents()):
            self.assertEqual(result, results[idx])

    def test_iter(self):
        results = [
            Path('path'),
            Path('path/to'),
            Path('path/to/nothing')
        ]

        for idx, result in enumerate(Path('path/to/nothing')):
            self.assertEqual(result, results[idx])

    def test_add(self):
        self.assertEqual(Path('path') + Path('to') + Path('nothing'),
                         Path('path/to/nothing'))

    def test_add_string(self):
        self.assertEqual(Path('path') + 'to/nothing',
                         Path('path/to/nothing'))

    def test_add_string_inv(self):
        self.assertEqual('path' + Path('to/nothing'),
                         Path('path/to/nothing'))

    def test_add_error_left(self):

        with self.assertRaises(ValueError):
            3 + Path('to/nothing')

    def test_add_error_right(self):

        with self.assertRaises(ValueError):
            Path('to/nothing') + 3

    def test_sub(self):
        self.assertEqual(Path('path/to/nothing') - Path('to/nothing'),
                         Path('path'))

    def test_sub_string(self):
        self.assertEqual(Path('path/to/nothing') - 'to/nothing',
                         Path('path'))

    def test_sub_string_inv(self):
        self.assertEqual('path/to/nothing' - Path('to/nothing'),
                         Path('path'))

    def test_sub_string_not_endswith(self):
        with self.assertRaises(ValueError):
            'path/to/nothing' - Path('other/to/nothing')

    def test_sub_error_left(self):

        with self.assertRaises(ValueError):
            3 - Path('to/nothing')

    def test_sub_error_right(self):

        with self.assertRaises(ValueError):
            Path('to/nothing') - 3

    def test_lshift(self):
        self.assertEqual(Path('path/to/nothing') << 2,
                         Path('path'))

    def test_rshift(self):
        self.assertEqual(Path('path/to/nothing') >> 2,
                         Path('nothing'))

    def test_getitem_index(self):
        self.assertEqual(Path('path/to/nothing')[2],
                         Path('nothing'))

    def test_getitem_slice(self):
        self.assertEqual(Path('path/to/nothing')[1:],
                         Path('to/nothing'))

    def test_reversed(self):
        self.assertEqual(reversed(Path('path/to/nothing')),
                         Path('nothing/to/path'))

    def test_common_parent_equals(self):
        self.assertEqual(Path('path/to/nothing').common_parent(Path('path/to/nothing')),
                         Path('path/to/nothing'))

    def test_common_parent_contains(self):
        self.assertEqual(Path('path/to').common_parent(Path('path/to/nothing')),
                         Path('path/to'))

    def test_common_parent_contains_inv(self):
        self.assertEqual(Path('path/to/nothing').common_parent(Path('path/to')),
                         Path('path/to'))

    def test_common_parent_not_equals(self):
        self.assertEqual(Path('path/to/nothing').common_parent(Path('path/to/something')),
                         Path('path/to'))

    def test_common_parent_parent(self):
        self.assertEqual(Path('path/to').common_parent(Path('path/to/something')),
                         Path('path/to'))

    def test_common_parent_empty_parent(self):
        self.assertEqual(Path('path/to/nothing').common_parent(Path('other/path/to/something')),
                         Path())

    def test_common_parent_empty_parent_right(self):
        self.assertEqual(Path('other/path/to/nothing').common_parent(Path('path/to/something')),
                         Path())

    def test_common_parent_empty_path(self):
        self.assertEqual(Path().common_parent(Path('other/path/to/something')),
                         Path())

    def test_common_parent_empty_path_right(self):
        self.assertEqual(Path('other/path/to/something').common_parent(Path()),
                         Path())

    def test_common_parent_both_empty_path(self):
        self.assertEqual(Path().common_parent(Path()),
                         Path())
