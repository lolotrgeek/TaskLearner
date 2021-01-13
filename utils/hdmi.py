import cv2

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
while True:
    ret, im = camera.read()
    if not ret:
        print("failed to grab frame")

    cv2.imshow("Hdmi", im)
    key = cv2.waitKeyEx(1)
    if key & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
