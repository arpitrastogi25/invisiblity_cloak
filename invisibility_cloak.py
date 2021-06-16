import cv2
import numpy as np
import time

print(cv2.__version__)
capture_video = cv2.VideoCapture(0)
background = 0
h_min = 140
h_max = 179
s_min = 92
s_max = 255
v_min = 0
v_max = 255
hsv_calibrated = 0

def empty(a):
    pass

def calibrate_hsv():
    cv2.namedWindow('Calibrate',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Calibrate',400,400)
    img = 255 * np.ones((50, 400, 3), np.uint8)
    cv2.putText(img, "Press \'s\' to save HSV values.", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 0), 2)
    cv2.imshow('Calibrate', img)
    cv2.createTrackbar('Hue min','Calibrate',h_min,179,empty)
    cv2.createTrackbar('Hue max','Calibrate',h_max,179,empty)
    cv2.createTrackbar('Sat min','Calibrate',s_min,255,empty)
    cv2.createTrackbar('Sat max','Calibrate',s_max,255,empty)
    cv2.createTrackbar('Val min','Calibrate',v_min,255,empty)
    cv2.createTrackbar('Val max','Calibrate',v_max,255,empty)


def findMask(img):
    global hsv_calibrated, h_min, h_max, s_min, s_max, v_min, v_max
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if (hsv_calibrated == 0):
        h_min = cv2.getTrackbarPos('Hue min', 'Calibrate')
        h_max = cv2.getTrackbarPos('Hue max', 'Calibrate')
        s_min = cv2.getTrackbarPos('Sat min', 'Calibrate')
        s_max = cv2.getTrackbarPos('Sat max', 'Calibrate')
        v_min = cv2.getTrackbarPos('Val min', 'Calibrate')
        v_max = cv2.getTrackbarPos('Val max', 'Calibrate')

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imghsv, lower, upper)

    median = cv2.medianBlur(mask, 25)
    if (hsv_calibrated == 0):
        cv2.imshow("mask", median)
    return median


def main():
    time.sleep(1)
    count = 0
    global hsv_calibrated
    calibrate = input('1. Do you want to calibrate the HSV value of the mask ? [y/n] ')
    if not (calibrate=='y' or calibrate == 'Y'):
        hsv_calibrated = 1
    else:
        calibrate_hsv()
        while True:
            return_val, background = capture_video.read()
            if return_val == False:
                continue
            background = np.flip(background, axis=1)
            findMask(background)
            cv2.imshow('frame', background)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.destroyWindow('Calibrate')
                cv2.destroyWindow('frame')
                cv2.destroyWindow('mask')
                hsv_calibrated = 1
                break

    print('2. Press space to capture background.')
    while True:
        return_val, background = capture_video.read()
        if return_val == False:
            continue
        background = np.flip(background, axis = 1)
        cv2.imshow('frame',background)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.destroyWindow('frame')
            break

    print('3. Displaying final Video with Invisivility cloak ! (Press \'q\' to exit)')
    while (capture_video.isOpened()):
        return_val, img = capture_video.read()
        if not return_val :
            break
        count = count + 1
        img = np.flip(img, axis = 1)
        mask = findMask(img)
        #mask_inv = cv2.bitwise_not(mask)
        kernel = np.ones((5, 5))
        mask_dil = cv2.dilate(mask, kernel, iterations=3)
        mask_dil_inv = cv2.bitwise_not(mask_dil)

        img_mask = cv2.bitwise_and(img, img, mask=mask_dil_inv)
        background_mask = cv2.bitwise_and(background, background, mask=mask_dil)
        img_final = cv2.add(img_mask,background_mask)

        cv2.imshow('img_final',img_final)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()