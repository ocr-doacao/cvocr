# coding=utf-8
__author__ = 'andre'

import cv2
import numpy as np

# Daqui em diante é preciso refatorar.

class Lista:
    def __init__(self, ponto):
        self.inicio = PontoPreto(ponto)
        self.fim = self.inicio
        self.tam = 1
        self.pai = self
        self.maxV = ponto[0]
        self.minV = ponto[0]
        self.maxH = ponto[1]
        self.minH = ponto[1]

    def inserePonto(self, ponto):
        if self != self.pai:
            self.pai.inserePonto(ponto)
        else:
            self.inserePontoLocal(ponto)

    def inserePontoLocal(self, ponto):
        self.inicio = PontoPreto(ponto, self.inicio)
        self.tam += 1
        if ponto[0] > self.maxV:
            self.maxV = ponto[0]
        elif ponto[0] < self.minV:
            self.minV = ponto[0]
        if ponto[1] > self.maxH:
            self.maxH = ponto[1]
        elif ponto[1] < self.minH:
            self.minH = ponto[1]

    def printMap(self, imgmap, valor):
        ponto = self.inicio
        while ponto is not None:
            imgmap[ponto.posicao[0]][ponto.posicao[0]] = valor
            ponto = ponto.filho

    def moveLista(self, lista):
        if self.tam != 0:
            while lista.pai != lista:
                lista = lista.pai
            lista.fim.filho = self.inicio
            lista.fim = self.fim
            self.pai = lista
            self.inicio = None
            self.fim = None
            self.pai.tam += self.tam
            self.tam = 0
            if self.pai.maxV < self.maxV:
                self.pai.maxV = self.maxV
            elif self.pai.minV > self.minV:
                self.pai.minV = self.minV
            if self.pai.maxH < self.maxH:
                self.pai.maxH = self.maxH
            elif self.pai.minH > self.minH:
                self.pai.minH = self.minH

    def printMe(self):
        ponto = self.inicio
        while ponto is not None:
            print ponto
            ponto = ponto.filho

class PontoPreto:
    def __init__(self, posicao=(-1, -1), filho=None):
        self.posicao = posicao
        self.filho = filho

    def __str__(self):
        return str(self.posicao)

def conexao(imgmap, ponto):
    val = set()
    for i in range(ponto[0]-1, ponto[0]+2):
        for j in range(ponto[1]-1, ponto[1]+2):
            if i == ponto[0] and j == ponto[1]:
                continue
            if imgmap[i][j] > 0:
                val.add(imgmap[i][j])
    lst = list(val)
    lst.sort()
    return lst

# Aqui começa o código desta parte

class CVUtil:
    def __init__(self, fname=None):
        self.file_name = fname
        self.image_color = None
        self.image_gray = None
        self.image_bin = None
        self.height = None
        self.width = None
        self.structs = []
        if self.file_name is not None:
            self.load_file()

    def load_file(self, fname=None):
        if fname is not None:
            self.file_name = fname
        self.image_gray = cv2.imread(self.file_name, 0)
        self.image_color = cv2.imread(self.file_name)
        self.height, self.width = self.image_gray.shape

    def adaptive_threshold(self):
        img = self.image_gray
        # img = cv2.medianBlur(self.image_gray, 3)
        # img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        self.image_bin = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    def __conection(self, image_map, point):
        """
        Retorna a lista de 8 vizinhos dos elementos já mapeados em ordem crescente.
        :param image_map: Mapeamento, inicializado com zeros
        :param point:     Ponto para a análise
        :return:          Lista ordenada
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

    def get_elements(self):
        self.structs = []
        if self.image_bin is None:
            self.adaptive_threshold()

        image_map = np.zeros(self.image_bin.shape, dtype=np.int)

        for h in range(self.height-1):
            for w in range(self.width-1):
                if self.image_bin[h][w] < 127:
                    if len(self.structs) == 0:
                        self.structs.append(Lista((h, w)))
                        image_map[h][w] = 1
                    else:
                        cons = self.__conection(image_map, (h,w))
                        if len(cons) == 0:
                            self.structs.append(Lista((h, w)))
                            image_map[h][w] = len(self.structs)
                        else:
                            self.structs[cons[0]-1].inserePonto((h, w))
                            image_map[h][w] = cons[0]
                            for i in cons[1:]:
                                self.structs[i-1].moveLista(self.structs[cons[0]-1])

if __name__ == "__main__":
    cvu = CVUtil("pre_alpha/imagens/elementos3.png")
    cvu.get_elements()
    print len(cvu.structs)

    for s in cvu.structs:
        print ( s.maxV, s.minV, s.maxH, s.minH)