import cv2
import numpy as np
import detection_utils
import time
import ImageSource


class BallDetector:

    def __init__(self, cap, hsv_thresh_lower, hsv_thresh_upper, filter_mode, show_frames_on=True, input_scale=None, output_scale=None, print_frametime=False):
        self.hsv_thresh_lower = hsv_thresh_lower
        self.hsv_thresh_upper = hsv_thresh_upper
        self.cur_frame_dict = {}
        self.filter_mode = filter_mode
        self.cur_detected_balls = None
        self.show_frames_on = show_frames_on
        self.input_scale = input_scale
        self.output_scale = output_scale
        self.print_frametime = print_frametime

        self.image_source = ImageSource.ImageSource(cap)

    def preprocess_thresh(self):
        hsv = cv2.cvtColor(self.cur_frame_dict["raw"], cv2.COLOR_BGR2HSV)

        self.cur_frame_dict["mask"] = cv2.inRange(hsv, self.hsv_thresh_lower, self.hsv_thresh_upper)
        self.cur_frame_dict["masked"] = cv2.bitwise_and(self.cur_frame_dict["raw"], self.cur_frame_dict["raw"],
                                                        mask=self.cur_frame_dict["mask"])
        self.cur_frame_dict["gray"] = cv2.cvtColor(self.cur_frame_dict["masked"], cv2.COLOR_BGR2GRAY)
        self.cur_frame_dict["gray_blurred"] = cv2.blur(self.cur_frame_dict["gray"], (3, 3))
        self.cur_frame_dict["output"] = self.cur_frame_dict["raw"].copy()

        return self.cur_frame_dict["gray_blurred"]

    def preprocess_canny(self):
        self.cur_frame_dict["canny"] = cv2.Canny(self.cur_frame_dict["raw"], 100, 200)
        self.cur_frame_dict["output"] = self.cur_frame_dict["raw"].copy()
        return self.cur_frame_dict["canny"]

    def get_frame_to_hough(self):
        if self.filter_mode == "thresh":
            return self.preprocess_thresh()
        elif self.filter_mode == "canny":
            return self.preprocess_canny()
        else:
            raise Exception("Unknown filter mode" + str(self.filter_mode))

    def draw_circles(self):
        if self.cur_detected_balls is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_balls_int = np.uint16(np.around(self.cur_detected_balls))

            min_b = detected_balls_int[0, :][0][1]
            min_index = 0
            i = 0
            for pt in detected_balls_int[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                if b > min_b:
                    min_index = i
                    min_b = b

                # Draw the circumference of the circle.
                cv2.circle(self.cur_frame_dict["output"], (a, b), r, (0, 255, 0), 2)

                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(self.cur_frame_dict["output"], (a, b), 1, (0, 0, 255), 3)
                i += 1
            pt_min = detected_balls_int[0, :][min_index]
            a_min, b_min, r_min = pt_min[0], pt_min[1], pt_min[2]
            cv2.circle(self.cur_frame_dict["output"], (a_min, b_min), r, (255, 0, 0), 5)

    def show_frames(self):
        for im_name in self.cur_frame_dict.keys():
            im = self.cur_frame_dict.get(im_name)
            if self.output_scale:
                im = detection_utils.resize_with_aspect_ratio_rel(im, self.output_scale)

            cv2.imshow(im_name, im)

    def loop(self):
        prev = time.time()
        while True:
            raw = self.image_source.get_frame()

            if self.input_scale:
                self.cur_frame_dict["raw"] = detection_utils.resize_with_aspect_ratio_rel(raw, self.input_scale)
            else:
                self.cur_frame_dict["raw"] = raw

            frame_to_hough = self.get_frame_to_hough()
            self.cur_detected_balls = cv2.HoughCircles(frame_to_hough,
                                                cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                                param2=20, minRadius=10, maxRadius=30)

            self.draw_circles()

            if self.show_frames_on:
                self.show_frames()

            if self.print_frametime:
                t = time.time()
                print("Frametime (ms): " + str((t - prev) * 1000))
                prev = t

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
