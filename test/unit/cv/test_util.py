#!/usr/bin/python
# -*- coding: UTF8 -*-
import unittest
import numpy as np

import sys
import os
local = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local, "..", "..", "..", "cv"))
from util import adaptive_threshold, angle, horizontal_close, matrix_rotation, rotate, crop, pop_up

class TestUtil(unittest.TestCase):
    def test_adaptive_threshold(self):
        pass

    def test_angle(self):
        pass

    def test_horizontal_close(self):
        pass

    def test_matrix_rotation(self):
        pass

    def test_rotate(self):
        pass

    def test_crop(self):
        pass

    def test_pop_up(self):
        pass

if __name__ == "__main__":
    unittest.main()