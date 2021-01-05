import cv2

camera = cv2.VideoCapture(0)

while True:
        ret, im = camera.read()
        if not ret:
                print("failed to grab frame")

        scale = 2
        width = int(im.shape[1] * scale)
        height = int(im.shape[0] * scale)
        dim = (width, height)
        frame = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("Hdmi", frame)
        cv2.waitKey(1)
camera.release()
