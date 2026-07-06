import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0, cv.CAP_DSHOW) # 0 means the default webcam, if you have multiple webcams, you can change the number to 1, 2, etc.
# CAP_DSHOW is a flag that tells OpenCV to use the DirectShow backend for video capture, which is a Windows-specific API for capturing video from webcams and other video devices. It can help improve compatibility and performance when using certain webcams on Windows systems.

capture.set(3, 640) # 3 is a code number for the width of the webcam, 640 is the width in pixels
capture.set(4, 480) # 4 is a code number for the height of the webcam, 480 is the height in pixels
capture.set(10, 150) # 10 is a code number for the brightness of the webcam, 150 is the brightness value (0-255)

myColors = [[165, 82, 81, 170, 140, 255], # pink -> [h_min, s_min, v_min, h_max, s_max, v_max]
            [26, 21, 157, 41, 255, 255], # yellow
            [175, 67, 142, 179, 255, 255]] # orange

def findColor(webcam, myColors):
    imgHSV = cv.cvtColor(webcam, cv.COLOR_BGR2HSV)
    lower = np.array([myColors[0][0:3]]) # create a numpy array for the lower bound of the HSV values
    upper = np.array([myColors[0][3:6]]) 
    mask = cv.inRange(imgHSV, lower, upper) # filter the image to only show the colors within the specified range
    cv.imshow("Mask", mask)

while True:
    isTrue, webcam = capture.read()
    cv.imshow("Result", webcam)
    findColor(webcam, myColors)
    if cv.waitKey(1) & 0xFF == ord('q'):  
        break
    
capture.release()
cv.destroyAllWindows()

