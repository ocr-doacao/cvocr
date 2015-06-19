# coding=utf-8
import os
import cv2
import numpy as np
import math

LINES = 100

filenames = next(os.walk("imagens"))[2]
for fn in filenames:
    if fn != "image1orig.jpeg":
        continue
    fname, fext = os.path.splitext(fn)
    if fext in [".jpeg", ".jpg", ".png"]:
        try:
            os.makedirs(fname+"b", 0744)
        except OSError:
            pass
        img = cv2.imread(fn)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        height, width, depth = img.shape

    lsty = []
    i = 0
    s = width
    while len(lsty)!=1:
        w = (i + s)/2
        img = cv2.imread(fn)
        lsty = []
        ang = []
        ang2 = []
        lines = cv2.HoughLines(edges,1,np.pi/180,w)
        try:
            for rho, theta in lines[0]:
                alpha = 180*theta/np.pi
                if alpha < 11:
                    ang2.append(alpha)
                elif alpha > 169:
                    ang2.append(-(180 - alpha))

            if len(ang2) == LINES or s - i == 1:
                print len(lsty), len(ang2), np.average(ang2)
                ang = np.average(ang2)

                M = cv2.getRotationMatrix2D((width/2, height/2), ang, 1)
                print M.shape
                dst = cv2.warpAffine(img, M, (width, height))

                img2 = cv2.imread(fn, 0)
                img2 = cv2.medianBlur(img2, 3)
                img2 = cv2.fastNlMeansDenoising(img2, None, 10, 7, 21)
                bimg = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


                # Junção de palavras
                # 50 == 3000/60 (width/60)
                # ideia: fazer 2 buscas:
                #   1a) encontrar altura da letra usando um elemento estruturante grande (tira ruido de letras com i)
                #   2a) usar 70% da altura encontrada como tamanho do elemento estruturante
                cv2.bitwise_not(bimg, bimg)
                kernel = np.ones((1, width/30), np.uint8)
                outra = cv2.morphologyEx(bimg, cv2.MORPH_CLOSE, kernel)
                cv2.bitwise_not(outra, outra)

                # print ang
                cv2.putText(img, str(w), (10,100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 7, (0, 255, 255))
                cv2.imwrite(os.path.join("Analises", "hline_bin", fname+fext), img)
                cv2.imwrite(os.path.join("Analises", "hline_bin", fname+"Rot"+fext), dst)
                cv2.imwrite(os.path.join("Analises", "hline_bin", fname+"Close"+fext), outra)
                # cv2.imwrite(os.path.join(fname+"b", str(w)+fext), img)
                break
            elif len(ang2) < LINES:
                s = w
            elif len(ang2) > LINES:
                i = w
        except TypeError:
            s = w
