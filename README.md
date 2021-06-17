# invisiblity_cloak
Created a simple Invisibility cloak code (like that used by Harry Potter) using opencv-python. This uses primary webcam to capture live video.

1. You can choose to calibrate the HSV value of the color of the cloak. This is done in calibrate_hsv() function. By sliding the TrackBars in the 'Calibrate' window you can adjust them such that the cloak region appears white in the 'mask' window whereas everything appears black. By default the TrackBars are adjust to detect maroon color.

2. Then you need to capture a background image which will be visible through the region covered by the cloak making the foreground invisible.

3. Finally the live webcam image is masked with the background image creating a illusion that anything behind the cloak becomes invisible. Masking is done in findMask(img) function.

#------------------------------------------------------------------------------------------------------

Dependencies:-

*import cv2
*import numpy as np
*import time
