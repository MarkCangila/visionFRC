import cv2
import numpy as np
import keyboard
import imutils

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_EXPOSURE, -10) #Set exposure lower

        self.value = 70 #For debugging

        self.portraitModeSixInchAreaHexagonThing = 2800

        self.hsvValues = {
            "baseHue": 70,
            "hueRange": 20,
            "lowerSaturation": 10,
            "upperSaturation": 250,
            "lowerValue": 10,
            "upperValue": 250
        }

    def find(self):
        _, img = self.cap.read() #Get frame of video

        #For more debugging
        if keyboard.is_pressed("q"):
            value += 1
            print(value)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Convert image to hsv for color detection

        #Lower and upper bounds of what is roughly green, will change later
        lower = np.array([self.hsvValues["baseHue"] - self.hsvValues["hueRange"], self.hsvValues["lowerSaturation"], self.hsvValues["lowerValue"]]) 
        upper = np.array([self.hsvValues["baseHue"] + self.hsvValues["hueRange"], self.hsvValues["upperSaturation"], self.hsvValues["upperValue"]]) 

        mask = cv2.inRange(hsv, lower, upper) #Color mask

        #Blur it to reduce noise, then expand it
        mask = cv2.medianBlur(mask, 15) #Block size 15
        mask = cv2.GaussianBlur(mask, (15, 15), 0) #Block size 15

        #Get edges of image
        edges = cv2.Canny(img, 40, 100) #Lower bound 40, upper of 100

        #Apply color mask to edges
        edges = cv2.bitwise_and(edges, edges, mask=mask)

        #Get contours of image
        cnts = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        visionTargets = []
        areas = []

        for c in cnts:
            M = cv2.moments(c) #Gets centers of contours
            if(M["m00"] != 0):
                #Gets center coordinates of contour
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                peri = cv2.arcLength(c, True) #Perimeter of contour
                approx = cv2.approxPolyDP(c, 0.01 * peri, True) #Poly approximation of contour, epsilon of 1% perimeter
                if len(approx) == 8:
                    #Append area and approx'ed points
                    visionTargets.append(approx)
                    areas.append(cv2.contourArea(c))

        cv2.imshow("mask", mask)
        cv2.imshow("image", img)
        cv2.imshow("edges", edges)

        if cv2.waitKey(5) & 0xFF == 27:
            return
        
        return [visionTargets, areas]
    cv2.destroyAllWindows()