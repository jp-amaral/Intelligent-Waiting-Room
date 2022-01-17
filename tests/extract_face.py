from imutils import paths
import face_recognition
import pickle
import os
import cv2

imagePath = list(paths.list_images('Images'))

kEncodings = []
kNames = []

for (i, ip) in enumerate(imagePath):
    name = ip.split(os.path.sep)[-2]
    image = cv2.imread(ip)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    for encoding in encodings:
        kEncodings.append(encoding)
        kNames.append(name)
    
data = {"encodings":kEncodings, "names":kNames}
f = open("face_enc","wb")
f.write(pickle.dumps(data))
f.close()