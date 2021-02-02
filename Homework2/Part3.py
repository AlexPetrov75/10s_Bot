import cv2 as cv
import sys
import numpy as np
import math as math


def main():
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
                                param2=30, minRadius=1, maxRadius=60)

        if circle is not None:
                circle = np.uint16(np.around(circle))
                count = 0
                for i in circle[0, :]:
                    center = (i[0], i[1])
                    radius = i[2]
                    cv.circle(frame, center, radius, (0, 0, 255), 1)

                    Z = focalLen*(3/radius)
                    cv.putText(frame, str(int(Z))+'cm', (i[0]-30, i[1]), 
                            cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),
                            1,cv.LINE_AA)

                    X = ((i[0] - principalX)*Z)/focalLen
                    Y = ((i[1] - principalY)*Z)/focalLen
                    # print("X:",X,"\nY:",Y, "\n")

                    bf_right = Projection(X-3, Y-3, Z-3, focalLen, principalX, principalY)
                    tf_right = Projection(X-3, Y+3, Z-3, focalLen, principalX, principalY)
                    bf_left = Projection(X+3, Y-3, Z-3, focalLen, principalX, principalY)
                    tf_left = Projection(X+3, Y+3, Z-3, focalLen, principalX, principalY)
                    bb_right = Projection(X-3, Y-3, Z+3, focalLen, principalX, principalY)
                    tb_right = Projection(X-3, Y+3, Z+3, focalLen, principalX, principalY)
                    bb_left = Projection(X+3, Y-3, Z+3, focalLen, principalX, principalY)
                    tb_left = Projection(X+3, Y+3, Z+3, focalLen, principalX, principalY)

                    #draw front box
                    frame = draw_line(frame, bf_right, tf_right)
                    frame = draw_line(frame, tf_left, tf_right)
                    frame = draw_line(frame, bf_left, tf_left)
                    frame = draw_line(frame, bf_right, bf_left)

                    #draw back box
                    frame = draw_line(frame, bb_right, tb_right)
                    frame = draw_line(frame, tb_left, tb_right)
                    frame = draw_line(frame, bb_left, tb_left)
                    frame = draw_line(frame, bb_right, bb_left)

                    #connect them
                    frame = draw_line(frame, tf_right, tb_right)
                    frame = draw_line(frame, tf_left, tb_left)
                    frame = draw_line(frame, bf_left, bb_left)
                    frame = draw_line(frame, bf_right, bb_right)

                    count += 1

        cv.imshow('frame', frame)
        k = cv.waitKey(1)
        if k == ord('s') or k == 27:
            break

    cap.release()


def Projection(X,Y,Z,focalLen,cx,cy):
    proj_x = (focalLen*(X/Z))+cx
    proj_y = (focalLen*(Y/Z))+cy

    return (int(proj_x), int(proj_y))

def draw_line(frame, coords1, coords2):
    cv.line(frame, coords1, coords2, (0,0,255), 1)
    return frame

if __name__ == "__main__":
    main()