class ImageSource:

    def __init__(self, cap):
        self.cap = cap

    def get_frame(self):
        _, frame = self.cap.read()
        return frame
