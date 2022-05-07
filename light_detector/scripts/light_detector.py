#!/usr/bin/env python
#import libs
import cv2
import numpy as np
import time

# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('/home/robotics/Downloads/MusicLEDBox.mp4')
frame = cv2.imread('/home/robotics/Downloads/image/4.jpg')

while True:
    # _, frame = cap.read()
    #convert frame to monochrome and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0, sigmaY=0, borderType=cv2.BORDER_DEFAULT)
    #use function to identify threshold intensities and locations
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    #threshold the blurred frame accordingly
    hi, threshold = cv2.threshold(blur, maxVal-20, 255, cv2.THRESH_BINARY)
    thr = threshold.copy()
    #resize frame for ease
    cv2.resize(thr, (300,300))



    #find contours in thresholded frame
    edged = cv2.Canny(threshold, 50, 150)
    lightcontours = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #attempts finding the circle created by the torch illumination on the wall
    circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1.0, 10, param1=10, param2=15, minRadius=20, maxRadius=100)
    # circles = np.uint16(np.around(circles))



    #check if the list of contours is greater than 0 and if any circles are detected
    # if len(lightcontours)>0:
    #     if circles is not None:
    #         print("HERE")
    #         #Find the Maxmimum Contour, this is assumed to be the light beam
    #         maxcontour = max(lightcontours, key=cv2.contourArea)
    #         #avoids random spots of brightness by making sure the contour is reasonably sized
    #         if cv2.contourArea(maxcontour) > 2000:
    #             (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
    #             cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
    #             cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('blur', blur)
    cv2.imshow('light', thr)
    cv2.waitKey(4)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()