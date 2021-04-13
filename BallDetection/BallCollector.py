import BallDetector
import cv2


class BallCollector:

    def __init__(self, source_type, hsv_thresh_lower, hsv_thresh_upper, filter_mode, show_frames_on=True, input_scale=None,
                 output_scale=None, print_frametime=False, vid_file_path=None):

        self.ball_detector = BallDetector.BallDetector(source_type, hsv_thresh_lower, hsv_thresh_upper, filter_mode,
                                                       show_frames_on=show_frames_on, input_scale=input_scale,
                                                       output_scale=output_scale, print_frametime=print_frametime, vid_file_path=vid_file_path)
        self.detected_balls = None

    def loop(self):
        while True:
            self.ball_detector.detect_balls()
            self.detected_balls = self.ball_detector.detect_balls()

