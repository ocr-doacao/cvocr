#!/usr/bin/python
# -*- coding: UTF8 -*-

import os
import cv2
import numpy as np
import math
#from matplotlib import pyplot as plt

class Lista:
    def __init__(self, ponto, token):
        self.token = token
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


def main():
    imgDir = "imagens"
    extPermitidas = [".jpeg", ".jpg", ".png"]
    filenames = next(os.walk(imgDir))[2]

    for fn in filenames:
        if fn != "Ramon.jpg":
            continue

        fname, fext = os.path.splitext(fn)
        print fn
        if fext in extPermitidas:
            estruturas = []
            img = cv2.imread(os.path.join(imgDir, fn), 0)
            imgc = cv2.imread(os.path.join(imgDir, fn))
            img = cv2.medianBlur(img, 3)
            img2 = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
            # ret, bimg = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)

            bimg = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

            height, width = img.shape
            imgmap = np.zeros(img.shape, dtype=np.int)

            for h in range(height-1):
                for w in range(width-1):
                    if bimg[h][w] < 127:
                        if len(estruturas) == 0:
                            estruturas.append(Lista((h, w), 1))
                            imgmap[h][w] = 1
                        else:
                            cons = conexao(imgmap, (h,w))
                            if len(cons) == 0:
                                estruturas.append(Lista((h, w), len(estruturas)+1))
                                imgmap[h][w] = len(estruturas)
                            else:
                                estruturas[cons[0]-1].inserePonto((h, w))
                                imgmap[h][w] = cons[0]
                                for i in cons[1:]:
                                    estruturas[i-1].moveLista(estruturas[cons[0]-1])
            for e in estruturas:
                if e.tam > 0:
                    cv2.rectangle(imgc, (e.minH-1, e.minV-1), (e.maxH+1, e.maxV+1), (0, 0, 255), 1)
                    print e.tam
            cv2.imwrite(os.path.join("Analises", "Elementos", fname+fext), imgc)


if __name__ == "__main__":
    # print "L1"
    # l1 = Lista((1,1), 1)
    # l1.inserePonto((1,2))
    # l1.inserePonto((1,3))
    # l1.printMe()
    #
    # print "\nL2"
    # l2 = Lista((2,1), 2)
    # l2.inserePonto((3,2))
    # l2.inserePonto((4,3))
    # l2.printMe()
    #
    # print "\nL3"
    # l3 = Lista((7,1), 3)
    # l3.inserePonto((7,0))
    # l3.inserePonto((8,9))
    # l3.printMe()
    #
    # l2.moveLista(l1)
    # l2.moveLista(l1)
    # l2.moveLista(l1)
    # l2.moveLista(l1)
    # l2.moveLista(l1)
    # print "\nL2"
    # l2.inserePonto((5,5))
    # l2.printMe()
    # print "\nL1"
    # l1.printMe()
    #
    # l3.moveLista(l2)
    #
    # print "\nL1"
    # l1.printMe()
    # print "\nL2"
    # l2.printMe()
    # print "\nL3"
    # l3.printMe()
    #
    # l3.inserePonto((9,9))
    # print "\nL1"
    # l1.printMe()
    # print "\nL2"
    # l2.printMe()
    # print "\nL3"
    # l3.printMe()
    #
    # l3.moveLista(l2)
    #
    # print "\nL1"
    # l1.printMe()
    # print "\nL2"
    # l2.printMe()
    # print "\nL3"
    # l3.printMe()

    main()
