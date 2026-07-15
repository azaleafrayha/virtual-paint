import cv2 as cv
import numpy as np

# --- WEBCAM SETUP ---
capture = cv.VideoCapture(0, cv.CAP_DSHOW) # 0 means the default webcam, if you have multiple webcams, you can change the number to 1, 2, etc.
# CAP_DSHOW is a flag that tells OpenCV to use the DirectShow backend for video capture, which is a Windows-specific API for capturing video from webcams and other video devices. It can help improve compatibility and performance when using certain webcams on Windows systems.
capture.set(3, 640) # 3 is a code number for the width of the webcam, 640 is the width in pixels
capture.set(4, 480) # 4 is a code number for the height of the webcam, 480 is the height in pixels
capture.set(10, 150) # 10 is a code number for the brightness of the webcam, 150 is the brightness value (0-255)

# --- GET YOUR HSV VALUES ---
# ↳ run this function to get your HSV values for the color you want to track, then copy and paste the values into the myColors list in the main.py file
def empty(a):
    pass

cv.namedWindow("TrackBars") 
cv.resizeWindow("TrackBars", 640, 240)

cv.createTrackbar("Hue Min", "TrackBars", 0, 179, empty) 
cv.createTrackbar("Hue Max", "TrackBars", 0, 179, empty)
cv.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv.createTrackbar("Sat Max", "TrackBars", 0, 255, empty)
cv.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv.createTrackbar("Val Max", "TrackBars", 0, 255, empty)

while True:
    isTrue, webcam = capture.read()
    webcamHSV = cv.cvtColor(webcam, cv.COLOR_BGR2HSV) 

    h_min = cv.getTrackbarPos("Hue Min", "TrackBars") 
    h_max = cv.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv.getTrackbarPos("Val Max", "TrackBars")

    print(h_min, h_max, s_min, s_max, v_min, v_max) 

    lower = np.array([h_min, s_min, v_min]) 
    upper = np.array([h_max, s_max, v_max]) 
    mask = cv.inRange(webcamHSV, lower, upper) 

    Result = cv.bitwise_and(webcam, webcam, mask=mask) # apply the mask to the original image to get the result
    
    cv.imshow("Webcam", webcam)
    cv.imshow("Mask", mask)
    cv.imshow("Result", Result)
    
    if cv.waitKey(1) & 0xFF == ord('q'):  
        break
    
capture.release()
cv.destroyAllWindows()