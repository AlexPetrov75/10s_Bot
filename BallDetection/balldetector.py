import cv2
import numpy as np
import detection_utils


class BallDetector:

    def __init__(self, cap, hsv_thresh_lower, hsv_thresh_upper):
        self.hsv_thresh_lower = hsv_thresh_lower
        self.hsv_thresh_upper = hsv_thresh_upper
        self.cap = cap

    def loop(self):
        while True:
            im_dict = {}

            _, im_dict["frame"] = self.cap.read()

            hsv = cv2.cvtColor(im_dict["frame"], cv2.COLOR_BGR2HSV)

            lower_yellow = np.array([23, 10, 187], dtype=np.uint8)
            upper_yellow = np.array([89, 190, 255], dtype=np.uint8)

            im_dict["mask"] = cv2.inRange(hsv, lower_yellow, upper_yellow)
            # im_dict["frame_gray"] = cv2.cvtColor(im_dict["frame"], cv2.COLOR_BGR2GRAY)
            im_dict["masked"] = cv2.bitwise_and(im_dict["frame"], im_dict["frame"], mask=im_dict["mask"])
            im_dict["gray"] = cv2.cvtColor(im_dict["masked"], cv2.COLOR_BGR2GRAY)
            im_dict["gray_blurred"] = cv2.blur(im_dict["gray"], (3, 3))

            im_dict["output"] = im_dict["frame"].copy()
            im_dict["canny"] = cv2.Canny(im_dict["frame"], 100, 200)

            detected_circles = cv2.HoughCircles(im_dict["canny"],
                                                cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                                param2=20, minRadius=10, maxRadius=30)

            # Draw circles that are detected.
            if detected_circles is not None:

                # Convert the circle parameters a, b and r to integers.
                detected_circles = np.uint16(np.around(detected_circles))

                min_b = detected_circles[0, :][0][1]
                min_index = 0
                i = 0
                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]
                    if b > min_b:
                        min_index = i
                        min_b = b

                    # Draw the circumference of the circle.
                    cv2.circle(im_dict["output"], (a, b), r, (0, 255, 0), 2)

                    # Draw a small circle (of radius 1) to show the center.
                    cv2.circle(im_dict["output"], (a, b), 1, (0, 0, 255), 3)
                    i += 1
                pt_min = detected_circles[0, :][min_index]
                a_min, b_min, r_min = pt_min[0], pt_min[1], pt_min[2]
                cv2.circle(im_dict["output"], (a_min, b_min), r, (255, 0, 0), 5)

            for im_name in im_dict.keys():
                im_resized = detection_utils.resize_with_aspect_ratio(im_dict.get(im_name), width=500)
                cv2.imshow(im_name, im_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
