import cv2 as cv
import numpy as np
import math

# --- WEBCAM SETUP ---
capture = cv.VideoCapture(0, cv.CAP_DSHOW) # 0 means the default webcam, if you have multiple webcams, you can change the number to 1, 2, etc.
capture.set(3, 640) # 3 is a code number for the width of the webcam, 640 is the width in pixels
capture.set(4, 480) # 4 is a code number for the height of the webcam, 480 is the height in pixels
capture.set(10, 150) # 10 is a code number for the brightness of the webcam, 150 is the brightness value (0-255)

# --- COLOR CONFIGURATION ---
myColors = [[24, 28, 187, 57, 255, 255], # -> [h_min, s_min, v_min, h_max, s_max, v_max]
            [175, 67, 142, 179, 255, 255]]

myColorValues = [[0, 255, 222],  # -> in BGR format, these are the colors that will be used to draw the contours of the detected colors
                 [0, 68, 255]] 

def getContours(mask):
    x, y, width, height = 0, 0, 0, 0
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #RETR EXTERNAL -> retrieves only the extreme outer contours, CHAIN_APPROX_NONE -> stores all the points of the contours
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500: # filter out small contours/noise
            perimeter = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * perimeter, True) 
            x, y, width, height = cv.boundingRect(approx) # get the bounding box of the contour
    return x+width//2, y # x+width//2 is the center of the bounding box, y is the top of the bounding box

def findColor(webcam, myColors):
    imgHSV = cv.cvtColor(webcam, cv.COLOR_BGR2HSV)
    currentFramePoints = [] 
    
    for color in myColors:
        lower = np.array([color[0:3]])
        upper = np.array([color[3:6]]) 
        mask = cv.inRange(imgHSV, lower, upper) # filter the image to only show the colors within the specified range
        x, y = getContours(mask)
        currentFramePoints.append([x, y])
    return currentFramePoints

imgCanvas = np.zeros((480, 640, 3), np.uint8) # -> (height, width, channels), this is the canvas on which we will draw the lines
prevPoints = [[0, 0] for _ in range(len(myColors))] # -> [x,y], [x,y] for each color automatically
        
while True:
    isTrue, webcam = capture.read()
    Result = webcam.copy() # we need to copy the webcam image to Result because we will draw on Result and not on the original webcam image
    
    # get the current points of the detected colors
    currentPoints = findColor(webcam, myColors) 
    
    # DYNAMIC LOOP FOR EVERY COLOR
    for i in range(len(currentPoints)):
        x, y = currentPoints[i][0], currentPoints[i][1]
        px, py = prevPoints[i][0], prevPoints[i][1]
        
        if x != 0 and y != 0: # a color was detected
            if px != 0 and py != 0: # a color was detected in the previous frame
                cv.line(imgCanvas, (px, py), (x, y), myColorValues[i], 5, cv.LINE_AA) # draw a line from the previous point to the current point with the specified color and thickness of 5
                
            prevPoints[i] = [x, y] # update the previous point to the current point
        else:
            prevPoints[i] = [0, 0] # reset the previous point if no color was detected
    
    # overlay the imgCanvas on top of the Result image, so that we can see the lines drawn on the canvas
    Result[imgCanvas > 0] = imgCanvas[imgCanvas > 0]
    
    cv.imshow("Result", Result)
    if cv.waitKey(1) & 0xFF == ord('q'):  
        break

capture.release()
cv.destroyAllWindows()

