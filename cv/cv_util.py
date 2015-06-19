# coding=utf-8
__author__ = 'andre'

import os
import cv2
import numpy as np

from smart_list import List, Point

class CVUtil:
    LINES = 50
    WHITE = [255, 255, 255]

    def __init__(self, fname=None, path=None, verbose=False):
        self.file_name = fname
        self.image_color = None
        self.image_gray = None
        self.image_bin = None
        self.image_bin_bkp = None
        self.height = None
        self.width = None
        self.structs = []
        self.height_char = None
        self.verbose = verbose
        self.path = path
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

    def adaptive_threshold(self, blur=True):
        if self.verbose:
            print "Thresholding"
        img = self.image_gray
        if blur:
            img = cv2.medianBlur(img, 3)
            img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    def __conection(self, image_map, point):
        """
        Retorna a List de 8 vizinhos dos elementos já mapeados em ordem crescente.
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

    def __through_pixels(self, bool=True):
        if bool:
            for h in range(self.height-1):
                for w in range(self.width-1):
                    yield (h, w)
        else:
            for w in range(self.width-1):
                for h in range(self.height-1):
                    yield (h, w)

    def __list_manipulation(self, image_map, point):
        h, w = point
        if self.image_bin[h][w] < 127:

            if len(self.structs) == 0:
                self.structs.append(List((h, w)))
                image_map[h][w] = 1
            else:
                cons = self.__conection(image_map, (h,w))
                if len(cons) == 0:
                    self.structs.append(List((h, w)))
                    image_map[h][w] = len(self.structs)
                else:
                    self.structs[cons[0]-1].add((h, w))
                    image_map[h][w] = cons[0]
                    for i in cons[1:]:
                        self.structs[i-1].move(self.structs[cons[0]-1])

    def _valid_element(self, struct):
        if self.height_char is None:
            return not (struct.size == 0 or (struct.maxH-struct.minH) < 3 or (struct.maxV-struct.minV) < 10)
        return not \
            (
                struct.size == 0 or
                (struct.maxH-struct.minH) < 3 or
                (struct.maxV-struct.minV) < 10 or
                (struct.maxV-struct.minV) > 2.5*self.height_char
            )

    def all_elements(self):
        if self.verbose:
            print "Get elements"
        self.structs = []
        if self.image_bin is None:
            self.image_bin = self.adaptive_threshold()
        image_map = np.zeros(self.image_bin.shape, dtype=np.int)
        for point in self.__through_pixels():
            self.__list_manipulation(image_map, point)

    def angle(self, nlines, alpha):
        if self.verbose:
            print "Get angle"
        edges = cv2.Canny(self.image_gray, 50, 150, apertureSize=3)
        angle = None
        begin = 0
        end = self.width
        while angle is None:
            middle = (begin + end)/2
            lst_angle = []
            lines = cv2.HoughLines(edges, 1, np.pi/180, middle)
            try:
                for rho, theta in lines[0]:
                    theta = 180*theta/np.pi
                    if theta < alpha:
                        lst_angle.append(theta)
                    elif theta > 180 - alpha:
                        lst_angle.append(-(180 - theta))
                if len(lst_angle) == nlines or end - begin == 1:
                    angle = np.average(lst_angle)
                elif len(lst_angle) < nlines:
                    end = middle
                elif len(lst_angle) > nlines:
                    begin = middle
            except TypeError:
                end = middle
        return angle

    def _matrix_rotation(self, alpha):
        return cv2.getRotationMatrix2D((self.width/2, self.height/2), alpha, 1)

    def rotate(self, alpha, image):
        if self.verbose:
            print "Rotate image"
        matrix_rotation = self._matrix_rotation(alpha)
        return cv2.warpAffine(image, matrix_rotation, (self.width, self.height))

    def horizontal_close(self, lenght=None):
        if self.verbose:
            print "Making close"
        if lenght is None:
            lenght = self.width/30
        if self.image_bin is None:
            self.image_bin = self.adaptive_threshold()
        cv2.bitwise_not(self.image_bin, self.image_bin)
        kernel = np.ones((1, int(lenght)), np.uint8)
        self.image_bin = cv2.morphologyEx(self.image_bin, cv2.MORPH_CLOSE, kernel)
        cv2.bitwise_not(self.image_bin, self.image_bin)

    def optimized_close(self):
        if self.verbose:
            print "Optimized Close"
        alpha = self.angle(100,10)
        self.image_color = self.rotate(alpha, self.image_color)
        self.image_gray = self.rotate(alpha, self.image_gray)
        self.image_bin = self.adaptive_threshold()
        self.horizontal_close()
        self.all_elements()
        heights = []
        for struct in self.structs:
            if self._valid_element(struct):
                heights.append(struct.maxV-struct.minV)
        heights.sort()
        self.height_char = heights[len(heights)/2]
        lenght = self.height_char*0.7
        self.image_bin = self.adaptive_threshold()
        self.structs = []
        self.horizontal_close(lenght)
        self.all_elements()

    def save_element(self, element, name):
        cv2.imwrite(os.path.join(self.path, name), element)

    def crop(self, up_left, down_right, image):
        crop = image[up_left[1]:down_right[1], up_left[0]:down_right[0]]
        return cv2.copyMakeBorder(crop, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    def cutter(self):
        if self.verbose:
            print "Cutting image"
        self.image_bin = self.adaptive_threshold()
        contador = 1
        for struct in self.structs:
            if self._valid_element(struct):
                down_right = (struct.maxH, struct.maxV)
                up_left = (struct.minH, struct.minV)
                element = self.crop(up_left, down_right, self.image_color)
                self.save_element(element, "img"+str(contador)+".png")
                contador += 1
        if self.verbose:
            for struct in self.structs:
                if self._valid_element(struct):
                    down_right = (struct.maxH, struct.maxV)
                    up_left = (struct.minH, struct.minV)
                    cv2.rectangle(self.image_color, down_right, up_left, (0, 0, 255), 2)
            self.pop_up(self.image_color, "Delimited Image")

    def pop_up(self, image, title):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, image)
        cv2.waitKey(0)