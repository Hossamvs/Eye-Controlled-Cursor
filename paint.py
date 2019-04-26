    
import numpy as np
import cv2
from collections import deque

# Define the upper and lower boundaries for a color to be considered "Blue"
blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# Setup deques to store separate colors in separate arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]
blpoints = [deque(maxlen=512)]

bindex = 0
gindex = 0
rindex = 0
yindex = 0
blindex = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (0, 0, 0)]
colorIndex = 0

# Setup the Paint interface
canvas = np.zeros((600,800,3)) + 255
canvas = cv2.rectangle(canvas, (40,0), (140,65), (100,0,0), 2)
canvas = cv2.rectangle(canvas, (40,85), (140,150), colors[0], -1)
canvas = cv2.rectangle(canvas, (40,170), (140,235), colors[1], -1)
canvas = cv2.rectangle(canvas, (40,255), (140,320), colors[2], -1)
canvas = cv2.rectangle(canvas, (40,340), (140,405), colors[3], -1)
canvas = cv2.rectangle(canvas, (40,425), (140,490), colors[4], -1)

cv2.putText(canvas, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(canvas, "BLUE", (55, 118), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(canvas, "GREEN", (55, 203), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(canvas, "RED", (55, 288), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(canvas, "YELLOW", (55, 373), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.putText(canvas, "BLACK", (55, 458), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Load the video
camera = cv2.VideoCapture(0)

while True:
    # Grab the current canvas
    (grabbed, originalFrame) = camera.read()
    frame = cv2.resize(originalFrame, (800,600))
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Add the coloring options to the frame
    frame = cv2.rectangle(frame, (40,0), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (40,85), (140,150), colors[0], -1)
    frame = cv2.rectangle(frame, (40,170), (140,235), colors[1], -1)
    frame = cv2.rectangle(frame, (40,255), (140,320), colors[2], -1)
    frame = cv2.rectangle(frame, (40,340), (140,405), colors[3], -1)
    frame = cv2.rectangle(frame, (40,425), (140,490), colors[4], -1)

    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (55, 118), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (55, 203), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (55, 288), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (55, 373), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLACK", (55, 458), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

    # Check to see if we have reached the end of the video
    if not grabbed:
        break

    # Determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # Find contours in the image
    (_, cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Check to see if any contours were found
    # Another approach would be to check if we have one and only one contour to work with to avoid confusion
    if len(cnts) > 0:
    	# Sort the contours and find the largest one
    	# will assume this contour correspondes to the area of rhe object
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Get the moments to calculate the center of the contour (in this case Circle)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        #1 is Y  #0 is X
        if center[0] <= 140:
            if 0 <= center[1] <= 65: # Clear All
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                blpoints = [deque(maxlen=512)]

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0
                blindex = 0

                canvas[:,140:,:] = 255
            elif 85 <= center[1] <= 150:
                    colorIndex = 0 # Blue
            elif 170 <= center[1] <= 235:
                    colorIndex = 1 # Green
            elif 255 <= center[1] <= 320:
                    colorIndex = 2 # Red
            elif 340 <= center[1] <= 405:
                    colorIndex = 3 # Yellow
            elif 425 <= center[1] <= 490:
                    colorIndex = 4 # Black
        else :
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)
            elif colorIndex == 4:
                blpoints[blindex].appendleft(center)
    # Append the next deque when no contours are detected
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1
        blpoints.append(deque(maxlen=512))
        blindex += 1
    # Draw lines of all the colors (Blue, Green, Red , Yellow and Black)
    points = [bpoints, gpoints, rpoints, ypoints , blpoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(canvas, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Show the frame and the canvas image
    

    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", canvas)
    #cv2.imshow("mask", blueMask)

	# If the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()