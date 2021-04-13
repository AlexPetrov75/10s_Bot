import cv2
import numpy as np
import time
import picamera
import picamera.array


class ImageSource:

    def __init__(self, source_type: str, vid_file_path=None):
        self.source_type = source_type
        self.vid_file_path = vid_file_path

        if source_type == "file":
            if not vid_file_path:
                raise Exception("To use a video file as the source, provide a file path as vid_file_path kwarg")
            self.cap = cv2.VideoCapture(vid_file_path)
        elif source_type == "picamera":
            self.pi_camera = picamera.PiCamera()
            self.pi_camera.resolution = (640, 480)
            self.pi_camera.framerate = 32
            time.sleep(0.1)  # Allow camera to warm up
        else:
            raise Exception(source_type + "is not a valid image source type.")

    def get_frame_from_file(self) -> np.ndarray:
        _, frame = self.cap.read()
        return frame

    def get_frame_from_picamera(self):
        stream = picamera.array.PiRGBArray(self.pi_camera)
        self.pi_camera.capture(stream, format="bgr")
        return stream.array

    def get_frame(self):
        if self.source_type == "file":
            return self.get_frame_from_file()
        elif self.source_type == "picamera":
            return self.get_frame_from_picamera()

