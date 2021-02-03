import cv2


def resize_with_aspect_ratio_rel(image, scale_ratio, inter=cv2.INTER_AREA):
    width = int(image.shape[1] * scale_ratio)
    height = int(image.shape[0] * scale_ratio)
    dsize = (width, height)
    output = cv2.resize(image, dsize)
    return output


def resize_with_aspect_ratio_abs(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)