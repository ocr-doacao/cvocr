# coding=utf-8
__author__ = 'andre'

class Set:
    def __init__(self, point):
        self.elements = {point}
        self.parent = self
        self.maxV = point[0]
        self.minV = point[0]
        self.maxH = point[1]
        self.minH = point[1]

    def add(self, point):
        if not (isinstance(point, tuple) and len(point) == 2):
            return False
        if self != self.parent:
            self.parent.add(point)
        else:
            self.__add_local(point)

    def __add_local(self, point):
        self.elements.add(point)
        if point[0] > self.maxV:
            self.maxV = point[0]
        elif point[0] < self.minV:
            self.minV = point[0]
        if point[1] > self.maxH:
            self.maxH = point[1]
        elif point[1] < self.minH:
            self.minH = point[1]
            
    def move(self, destination):
        if len(self.elements) != 0:
            while destination.parent != destination:
                destination = destination.parent
            self.parent = destination
            destination.elements = destination.elements | self.elements
            self.elements = set()
            if self.parent.maxV < self.maxV:
                self.parent.maxV = self.maxV
            elif self.parent.minV > self.minV:
                self.parent.minV = self.minV
            if self.parent.maxH < self.maxH:
                self.parent.maxH = self.maxH
            elif self.parent.minH > self.minH:
                self.parent.minH = self.minH

    def __str__(self):
        return str((self.minH, self.maxH, self.minV, self.maxV))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.elements == other.elements
        return False

    def __contains__(self, element):
        return element in self.elements

    def __len__(self):
        return len(self.elements)