import numpy as np


class PreprocessorInterface:

    def __init__(self):
        pass

    def preprocess(self, raw_img: np.ndarray) -> np.ndarray:
        pass
