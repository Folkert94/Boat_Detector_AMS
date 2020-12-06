import cv2
import numpy as np
import time
from datetime import datetime
import os

# Create a new VideoCapture object
cam = cv2.VideoCapture('http://192.168.178.33/live')

# Initialise variables to store current time difference as well as previous time call value
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



# Keep looping
while True:
    # Get the current time, increase delta and update the previous variable
    current = time.time()
    delta += current - previous
    previous = current

    # Check if 3 (or some other value) seconds passed
    if delta > 10:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
        print("grabbing frame ", time.time())
        cv2.imwrite("stream_log/{}/{}.bmp".format(dt_string.split()[0], dt_string.split()[1]), img)
        # Operations on image
        # Reset the time counter
        delta = 0

    # Show the image and keep streaming
    _, img = cam.read()
    cv2.waitKey(1)