import cv2

def save(*args):
    return args

def gray_from_path(path:str):
    image = cv2.imread(path)
    if image is None:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def args(path, pimg, rimg):
    image = None
    if pimg:
        image = pimg
    elif rimg:
        image = cv2.cvtColor(rimg, cv2.COLOR_BGR2GRAY)
    elif path:
        image = gray_from_path(path)
    return image