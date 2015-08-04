#================================================================================
# PROJECT   : ASSISTED DRIVING BY ARTIFICIAL VISION                             *
#           : (DETECTING LINES ON THE NIGHT)                                    *
# VERSION   : 1.0                                                               *
# AUTHOR    : Jonas Carrillo Sisalima             jonascs1692@gmail.com         *
# PROFESSOR : Rodrigo Barba                       lrbarba@utpl.edu.ec           *
# COMPANY   : Sic ElectriTelecom  Loja-Ecuador                                  *
# DTAE      : 13/07/2015                                                        *
#================================================================================

#Import packages needed
import numpy as np
import math
import cv2

#call the video source
cap = cv2.VideoCapture('videos/video1.mp4')

w1 = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)  #Obtain video dimension x
h1 = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) #Obtain video dimension y
w=int(w1)
h=int(h1)

#Data for the region of interest
roiWid = w1
roiHig = h1
roiX = 0
roiY = int(h1/2)-270

#Process for lines on the road
def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope
    m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation
    theta1 = math.atan(m)                  #calculate the slope angle
    return theta1*(180/np.pi)              #Calculated angle in radians
    
while (cap.isOpened()):
    ret,frame1 = cap.read() 
    frame = cv2.resize(frame1,(600,600))                      #resize video source
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            #converted to gray
    equ = cv2.equalizeHist(gray)                              #Using histogram equalization function
    video = cv2.cvtColor(equ,cv2.COLOR_GRAY2BGR)
    cv2.rectangle(video, (roiX, roiY), (w,h ), (255, 0, 0),1) 
    
    hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)              #separate the processed image intensity   
    grayROI  = hsv[roiY:roiY+roiHig, roiX:roiX+roiWid]        #ROI
    
    low_white = np.array([0,0,250],dtype=np.uint8)            #lower parameter for filtering the image hsv
    high_white = np.array([255,255,255],dtype=np.uint8)       #Upper parameter for filtering the image hsv
    
    mask = cv2.inRange(grayROI,low_white,high_white)          #mask image with declared parameters
    #Length for lines to find
    minLineLength = 150
    maxLineGap = 20
    lines = cv2.HoughLinesP(mask,1,np.pi/180,10,minLineLength,maxLineGap)
    frameClone = frame.copy()
    for x1,y1,x2,y2 in lines[0]:
      if (round(x2-x1)!=0):
            arctan = slope(x1,x2,y1,y2)
            if (round(arctan>=round(-80)) and round(arctan<=round(-30))):
                cv2.line(frameClone,(x1 + roiX,y1 + roiY),(x2 + roiX,y2 + roiY),(0,255,0),2)
            if ( round(arctan>=round(30)) and round(arctan<=round(80))):
                cv2.line(frameClone,(x1 + roiX,y1 + roiY),(x2 + roiX,y2 + roiY),(0,255,0),2)
    #cv2.imshow('frame',mask)
    cv2.imshow('DETECTING LINES',frameClone)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
