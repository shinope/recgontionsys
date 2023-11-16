import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1ab24-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-1ab24.appspot.com"
})


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imgBackground = cv2.imread('Resources/background.png')


#importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

#print(len(imgModeList))

#load the encoding file

print('Loading encoding file')
file = open('encodeFile.p','rb')

encodeListKnownWithIds= pickle.load(file)
file.close()

encodeListKnown, staffIds= encodeListKnownWithIds
#print(staffIds)
print('encode file loaded')

modeType = 0
counter = 0
id = -1
imgStaff = []


while True:

    success, img = cap.read()

    imgS =cv2.resize(img, (0,0), None ,0.25, 0.25)
    imgS =cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]


    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        #print("Match Index", matchIndex)











        if matches[matchIndex]:
                # print("Known Face Detected")
                # print(staffIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id=staffIds[matchIndex]
            if counter == 0:
                counter=1

        if counter!=0:
            if counter==1:
                staffInfo = db.reference(f'staff/{id}').get
                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)


