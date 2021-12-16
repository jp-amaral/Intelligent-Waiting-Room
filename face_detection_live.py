import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open camera")

while True:
    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.35,6)
    print(len(faces))

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
    
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows