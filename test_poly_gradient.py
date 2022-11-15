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
        self.assertAlmostEqual(
            [[0.1, 0.1],
             [0.3, 0.3],
             [0.5, 0.5],
             [0.7, 0.7],
             [0.9, 0.9]],
            gradients, places=4)
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 4, 0, 0)
                      for x in range(2)] for y in range(4)]
        self.assertAlmostEqual(
            [[0.125, 0.125],
             [0.375, 0.375],
             [0.625, 0.625],
             [0.875, 0.875]],
            gradients, places=4)
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 3, 0, 0)
                      for x in range(2)] for y in range(3)]
        self.assertAlmostEqual(
            [[0.1667, 0.1667],
             [0.5   , 0.5   ],
             [0.8333, 0.8333]],
            gradients, places=4)

    def test_pre_no_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 6, 0, 1)
                      for x in range(2)] for y in range(6)]
        self.assertAlmostEqual(
            [[ 0,  0],
             [0.1, 0.1],
             [0.3, 0.3],
             [0.5, 0.5],
             [0.7, 0.7],
             [0.9, 0.9]],
            gradients, places=4)

    def test_no_pre_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 6, 1, 0)
                      for x in range(2)] for y in range(6)]
        self.assertAlmostEqual(
            [[0.1, 0.1],
             [0.3, 0.3],
             [0.5, 0.5],
             [0.7, 0.7],
             [0.9, 0.9],
             [1  , 1  ]],
            gradients, places=4)

    def test_pre_post(self):
        gradients = [[poly_gradient.linear_gradient(x, y, 2, 7, 1, 1)
                      for x in range(2)] for y in range(7)]
        self.assertAlmostEqual(
            [[0,   0  ],
             [0.1, 0.1],
             [0.3, 0.3],
             [0.5, 0.5],
             [0.7, 0.7],
             [0.9, 0.9],
             [1  , 1  ]],
            gradients, places=4)


class TestRadialGradient(FloatIterableTest):
    def test_no_pre_no_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 0, 0)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[0     , 0.088 , 0.1667, 0.088 , 0     ],
             [0.088 , 0.3619, 0.50  , 0.3619, 0.088 ],
             [0.1667, 0.50  , 0.8333, 0.50  , 0.1667],
             [0.088 , 0.3619, 0.50  , 0.3619, 0.088 ],
             [0     , 0.088 , 0.1667, 0.088 , 0     ]],
            gradients, places=4)

    def test_pre_no_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 1, 0)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[0     , 0.132 , 0.25, 0.132 , 0    ],
             [0.132 , 0.5429, 0.75, 0.5429, 0.132],
             [0.25  , 0.75  , 1   , 0.75  , 0.25 ],
             [0.132 , 0.5429, 0.75, 0.5429, 0.132],
             [0     , 0.132 , 0.25, 0.132 , 0    ]],
            gradients, places=4)

    def test_no_pre_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 0, 1)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[ 0   , 0     , 0   , 0     , 0   ],
             [ 0   , 0.0429, 0.25, 0.0429, 0   ],
             [ 0   , 0.25  , 0.75, 0.25  , 0   ],
             [ 0   , 0.0429, 0.25, 0.0429, 0   ],
             [ 0   , 0     , 0   , 0     , 0   ]],
            gradients, places=4)

    def test_pre_post(self):
        gradients = [[poly_gradient.radial_gradient(x, y, 5, 5, 1, 1)
                      for x in range(5)] for y in range(5)]
        self.assertAlmostEqual(
            [[ 0   , 0     , 0   , 0     ,  0   ],
             [ 0   , 0.0858, 0.5 , 0.0858,  0   ],
             [ 0   , 0.5   , 1   , 0.5   ,  0   ],
             [ 0   , 0.0858, 0.5 , 0.0858,  0   ],
             [ 0   , 0     , 0   , 0     ,  0   ]],
            gradients, places=4)


if __name__ == '__main__':
    unittest.main()
