# coding=utf-8
__author__ = 'andre'

import os
import cv2

from .topology import Topology
from .util import angle, adaptive_threshold, crop, horizontal_close, pop_up, rotate

class CVUtil:
    LINES = 50
    WHITE = [255, 255, 255]
    ALPHA = 10

    def __init__(self, fname=None, path=None, verbose=False):
        self.file_name = fname
        self.image_color = None
        self.image_gray = None
        self.image_bin = None
        self.height = None
        self.width = None
        self.structs = []
        self.height_char = None
        self.verbose = verbose
        self.path = path
        self.topology = Topology(verbose)
        if self.file_name is not None:
            self.load_file()

    def load_file(self, fname=None):
        if fname is not None:
            self.file_name = fname
        if self.verbose:
            print "Loading file ", self.file_name
        self.image_gray = cv2.copyMakeBorder(cv2.imread(self.file_name, 0), 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=self.WHITE)
        self.image_color = cv2.copyMakeBorder(cv2.imread(self.file_name), 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=self.WHITE)
        self.height, self.width = self.image_gray.shape

    def optimized_close(self):
        if self.verbose:
            print "Optimized Close"
        alpha = angle(self.image_gray, 100, self.ALPHA, self.verbose)
        self.image_color = rotate(alpha, self.image_color, self.verbose)
        self.image_gray = rotate(alpha, self.image_gray, self.verbose)
        self.image_bin = adaptive_threshold(self.image_gray, verbose=self.verbose)
        self.image_bin = horizontal_close(self.image_bin, verbose=self.verbose)
        self.topology.calculate(self.image_bin)
        heights = []
        for component in self.topology.get_components():
            heights.append(component.maxV-component.minV)
        heights.sort()
        self.height_char = heights[len(heights)/2]
        lenght = self.height_char*0.7
        self.image_bin = adaptive_threshold(self.image_gray, verbose=self.verbose)
        self.structs = []
        self.image_bin = horizontal_close(self.image_bin, lenght, verbose=self.verbose)
        self.topology.calculate(self.image_bin)

    def save_element(self, element, name):
        cv2.imwrite(os.path.join(self.path, name), element)

    def cutter(self):
        if self.verbose:
            print "Cutting image"
        self.image_bin = adaptive_threshold(self.image_gray, verbose=self.verbose)
        contador = 1
        for component in self.topology.get_components(self.height_char):
            down_right = (component.maxH, component.maxV)
            up_left = (component.minH, component.minV)
            element = crop(up_left, down_right, self.image_color)
            self.save_element(element, "img"+str(contador)+".png")
            contador += 1
        if self.verbose:
            for component in self.topology.get_components(self.height_char):
                down_right = (component.maxH, component.maxV)
                up_left = (component.minH, component.minV)
                cv2.rectangle(self.image_color, down_right, up_left, (0, 0, 255), 2)
            pop_up(self.image_color, "Delimited Image")