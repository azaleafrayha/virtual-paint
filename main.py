import cv2 as cv
import numpy as np
import math

capture = cv.VideoCapture(0, cv.CAP_DSHOW) # 0 means the default webcam, if you have multiple webcams, you can change the number to 1, 2, etc.
# CAP_DSHOW is a flag that tells OpenCV to use the DirectShow backend for video capture, which is a Windows-specific API for capturing video from webcams and other video devices. It can help improve compatibility and performance when using certain webcams on Windows systems.

capture.set(3, 640) # 3 is a code number for the width of the webcam, 640 is the width in pixels
capture.set(4, 480) # 4 is a code number for the height of the webcam, 480 is the height in pixels
capture.set(10, 150) # 10 is a code number for the brightness of the webcam, 150 is the brightness value (0-255)

myColors = [[24, 28, 187, 57, 255, 255], # yellow -> [h_min, s_min, v_min, h_max, s_max, v_max]
            [175, 67, 142, 179, 255, 255]] # orange

myColorValues = [[0, 255, 222],
                 [0, 68, 255]] # in BGR format, these are the colors that will be used to draw the contours of the detected colors

myPoints = [] # [x, y, colorId] -> this list will store the points where the colors are detected, along with the color ID


def findColor(webcam, myColors, myColorValues):
    imgHSV = cv.cvtColor(webcam, cv.COLOR_BGR2HSV)
    count = 0 # count means the index of the color in the myColors list, which will be used to get the corresponding color value from myColorValues
    newPoints = [] # this list will store the new points detected in this frame
    for color in myColors:
        lower = np.array([color[0:3]]) # create a numpy array for the lower bound of the HSV values
        upper = np.array([color[3:6]]) 
        mask = cv.inRange(imgHSV, lower, upper) # filter the image to only show the colors within the specified range
        x, y = getContours(mask)
        if x != 0 and y != 0: # if a color is detected (x and y are not zero)
            newPoints.append([x, y, count]) 
        count += 1
    return newPoints

def getContours(webcam):
    x, y, width, height = 0, 0, 0, 0
    contours, hierarchy = cv.findContours(webcam, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #RETR EXTERNAL -> retrieves only the extreme outer contours, CHAIN_APPROX_NONE -> stores all the points of the contours
    for cnt in contours:
        area = cv.contourArea(cnt)
        print(area)
        if area > 500: # filter out small contours/noise
            #cv.drawContours(Result, cnt, -1, (0, 0, 255), 3) -> only to check if the contours are being detected correctly
            perimeter = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * perimeter, True) 
            x, y, width, height = cv.boundingRect(approx) # get the bounding box of the contour
    return x+width//2, y # x+width//2 is the center of the bounding box, y is the top of the bounding box

def drawOnCanvas(myPoints, myColorValues):
    for i in range(1, len(myPoints)): # we start from index 1 (not 0) bcs we need to check the previous point (to draw a line from the previous point to the current point)
        prevPoint = myPoints[i-1]
        currPoint = myPoints[i]
        
        if prevPoint[2] == currPoint[2]:
            distance = math.hypot(currPoint[0] - prevPoint[0], currPoint[1] - prevPoint[1]) # calculate the distance between the two points
            
            if distance < 50: # -> 50 pixels
                cv.line(Result, (prevPoint[0], prevPoint[1]), (currPoint[0], currPoint[1]), myColorValues[currPoint[2]], 5, cv.LINE_AA)
                        # (Result, initial coordinate, final coordinate, corresponding color to the color ID, thickness of 5 pixels, anti-aliased line)
            else:
                cv.line(Result, (prevPoint[0], prevPoint[1]), (currPoint[0], currPoint[1]), myColorValues[currPoint[2]], 5, cv.LINE_AA)
                # this is to avoid drawing lines when the color is not detected for a while
                
        # we don't need an else here because if the color ID is different, we only want to draw lines between points of the same color
        
while True:
    isTrue, webcam = capture.read()
    Result = webcam.copy() # we need to copy the webcam image to Result because we will draw on Result and not on the original webcam image
    newPoints = findColor(webcam, myColors, myColorValues)
    if len(newPoints) != 0: # if a color was detected in this frame
        for newP in newPoints:
            myPoints.append(newP) # we can't put a list inside a list, so we have to append each point individually (by this loop)
    
    if len(myPoints) != 0: # if there are any points in the myPoints list, we will draw them on the canvas
        drawOnCanvas(myPoints, myColorValues)

    cv.imshow("Result", Result)
    if cv.waitKey(1) & 0xFF == ord('q'):  
        break

capture.release()
cv.destroyAllWindows()

