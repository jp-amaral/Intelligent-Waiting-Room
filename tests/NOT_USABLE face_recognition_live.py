import cv2
import face_recognition
import pickle
import os
import face_recognition_models
import imutils

#NOT TO USE, TOO SLOW

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
data = pickle.loads(open('face_enc', "rb").read())

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open camera")

while True:
    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray,1.35,6)
    encodings = face_recognition.face_encodings(rgb)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name = "unknown"

        if True in matches:
            matchedIds = [i for (i,b) in enumerate(matches) if b]
            count = {}

            for i in matchedIds:
                name = data["names"][i]
                count[name] = count.get(name,0) + 1
            
            name = max(count, key=count.get)
            names.append(name)

    for ((x,y,w,h),name) in zip(faces, names):
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
        cv2.putText(img, name, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
    
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows