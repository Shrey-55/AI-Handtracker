import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
############################
wCam, hCam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
###############################

detector= htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        #print(totalFingers)

        cv2.putText(img,str(totalFingers),(10,70),0,3,(255,255,0),2)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 400), cv2.FONT_HERSHEY_PLAIN, 3,
              (255, 0, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break