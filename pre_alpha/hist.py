import os
import cv2
import numpy as np
import math
# from matplotlib import pyplot as plt


# img = cv2.imread('image1.jpeg', 0)
# img = cv2.medianBlur(img, 3)
#
# ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
#
# print ret
# print th1


# th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
#                             cv2.THRESH_BINARY, 11, 2)
# th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#                             cv2.THRESH_BINARY, 11, 2)
#
# titles = ['Original Image', 'Global Thresholding (v = 127)',
#           'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
#
# cv2.imwrite("image1TH1.jpeg", th1)
# cv2.imwrite("image1TH2.jpeg", th2)
# cv2.imwrite("image1TH3.jpeg", th3)


#
# for i in xrange(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()


filenames = next(os.walk("imagens"))[2]
for fn in filenames:
    if fn != "image1orig.jpeg":
        continue
    fname, fext = os.path.splitext(fn)
    if fext in [".jpeg", ".jpg", ".png"]:
        # try:
        #     os.makedirs(fname+"L", 0744)
        # except OSError:
        #     pass
        img = cv2.imread('image1.jpeg', 0)
        img = cv2.medianBlur(img, 3)

        ret, gray = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        # img = cv2.imread(fn)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        minimo = np.min(gray)
        maximo = np.max(gray)
        #
        # print minimo, maximo
        # break

        # print minimo+3*(maximo-minimo)/4

        height, width = img.shape
        print fname, height, width

        print "Laco 1"
        lcount = {}
        for i in range(0, height-1):
            lcount[i] = 0
            for j in range(0, width-1):
                # if gray[i][j] < minimo+3*(maximo-minimo)/4:
                if gray[i][j] < 100:
                    lcount[i] += 1

        # for i in lcount:
        #     print i, lcount[i]

        # lpontos = {}
        # for l in lcount:
        #     lpontos[lcount[l]] = 0
        # for l in lcount:
        #     lpontos[lcount[l]] += 1

        imgLines = []
        lines = []
        noLine = True
        print "Laco 2"
        for l in lcount:
            if 1000*lcount[l]/width >= 10 and noLine:
                noLine = False
                inicio = l
            elif 1000*lcount[l]/width < 15 and not noLine:
                noLine = True
                lines.append((inicio, l, l-inicio))
                imgLines.append(gray[inicio:l, :])

        words = []
        print "Laco 3"
        for l in lines:
            colunasNegras = {}
            for j in range(0, width-1):
                colunasNegras[j] = 0
                for i in range(l[0], l[1]):
                    if gray[i][j] < minimo+3*(maximo-minimo)/4:
                        colunasNegras[j] += 1
            wordStatus = -1
            for c in range(len(colunasNegras)):
                if colunasNegras[c] > 1 and wordStatus != 0:
                    if wordStatus == -1:
                        inicio = c
                    wordStatus = 0
                elif wordStatus != -1:
                    if wordStatus == 0:
                        fim = c
                    wordStatus += 1
                    if wordStatus > 2*l[2]/3:
                        words.append(((inicio-1, l[0]-1), (fim+1, l[1]+1)))
                        wordStatus = -1

        for w in words:
            cv2.rectangle(img, w[1], w[0], (0, 0, 255), 1)
        cv2.imwrite(os.path.join("Analises", "word", fname+"Word"+fext), img)
        cv2.imwrite(os.path.join("Analises", "word", fname+"Gray"+fext), gray)

        # os.system('play --no-show-progress --null --channels 1 synth 300 sine 2000')

        # for i in range(len(imgLines)):
        #     cv2.imwrite(os.path.join(fname+"L", str(i)+fext), imgLines[i])

        # fd = open(fname+".txt", "w")
        # fd.write('%d\t%d\t%d\n' % (height, width, depth) )
        # for l in lcount:
        #     fd.write('%d\t%d\n' % (l, lcount[l]))
        #     # print l, lpontos[l]
        # fd.close()
