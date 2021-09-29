import cv2
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.abi', fourcc, 20.0, (640, 480))

# starting camera
cam = cv2.VideoCapture(0)
time.sleep(5)

# setting up background
bg = 0
for i in range(60):
    ret, bg = cam.read()
bg = np.flip(bg, axis = 1)

# when camera starts
while (cam.isOpened):
    ret, img = cam.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #mask 1 - has red
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    #mask 2
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red2, upper_red2)
    #mixing them
    mask_1 = mask_1 + mask_2

    # removing red color
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    # wherever mask 1 (red) isn't there, store in mask 2
    mask_2 = cv2.bitwise_not(mask_1)

    # take bg + removed part
    res1 = cv2.bitwise_and(img, img, mask = mask_2)
    res2 = cv2.bitwise_and(bg, bg, mask = mask_1)
    # add them together
    finaloutput = cv2.addWeighted(res1, 1, res2, 1, 0)

    #final output
    output_file.write(finaloutput)
    cv2.imshow('magic', finaloutput)
    cv2.waitKey(1)

# closing camera
cam.release()
out.release()
cv2.destroyAllWindows