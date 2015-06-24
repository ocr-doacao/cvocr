# coding=utf-8
__author__ = 'andre'

from .set import Set
import numpy as np

class Topology:
    def __init__(self, verbose=False):
        self.image = None
        self.width = None
        self.height = None
        self.components = []
        self.verbose = verbose

    def __conection(self, image_map, point):
        """
        Retorna uma lista dos componentes 8 conexos já mapeados em ordem crescente.
        :param image_map: Mapeamento, inicializado com zeros
        :param point:     Ponto para a análise
        :return:          List ordenada
        """
        val = set()
        for i in range(point[0]-1, point[0]+2):
            for j in range(point[1]-1, point[1]+2):
                if i == point[0] and j == point[1]:
                    continue
                if image_map[i][j] > 0:
                    val.add(image_map[i][j])
        lst = list(val)
        lst.sort()
        return lst

    def __through_pixels(self):
        for h in range(self.height-1):
            for w in range(self.width-1):
                yield (h, w)

    def __list_manipulation(self, image_map, point):
        h, w = point
        if self.image[h][w] < 127:
            if len(self.components) == 0:
                self.components.append(Set((h, w)))
                image_map[h][w] = 1
            else:
                cons = self.__conection(image_map, (h,w))
                if len(cons) == 0:
                    self.components.append(Set((h, w)))
                    image_map[h][w] = len(self.components)
                else:
                    self.components[cons[0]-1].add((h, w))
                    image_map[h][w] = cons[0]
                    for i in cons[1:]:
                        self.components[i-1].move(self.components[cons[0]-1])

    def __valid_component(self, component, height=None):
        comp = (len(component) == 0 or (component.maxH-component.minH) < 3 or (component.maxV-component.minV) < 10)
        if height is None:
            return not comp
        return not (comp or (component.maxV-component.minV) > 2.5*height)

    def calculate(self, image):
        self.components = []
        self.image = image
        self.height, self.width = self.image.shape
        image_map = np.zeros(self.image.shape, dtype=np.int)
        if self.verbose:
            print "Get components"
        for point in self.__through_pixels():
            self.__list_manipulation(image_map, point)
        self.components = filter(lambda c: len(c) > 0, self.components)

    def get_components(self, height=None):
        for component in self.components:
            if self.__valid_component(component, height):
                yield component

    def __getitem__(self, key):
        return self.components[key]

    def __len__(self):
        return len(self.components)

    def __contains__(self, component):
        return component in self.components