# coding=utf-8
__author__ = 'andre'

class List:
    def __init__(self, point):
        self.begin = Point(point)
        self.end = self.begin
        self.size = 1
        self.parent = self
        self.maxV = point[0]
        self.minV = point[0]
        self.maxH = point[1]
        self.minH = point[1]

    def add(self, point):
        if self != self.parent:
            self.parent.add(point)
        else:
            self.add_local(point)

    def add_local(self, point):
        self.begin = Point(point, self.begin)
        self.size += 1
        if point[0] > self.maxV:
            self.maxV = point[0]
        elif point[0] < self.minV:
            self.minV = point[0]
        if point[1] > self.maxH:
            self.maxH = point[1]
        elif point[1] < self.minH:
            self.minH = point[1]

    def print_map(self, image_map, value):
        point = self.begin
        while point is not None:
            image_map[point.position[0]][ponto.position[0]] = value
            point = point.child
            
    def move(self, lst):
        if self.size != 0:
            while lst.parent != lst:
                lst = lst.parent
            lst.end.child = self.begin
            lst.end = self.end
            self.parent = lst
            self.begin = None
            self.end = None
            self.parent.size += self.size
            self.size = 0
            if self.parent.maxV < self.maxV:
                self.parent.maxV = self.maxV
            elif self.parent.minV > self.minV:
                self.parent.minV = self.minV
            if self.parent.maxH < self.maxH:
                self.parent.maxH = self.maxH
            elif self.parent.minH > self.minH:
                self.parent.minH = self.minH

    def print_me(self):
        point = self.begin
        while point is not None:
            print point
            point = point.child

    def __str__(self):
        return str((self.minH, self.maxH, self.minV, self.maxV))

class Point:
    def __init__(self, position=(-1, -1), child=None):
        self.position = position
        self.child = child

    def __str__(self):
        return str(self.position)

# A main é apenas um teste manual, deve ser modificado pra um teste adequado.
if __name__ == "__main__":
    print "L1"
    l1 = List((1,1))
    l1.add((1,2))
    l1.add((1,3))
    l1.print_me()
    
    print "\nL2"
    l2 = List((2,1))
    l2.add((3,2))
    l2.add((4,3))
    l2.print_me()
    
    print "\nL3"
    l3 = List((7,1))
    l3.add((7,0))
    l3.add((8,9))
    l3.print_me()
    
    l2.move(l1)
    l2.move(l1)
    l2.move(l1)
    l2.move(l1)
    l2.move(l1)
    print "\nL2"
    l2.add((5,5))
    l2.print_me()
    print "\nL1"
    l1.print_me()
    
    l3.move(l2)
    
    print "\nL1"
    l1.print_me()
    print "\nL2"
    l2.print_me()
    print "\nL3"
    l3.print_me()
    
    l3.add((9,9))
    print "\nL1"
    l1.print_me()
    print "\nL2"
    l2.print_me()
    print "\nL3"
    l3.print_me()
    
    l3.move(l2)
    
    print "\nL1"
    l1.print_me()
    print "\nL2"
    l2.print_me()
    print "\nL3"
    l3.print_me()