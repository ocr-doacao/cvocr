#!/usr/bin/python
# -*- coding: UTF8 -*-
import unittest
from random import randint

import sys
import os
local = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local, "..", "..", ".."))
from cv.set import Set

class TestSet(unittest.TestCase):
    def auto_create(self, set_list):
        size = randint(20, 100)
        for i in range(1, size):
            for s in set_list:
                s.add((i, i))
        return size

    def test_empty_create(self):
        self.failUnlessRaises(TypeError, Set)

    def test_create(self):
        s1 = Set((0, 0))
        self.assertIn((0, 0), s1)
        self.assertEqual(1, len(s1))

    def test_add(self):
        s1 = Set((0, 0))
        size = self.auto_create([s1])
        self.assertEqual(size, len(s1))

    def test_edges(self):
        s1 = Set((5, 5))
        s1.add((0, 5))
        s1.add((5, 0))
        s1.add((10, 5))
        s1.add((5, 10))
        self.assertEqual(str(s1), "(0, 10, 0, 10)")

    def test_equals(self):
        s1 = Set((0, 0))
        s2 = Set((0, 0))
        self.auto_create([s1, s2])
        self.assertTrue(s1 == s2)
        s2.add((0, 1))
        self.assertFalse(s1 == s2)

    def test_move(self):
        s1 = Set((0, 0))
        s2 = Set((0, 1))
        size = self.auto_create([s1, s2])
        self.assertTrue((0, 0) in s1)
        self.assertFalse((0, 1) in s1)
        s2.move(s1)
        self.assertEqual(size+1, len(s1))
        self.assertEqual(0, len(s2))

    def test_move_add(self):
        s1 = Set((0, 0))
        s2 = Set((0, 1))
        size = self.auto_create([s1, s2])
        s2.move(s1)
        s2.add((0, 2))
        self.assertEqual(size+2, len(s1))
        self.assertEqual(0, len(s2))

    def test_move_in_moved(self):
        s1 = Set((0, 0))
        s2 = Set((0, 1))
        s3 = Set((0, 2))
        size = self.auto_create([s1, s2])
        s2.move(s1)
        s3.move(s2)
        s3.add((0, 3))
        self.assertEqual(size+3, len(s1))
        self.assertEqual(0, len(s2))
        self.assertEqual(0, len(s3))

    def test_move_edges(self):
        s1 = Set((5, 5))
        s2 = Set((0, 5))
        s3 = Set((5, 0))
        s4 = Set((10, 5))
        s5 = Set((5, 10))
        s2.move(s1)
        s3.move(s1)
        s4.move(s2)
        s5.move(s3)
        self.assertEqual(str(s1), "(0, 10, 0, 10)")

if __name__ == "__main__":
    unittest.main()