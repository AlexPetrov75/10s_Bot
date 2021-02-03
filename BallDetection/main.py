import cv2
import os
import balldetector
import numpy as np

if __name__ == "__main__":
    test_vid_path = os.path.join(os.getcwd(), "Test", "tennisballwizard.mp4")
    cap = cv2.VideoCapture(test_vid_path)
    lower_yellow = np.array([23, 10, 187], dtype=np.uint8)
    upper_yellow = np.array([89, 190, 255], dtype=np.uint8)
    bd = balldetector.BallDetector(cap, lower_yellow, upper_yellow, "thresh", output_scale=0.5)
    bd.loop()