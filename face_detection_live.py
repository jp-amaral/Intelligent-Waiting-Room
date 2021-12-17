import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

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
    
    img = cv2.resize(img, (960,740))

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF

    out.write(img)

    if k == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows