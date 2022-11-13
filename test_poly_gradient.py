#!/usr/bin/env python3
import collections
import itertools
import poly_gradient
import unittest


class FloatIterableTest(unittest.TestCase):
    def assertAlmostEqual(self, first, second, places=7, msg=None, delta=None):
        if isinstance(first, collections.abc.Iterable) \
                and isinstance(second, collections.abc.Iterable):
            for (f, s) in itertools.zip_longest(first, second):
                self.assertAlmostEqual(f, s, places, msg, delta)
        else:
            super().assertAlmostEqual(first, second, places, msg, delta)


class TestLinearGradient(FloatIterableTest):
    def test_no_pre_no_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 5, 0, 0)
                      for x in range(2)] for y in range(5)]
        self.assertEqual([[10, 10],
                          [30, 30],
                          [50, 50],
                          [70, 70],
                          [90, 90]], gradients)
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 4, 0, 0)
                      for x in range(2)] for y in range(4)]
        self.assertAlmostEqual([[12.5, 12.5],
                                [37.5, 37.5],
                                [62.5, 62.5],
                                [87.5, 87.5]], gradients)
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 3, 0, 0)
                      for x in range(2)] for y in range(3)]
        self.assertAlmostEqual([[      50/3,       50/3],
                                [        50,         50],
                                [100 - 50/3, 100 - 50/3]], gradients)

    def test_pre_no_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 6, 0, 1)
                      for x in range(2)] for y in range(6)]
        self.assertEqual([[ 0,  0],
                          [10, 10],
                          [30, 30],
                          [50, 50],
                          [70, 70],
                          [90, 90]], gradients)

    def test_no_pre_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 6, 1, 0)
                      for x in range(2)] for y in range(6)]
        self.assertEqual([[ 10,  10],
                          [ 30,  30],
                          [ 50,  50],
                          [ 70,  70],
                          [ 90,  90],
                          [100, 100]], gradients)

    def test_pre_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 7, 1, 1)
                      for x in range(2)] for y in range(7)]
        self.assertEqual([[  0,   0],
                          [ 10,  10],
                          [ 30,  30],
                          [ 50,  50],
                          [ 70,  70],
                          [ 90,  90],
                          [100, 100]], gradients)


class TestRadialGradient(FloatIterableTest):
    def test_no_pre_no_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 0, 0)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[ 0   ,  8.8 , 16.67,  8.8 ,  0   ],
             [ 8.8 , 36.19, 50   , 36.19,  8.8 ],
             [16.67, 50   , 83.33, 50   , 16.67],
             [ 8.8 , 36.19, 50   , 36.19,  8.8 ],
             [ 0   ,  8.8 , 16.67,  8.8 ,  0   ]],
            gradients, places=2)

    def test_pre_no_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 1, 0)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[ 0   , 13.2 , 25   , 13.2 ,  0   ],
             [13.2 , 54.29, 75   , 54.29, 13.2 ],
             [25   , 75   ,100   , 75   , 25   ],
             [13.2 , 54.29, 75   , 54.29, 13.2 ],
             [ 0   , 13.2 , 25   , 13.2 ,  0   ]],
            gradients, places=2)

    def test_no_pre_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 0, 1)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[ 0   ,  0   ,  0   ,  0   ,  0   ],
             [ 0   ,  4.29, 25   ,  4.29,  0   ],
             [ 0   , 25   , 75   , 25   ,  0   ],
             [ 0   ,  4.29, 25   ,  4.29,  0   ],
             [ 0   ,  0   ,  0   ,  0   ,  0   ]],
            gradients, places=2)

    def test_pre_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 1, 1)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[ 0   ,  0   ,  0   ,  0   ,  0   ],
             [ 0   ,  8.58, 50   ,  8.58,  0   ],
             [ 0   , 50   ,100   , 50   ,  0   ],
             [ 0   ,  8.58, 50   ,  8.58,  0   ],
             [ 0   ,  0   ,  0   ,  0   ,  0   ]],
            gradients, places=2)


if __name__ == '__main__':
    unittest.main()
