import cv2
import numpy as np
import detection_utils
import time
import ImageSource
import PreprocessorInterface
import CannyPreprocessor
import ThresholdPreprocessor


class BallDetector:

    def __init__(self, cap, hsv_thresh_lower, hsv_thresh_upper, filter_mode, show_frames_on=True, input_scale=None, output_scale=None, print_frametime=False):
        self.hsv_thresh_lower = hsv_thresh_lower
        self.hsv_thresh_upper = hsv_thresh_upper
        self.cur_detected_balls = None
        self.show_frames_on = show_frames_on
        self.input_scale = input_scale
        self.output_scale = output_scale
        self.print_frametime = print_frametime
        self.output_img = None

        self.image_source = ImageSource.ImageSource(cap)

        self.preprocessor = self.get_preprocessor(filter_mode, hsv_thresh_lower, hsv_thresh_upper)

    @staticmethod
    def get_preprocessor(filter_mode, hsv_thresh_lower, hsv_thresh_upper):
        if filter_mode == "canny":
            return CannyPreprocessor.CannyPreprocessor()
        elif filter_mode == "thresh":
            return ThresholdPreprocessor.ThresholdPreprocessor(hsv_thresh_lower, hsv_thresh_upper)
        else:
            raise Exception("Unknown preprocessing mode: " + str(filter_mode))

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
                cv2.circle(self.output_img, (a, b), r, (0, 255, 0), 2)

                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(self.output_img, (a, b), 1, (0, 0, 255), 3)
                i += 1
            pt_min = detected_balls_int[0, :][min_index]
            a_min, b_min, r_min = pt_min[0], pt_min[1], pt_min[2]
            cv2.circle(self.output_img, (a_min, b_min), r, (255, 0, 0), 5)

    def show_frames(self):
        if self.output_scale:
            self.output_img = detection_utils.resize_with_aspect_ratio_rel(self.output_img, self.output_scale)

        cv2.imshow("output", self.output_img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            quit()

    def detect_balls(self):
        prev = time.time()
        raw = self.image_source.get_frame()

        if self.input_scale:
            raw = detection_utils.resize_with_aspect_ratio_rel(raw, self.input_scale)

        self.output_img = raw.copy()

        frame_to_hough = self.preprocessor.preprocess(raw)
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

        return self.cur_detected_balls

