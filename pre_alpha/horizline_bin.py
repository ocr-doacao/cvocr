import os
import cv2
import numpy as np
import math

LINES = 50

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
        # print fn
        img = cv2.imread(fn)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        height, width, depth = img.shape
        #print height, width, depth

    lsty = []
    i = 0
    s = width
    while len(lsty)!=1:
        w = (i + s)/2
        img = cv2.imread(fn)
        lsty = []
        ang = []
        lines = cv2.HoughLines(edges,1,np.pi/180,w)
        try:
            for rho,theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                fx1 = float(x0 + 1000*(-b))
                fy1 = float(y0 + 1000*(a))
                fx2 = float(x0 - 1000*(-b))
                fy2 = float(y0 - 1000*(a))
                if np.fabs((fx1-fx2)/(fy1-fy2)) > 5:
                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    lsty.append(int((fy1+fy2)/2))
                    auxang = math.atan2((fy1-fy2), (fx1-fx2))*180/np.pi
                    if auxang < 0:
                        auxang = - (180 + auxang)
                    else:
                        auxang = - (auxang - 180)
                    ang.append(auxang)
            # print i, s, LINES, len(lsty), w
            if len(lsty) == LINES or s - i == 1:
                # print fn, w, len(lsty)
                print LINES, np.average(ang)
                ang = -np.average(ang)

                M = cv2.getRotationMatrix2D((width/2, height/2), ang, 1)
                dst = cv2.warpAffine(img, M, (width, height))

                img2 = cv2.imread(fn, 0)
                img2 = cv2.medianBlur(img2, 3)
                img2 = cv2.fastNlMeansDenoising(img2, None, 10, 7, 21)
                bimg = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                # 50 == 3000/60 (width/60)
                # ideia: fazer 2 buscas:
                #   1a) encontrar altura da letra usando um elemento estruturante grande (tira ruido de letras com i)
                #   2a) usar 70% da altura encontrada como tamanho do elemento estruturante
                cv2.bitwise_not(bimg, bimg)
                kernel = np.ones((1, 49), np.uint8)
                outra = cv2.morphologyEx(bimg, cv2.MORPH_CLOSE, kernel)
                cv2.bitwise_not(outra, outra)

                # print ang
                cv2.putText(img, str(w), (10,100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 7, (0, 255, 255))
                cv2.imwrite(os.path.join("Analises", "hline_bin", fname+fext), img)
                cv2.imwrite(os.path.join("Analises", "hline_bin", fname+"Rot"+fext), dst)
                cv2.imwrite(os.path.join("Analises", "hline_bin", fname+"Close"+fext), outra)
                # cv2.imwrite(os.path.join(fname+"b", str(w)+fext), img)
                break
            elif len(lsty) < LINES:
                s = w
            elif len(lsty) > LINES:
                i = w
        except TypeError:
            s = w
