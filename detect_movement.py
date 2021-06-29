import cv2

image1 = cv2.imread("stream_log/28_11_2020/14_27_28.bmp")
image2 = cv2.imread("stream_log/28_11_2020/14_27_38.bmp")

# blur the image to ignore water ripples
gray_frame=cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
frame1=cv2.GaussianBlur(gray_frame,(25,25),0)

gray_frame=cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
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
        motion = 1
  
        (x, y, w, h) = cv2.boundingRect(contour) 
        # making green rectangle arround the moving object 
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 3) 

cv2.imshow('image',image2)
cv2.waitKey(0)
cv2.destroyAllWindows()
