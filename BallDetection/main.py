import cv2
import os
import BallDetector
import BallCollector
import numpy as np

if __name__ == "__main__":
    lower_yellow = np.array([23, 10, 187], dtype=np.uint8)
    upper_yellow = np.array([89, 190, 255], dtype=np.uint8)
    bc = BallCollector.BallCollector("picamera", lower_yellow, upper_yellow, "canny", input_scale=0.5, print_frametime=True)
    bc.loop()