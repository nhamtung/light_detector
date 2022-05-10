#!/usr/bin/env python
import cv2
import numpy as np
import time

# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('/home/robotics/Downloads/MusicLEDBox.mp4')
frame = cv2.imread('/home/robotics/Downloads/image/13.jpg')

while True:
    # _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0, sigmaY=0, borderType=cv2.BORDER_DEFAULT)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    hi, threshold = cv2.threshold(blur, maxVal-40, 255, cv2.THRESH_BINARY)
    thr = threshold.copy()
    cv2.resize(thr, (200,200))

    edged = cv2.Canny(threshold, 50, 150)
    lightcontours = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.0, 100, param1=100, param2=30, minRadius=5, maxRadius=50)
    if len(lightcontours)>0 and circles is not None:
        count = 0
        circles = np.uint16(np.around(circles))
        for pt in circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            cv2.circle(frame, (a, b), 40, (0, 255, 0), 2)
            # print("(a, b) = (" + str(a) + ", " + str(b) +")")
            count = count +1
            # frame = cv2.putText(frame, str(count), (a-15, b+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        print("number of circles: " + str(count))

        # maxcontour = max(lightcontours, key=cv2.contourArea)
        # if cv2.contourArea(maxcontour) > 2000:
        #     (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
        #     cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
        #     cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)

    cv2.imshow('light', thr)
    cv2.imshow('frame', frame)
    # cv2.imshow('gray', gray)
    # cv2.imshow('blur', blur)
    cv2.waitKey(4)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()