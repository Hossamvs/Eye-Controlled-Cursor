import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx   #to get screen coordinates and size

mouse=Controller() #init mouse object

app=wx.App(False) 
(sx,sy) = wx.GetDisplaySize()
(camx,camy) = (320,240) #define resolution

#lowerBound = np.array([33,80,40])#hsv values
#upperBound = np.array([102,255,255])
lowerBound=np.array([40,80,40])
upperBound=np.array([65,225,255])

cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy) #capturing the image

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0

while True:
    ret, image=cam.read()

    #convert image to hsv and create a mask within the color ranges
    imgHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen) #kernel opening is to remove random dots 
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose) #kernel closing is to remove random holes
    
    maskFinal=maskClose
    _,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #conts contains a list of contours
    #basically we find a list of the contours in the image "maskFinal" #CHAIN_APPROX_NONE is to store all possible subsequent contour points
    #RETR_EXTERLNAL is to retrive the outer contours
    if(len(conts)==2):
        if(pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(image,(int(x1),int(y1)),(int(x1+w1),int(y1+h1)),(255,0,0),2)
        cv2.rectangle(image,(int(x2),int(y2)),(int(x2+w2),int(y2+h2)),(255,0,0),2)#bounding boxes
        cx1=x1+w1/2 
        cy1=y1+h1/2
        cx2=x2+w2/2
        cy2=y2+h2/2 #get center of bounding boxes to draw line
        cx=(cx1+cx2)/2
        cy=(cy1+cy2)/2
        cv2.line(image, (int(cx1),int(cy1)),(int(cx2),int(cy2)),(255,0,0),2)#line and dot
        cv2.circle(image, (int(cx),int(cy)),2,(0,0,255),2)
        mouseLoc=(int(sx-(cx*sx/camx)), int(cy*sy/camy)) #move mouse accordingly
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pinchFlag==0):
            pinchFlag=1
            #mouse.press(Button.left)
        cv2.rectangle(image,(int(x),int(y)),(int(x+w),int(y+h)),(255,0,0),2)
        cx=x+w/2
        cy=y+h/2
        cv2.circle(image,(int(cx),int(cy)),int((w+h)/4),(0,0,255),2)
        mouseLoc=(int(sx-(cx*sx/camx)), int(cy*sy/camy))
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass    

    #cv2.imshow("maskClose",maskClose)
    #cv2.imshow("maskOpen",maskOpen)
    #cv2.imshow("mask",mask)
    cv2.imshow("cam",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()



