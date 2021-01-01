import numpy as np
import cv2
import imutils
from imutils.video import WebcamVideoStream

camera = WebcamVideoStream(src=0).start()
obs = camera.read()

def transposer(image):
    if len(image.shape) == 3:
        return np.transpose(image, (2, 0, 1))
    return np.transpose(image, (0, 3, 1, 2))


print(transposer(obs))
