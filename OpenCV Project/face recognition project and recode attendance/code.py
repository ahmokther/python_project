import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


path = 'class people'
images =[]
classNames = []
myList = os.listdir(path)
#print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

def MarkAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDateList = f.readline()
        nameList = []

        for line in myDateList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtstrg = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstrg}')






encodeListKnown = findEncodings(images)
print('Encoding Complete')
cap = cv2.VideoCapture(0)



while True:
    success,img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurrentFrame = face_recognition.face_locations(imgS)
    encodesCurrentFrame = face_recognition.face_encodings(imgS,facesCurrentFrame)
    for encodeFace,faceloc in zip(encodesCurrentFrame,facesCurrentFrame):
        matces = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDistance)
        matceIndex = np.argmin(faceDistance)

        if matces[matceIndex]:
            name = classNames[matceIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            y1, x2, y2, x1 = y1*4 ,x2*4 ,y2*4 ,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            MarkAttendance(name)

    cv2.imshow('WebCam',img)
    cv2.waitKey(1)
