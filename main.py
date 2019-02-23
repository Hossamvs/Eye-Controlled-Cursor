import numpy as np
import cv2
import win32api 

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
left_eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')
cap = cv2.VideoCapture(0) #0 is first webcam, #1 is second ...etc

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w, y+h), (255,0,0), 2)
        cv2.putText(frame,"Face",(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        left_eye = left_eye_cascade.detectMultiScale(roi_gray,3,5) #detect objects in first bounding box
        right_eye = right_eye_cascade.detectMultiScale(roi_gray,3,5)
        for(lex,ley,lew,leh) in left_eye:
            cv2.rectangle(roi_color, (lex,ley),(lex+lew, ley+leh), (0,0,255), 1)
            cv2.putText(roi_color,"left eye",(lex-10,ley-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            # roi_gray_eye = roi_gray[ley:ley+leh, lex:lex+lew]
            # roi_color_eye = roi_color[ley:ley+leh, lex:lex+lew]
            # circles = cv2.HoughCircles(roi_gray,cv2.HOUGH_GRADIENT,1.2,100)
            # if circles is not None:
            #     circles = np.round(circles[0,:]).astype("int")
            #     for(ix,iy,ir) in circles:
            #         cv2.circle(roi_color_eye, (ix,iy),ir, (0,255,0),2)
        for(rex,rey,rew,reh) in right_eye:
            cv2.rectangle(roi_color, (rex,rey),(rex+rew, rey+reh), (255,255,0), 1)
            cv2.putText(roi_color,"right eye",(rex-10,rey-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),1) 

    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('gray',gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()