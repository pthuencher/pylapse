# 3rd pary imports
import cv2

def crop(img, crop):
    dx = crop[0]
    dy = crop[1]
    return img[dx[0]:dx[1], dy[0]:dy[1]]

def resize(img, resize):
    return cv2.resize(img, resize, interpolation=cv2.INTER_LINEAR)
