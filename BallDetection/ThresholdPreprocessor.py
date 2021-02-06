from PreprocessorInterface import PreprocessorInterface
import cv2
import numpy as np


class ThresholdPreprocessor(PreprocessorInterface):

    def __init__(self, hsv_thresh_lower: np.array, hsv_thresh_upper: np.array):
        super().__init__()
        self.hsv_thresh_lower = hsv_thresh_lower
        self.hsv_thresh_upper = hsv_thresh_upper

    def preprocess(self, raw_img: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(raw_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.hsv_thresh_lower, self.hsv_thresh_upper)
        masked = cv2.bitwise_and(raw_img, raw_img, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.blur(gray, (3, 3))
        return gray_blurred
