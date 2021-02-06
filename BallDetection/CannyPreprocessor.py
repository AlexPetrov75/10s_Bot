from PreprocessorInterface import PreprocessorInterface
import numpy as np
import cv2


class CannyPreprocessor(PreprocessorInterface):

    def __init__(self):
        super().__init__()

    def preprocess(self, raw_img: np.ndarray):
        return cv2.Canny(raw_img, 50, 100)
