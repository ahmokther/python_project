import cv2
import time
import os
import HandTrackingModule as htm


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "hand"
mylist = os.listdir(folderPath)
#print(mylist)
overlaylist =[]
for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')
    overlaylist.append(image)
#print(len(overlaylist))

pTime = 0

detector = htm.handDetector(detectionCon=float(0.7))
tipsId = [4,8,12,16,20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    imlist = detector.findPosition(img,draw=False)
    #print(imlist)
    if len(imlist) != 0:
        finger = []
        #thum
        if imlist[tipsId[0]][1] > imlist[tipsId[0]-1][1]:   #imlist[tipsId[0]][1] < imlist[tipsId[0]-1][1] use for left thum
                                                            #imlist[tipsId[0]][1] > imlist[tipsId[0]-1][1] use for right thum
            finger.append(1)

        else:
            finger.append(0)





        #4 fingures
        for id in range(1,5):
            if imlist[tipsId[id]][2] < imlist[tipsId[id]-2][2]:
                finger.append(1)

            else:
                finger.append(0)

        #print(finger)
        TotalfingerCount = finger.count(1)
        print(TotalfingerCount)
        h, w, c = overlaylist[TotalfingerCount-1].shape
        img[0:h, 0:w] = overlaylist[TotalfingerCount-1]
        cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(TotalfingerCount),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),15)






    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
