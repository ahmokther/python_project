#install this pakages opencv python,numpy,pychaw

import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector(detectionCon=float(0.7))



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPar = 0









while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2


        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)
        # Hand Range 25 to 200
        #Volue Range -64 to 0
        vol = np.interp(length,[25,180],[minVol,maxVol])
        volBar = np.interp(length, [25, 180], [400, 150])
        volPar = np.interp(length, [25, 180], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)



        if length <30:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (200,0,0), cv2.FILLED)
        cv2.putText(img, f'{int(volPar)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 3)



    cTime = time.time()
    fps = 1 /(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS{int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(1,188,161),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)
