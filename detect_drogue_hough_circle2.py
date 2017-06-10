# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 11:42:53 2017

@author: GK
"""

import numpy as np
import cv2
import sys
import os


print os.getcwd()
videos = ['F18_Mid-Air-edit1.mp4', 'F18_Mid-Air-edit2.mp4']
fourcc = cv2.cv.CV_FOURCC('M','J','P','G')

view = False
write = True

for video in videos:
    cap = cv2.VideoCapture(video)
    
    
    while not cap.isOpened():
        cap = cv2.VideoCapture(video)
        cv2.waitKey(1000)
        print "Wait for the header"
        
    
    pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    circles = np.zeros((1,1,3), dtype=np.uint16)
    
    if view:
        cv2.namedWindow('detected circles')
    
    
    
    if write:
        #Setup Video Writer
        h = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        size = (w,h)
        output_file = "output\o2-%s.avi" % video
        
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print fps
        out = cv2.VideoWriter(output_file, fourcc, fps, size, True)
        print "Writer is Open?",  out.isOpened()
        
        
        while not out.isOpened():
            print "Waiting for Writer"
            out = cv2.VideoWriter(output_file, fourcc, fps, (w,h))
        
    
    while cap.isOpened():
        flag, frame = cap.read()
        
        if flag:
            
    #        img = cv2.imread(frame)
            img = cv2.medianBlur(frame,5)
            cimg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            
            '''
            min-distance = 10
            canny-detector parameter = 100
            accumulator = 50
            minRadius = 10
            maxRadisu = 80
            '''
            new_circles = cv2.HoughCircles(cimg,cv2.cv.CV_HOUGH_GRADIENT,1,10,
                                param1=100,param2=50,minRadius=10,maxRadius=80)
            if new_circles is not None:
                circles = np.uint16(np.around(new_circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),4)
                # draw the center of the circle
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
            
            if write:
                out.write(img)
            if view:
                cv2.imshow('detected circles',img)
            pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) 
        else:
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame)
            print "frame is not ready"
            cv2.waitKey(1000)
        
        if cv2.waitKey(10) == 27:
            if write:
                out.release()
            cap.release()
            break
        if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
            if write:
                out.release()
            cap.release()
            break
    
    cv2.destroyAllWindows()