import unittest

from vrypy.test.deep import bag, ignore, super_dict_of


class SomeObject:
    pass


class CompareTest(unittest.TestCase):
    def test_bag_eq(self):
        cases = [
            ([1, 2, 3], bag([2, 3, 1])),
            ((1, 2), bag((2, 1))),
            ({3: [2, 1]}, {3: bag([1, 2])}),
            ([1, 2, [4, 3]], [1, 2, bag([3, 4])]),
            ([], bag([])),
        ]
        self._check_eq(cases)

    def test_bag_neq(self):
        cases = [
            ([1, 2, 3], bag([1, 2, 2, 3])),
            ((1, 2), bag([1, 2])),
            ({1: [2, 3]}, {1: bag([3, 4])}),
        ]
        self._check_neq(cases)

    def test_ignore_eq(self):
        cases = [
            (1, ignore()),
            ("hi", ignore()),
            ({1: 2}, ignore()),
            ((1, 2), (1, ignore())),
            ([1, 2, 3, 4], [1, 2, ignore(), ignore()]),
            ({1: "hi"}, {1: ignore()}),
            ((1, [2]), (1, ignore())),
            ((1, SomeObject()), (1, ignore())),
        ]
        self._check_eq(cases)

    def test_ignore_neq(self):
        cases = [([1, 2, 3], [1, 2, 3, ignore()]), ({1: 2, 3: 4}, {1: ignore(), 3: 5})]
        self._check_neq(cases)

    def test_super_dict_of_eq(self):
        cases = [
            ({1: 2, 3: 4}, super_dict_of({1: 2})),
            ({}, super_dict_of({})),
            ({1: 2, 3: 4}, super_dict_of({})),
        ]
        self._check_eq(cases)

    def test_super_dict_of_neq(self):
        cases = [
            ({1: 2, 3: 4}, super_dict_of({1: 2, 4: 5})),
            ({}, super_dict_of({1: 2})),
            ("hi", super_dict_of({})),
        ]
        self._check_neq(cases)

    def _check_eq(self, cases):
        for case in cases:
            with self.subTest(case):
                self.assertEqual(*case)
                self.assertEqual(*reversed(case))
                self.assertTrue(case[0] == case[1])
                self.assertTrue(case[1] == case[0])

    def _check_neq(self, cases):
        for case in cases:
            with self.subTest(case):
                self.assertNotEqual(*case)
                self.assertNotEqual(*reversed(case))
                self.assertTrue(case[0] != case[1])
                self.assertTrue(case[1] != case[0])
