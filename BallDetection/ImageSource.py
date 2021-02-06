import cv2
import numpy as np


class ImageSource:

    def __init__(self, cap: cv2.VideoCapture):
        self.cap = cap

    def get_frame(self) -> np.ndarray:
        _, frame = self.cap.read()
        return frame
