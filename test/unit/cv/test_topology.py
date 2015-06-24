#!/usr/bin/python
# -*- coding: UTF8 -*-
import unittest
import numpy as np

import sys
import os
local = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local, "..", "..", ".."))
from cv.topology import Topology

class TestSet(unittest.TestCase):
    SIZE = 100

    def chess_board(self):
        image = np.empty((self.SIZE, self.SIZE))
        image[:, :] = 255
        image[::2, ::2] = 0
        image[1::2, 1::2] = 0
        return image

    def max_board(self):
        image = np.empty((self.SIZE, self.SIZE))
        image[:, :] = 255
        image[::2, ::2] = 0
        return image

    def assertTopologyLen(self, image, size):
        topology = Topology()
        topology.calculate(image)
        self.assertEqual(len(topology), size)

    def test_single_component(self):
        image = np.zeros((self.SIZE, self.SIZE))
        topology = Topology()
        topology.calculate(image)
        self.assertEqual(len(topology), 1)

    def test_no_component(self):
        image = np.empty((self.SIZE, self.SIZE))
        image[:, :] = 255
        self.assertTopologyLen(image, 0)

    def test_max_elements(self):
        image = self.max_board()
        self.assertTopologyLen(image, self.SIZE**2/4)

    def test_chess(self):
        image = self.chess_board()
        self.assertTopologyLen(image, 1)

    def test_get_components_empty(self):
        image = self.max_board()
        topology = Topology()
        topology.calculate(image)
        ncomponents = 0
        for component in topology.get_components():
            ncomponents += 1
        self.assertEqual(ncomponents, 0)

    def test_get_components_one(self):
        image = self.chess_board()
        topology = Topology()
        topology.calculate(image)
        ncomponents = 0
        for component in topology.get_components():
            ncomponents += 1
        self.assertEqual(ncomponents, 1)

    def test_get_components_height(self):
        image = self.chess_board()
        image[self.SIZE/2, :] = 255
        topology = Topology()
        topology.calculate(image)
        ncomponents = 0
        for component in topology.get_components():
            ncomponents += 1
        self.assertEqual(ncomponents, 2)

if __name__ == "__main__":
    unittest.main()