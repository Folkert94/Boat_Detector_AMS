import cv2
import numpy as np
import time
from datetime import datetime
import os

cam = cv2.VideoCapture('http://192.168.178.33/live')

previous = time.time()
delta = 0

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y %H_%M_%S")

fpath = 'stream_log/' + dt_string.split()[0]
isDirectory = os.path.isdir(fpath)
if not isDirectory:
    try:
        os.mkdir(fpath)
    except OSError:
        print ("Creation of the directory %s failed" % fpath)
    else:
        print ("Successfully created the directory %s " % fpath)

time_interval = 3
frame = None

while True:
    current = time.time()
    delta += current - previous
    previous = current


    if delta > time_interval:
        motion = 0
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
        print("checking frame ", time.time())
        if frame is None:
            frame = img
            continue

        temp_frame = img

        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame1=cv2.GaussianBlur(gray_frame,(25,25),0)

        gray_frame=cv2.cvtColor(temp_frame,cv2.COLOR_BGR2GRAY)
        frame2=cv2.GaussianBlur(gray_frame,(25,25),0)

        delta=cv2.absdiff(frame1,frame2)
        threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(threshold, None, iterations = 2) 
        
        # Finding contour of moving object 
        cnts,_ = cv2.findContours(thresh_frame.copy(),  
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        for contour in cnts: 
            if cv2.contourArea(contour) < 10000: 
                continue
                cv2.destroyAllWindows()
            print("movement detected")
            motion = 1
    
            # (x, y, w, h) = cv2.boundingRect(contour) 
            # cv2.rectangle(temp_frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 

        if motion == 1:
            cv2.imshow('image', temp_frame)
            print("writing frame ", time.time())
            cv2.imwrite("stream_log/{}/{}.bmp".format(dt_string.split()[0], dt_string.split()[1]), temp_frame)
            motion = 0

        frame = img
        delta = 0

    _, img = cam.read()
    cv2.waitKey(1)