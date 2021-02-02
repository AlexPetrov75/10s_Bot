import cv2 as cv
import sys
import numpy as np

focalLen = 485.82423388827533
principalX = 134.875
principalY = 239.875

#parse args
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "file_path")

cap = cv.VideoCapture(sys.argv[1])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        if frame is None:
            break
        print("can't read")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9,9), 2)

    rows = blur.shape[0]
    circle = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, rows / 8, param1=100, 
                              param2=30, minRadius=1, maxRadius=70)

    if circle is not None:
            circle = np.uint16(np.around(circle))
            for i in circle[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                cv.circle(frame, center, radius, (0, 0, 255), 1)

                camX = (i[0]-principalX) / focalLen
                camY = (i[0]-principalY) / focalLen

                Z = focalLen*(3/radius)
                cv.putText(frame, str(int(Z))+'cm', (i[0]-30, i[1]), 
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),
                           1,cv.LINE_AA)

                X = ((i[0] - principalX)*Z)/focalLen
                Y = ((i[1] - principalY)*Z)/focalLen
                print("X:",X,"\nY:",Y, "\ncamera coords:", camX,",", camY, "\n")

    cv.imshow('frame', frame)
    k = cv.waitKey(1)
    if k == ord('s') or k == 27:
        break

cap.release()
    