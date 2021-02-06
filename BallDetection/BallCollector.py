import BallDetector
import cv2


class BallCollector:

    def __init__(self, cap, hsv_thresh_lower, hsv_thresh_upper, filter_mode, show_frames_on=True, input_scale=None,
                 output_scale=None, print_frametime=False):

        self.ball_detector = BallDetector.BallDetector(cap, hsv_thresh_lower, hsv_thresh_upper, filter_mode,
                                                       show_frames_on=show_frames_on, input_scale=input_scale,
                                                       output_scale=output_scale, print_frametime=print_frametime)
        self.detected_balls = None

    def loop(self):
        while True:
            self.ball_detector.detect_balls()
            self.detected_balls = self.ball_detector.detect_balls()

