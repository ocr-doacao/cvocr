import os
import cv2
import numpy as np
import math

filenames = next(os.walk("."))[2]
for fn in filenames:
    fname, fext = os.path.splitext(fn)
    if fext in [".jpg", ".png"]:
        try:
            os.makedirs(fname, 0744)
        except OSError:
            pass
        print fn
        img = cv2.imread(fn)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        height, width, depth = img.shape
        #print height, width, depth

        for w in range(width, 1, -1):
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
                        ang.append(math.atan2((fy1-fy2), (fx1-fx2))*57.2957795)
                if len(lsty) == 0:
                    continue
                if len(lsty) < 15:
                    lsty.sort()
                    ang = np.around(ang, decimals=3)
                    ang.sort()
                    print fn, w, len(lsty)
                    print ang
                    cv2.putText(img, str(w), (10,100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 7, (0, 255, 255))
                    cv2.imwrite(os.path.join(fname, str(w)+fext), img)
                else:
                    break
            except TypeError:
                pass
