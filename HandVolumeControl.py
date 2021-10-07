import cv2
import mediapipe as mp
import time

import numpy as np

import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################
wCam, hCam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
###############################33

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volume.SetMasterVolumeLevel(0.0, None)

###################################################

detector = htm.handDetector(maxHands=1, detectionCon=0.7)
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList,_ = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cv2.circle(img, (x1, y1), 5, (255, 0, 0), -1)
        cv2.circle(img, (x2, y2), 5, (255, 255, 0), -1)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        vol = np.interp(length, [30, 300], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        # print(vol)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
    #           (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
