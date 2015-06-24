#!/usr/bin/python
# -*- coding: UTF8 -*-
import unittest
import numpy as np

import sys
import os
local = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local, "..", "..", ".."))
from cv.util import adaptive_threshold, angle, horizontal_close, matrix_rotation, rotate, crop, pop_up

class TestUtil(unittest.TestCase):
    def test_adaptive_threshold(self):
        raise NotImplementedError

    def test_angle(self):
        raise NotImplementedError

    def test_horizontal_close(self):
        raise NotImplementedError

    def test_matrix_rotation(self):
        raise NotImplementedError

    def test_rotate(self):
        raise NotImplementedError

    def test_crop(self):
        raise NotImplementedError

    def test_pop_up(self):
        raise NotImplementedError

if __name__ == "__main__":
    unittest.main()