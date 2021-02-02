import cv2 as cv
import sys
import numpy as np

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


    cv.imshow('frame', frame)
    k = cv.waitKey(1)
    if k == ord('s') or k == 27:
        break

cap.release()
    