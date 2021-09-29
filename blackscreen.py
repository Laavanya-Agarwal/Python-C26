import cv2
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.abi', fourcc, 20.0, (640, 480))

# starting camera
cam = cv2.VideoCapture(0)
time.sleep(5)

frame = cv2.resize(frame, (640, 480))
image = cv2.resize(image, (640, 480))

# when camera starts
while (cam.isOpened):
    ret, img = cam.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)

    lower_black = np.array([30, 30, 0])
    upper_black = np.array([104, 153, 70])

    mask = cv2.inRange(frame, lower_black, upper_black)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    f = frame - res
    f = np.where(f == 0, image, f)
    output_file.write(f)
    cv2.imshow('magic', f)
    cv2.waitKey(1)

# closing camera
cam.release()
out.release()
cv2.destroyAllWindows