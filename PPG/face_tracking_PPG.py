# Must be run in console to work properly

from locale import currency
import numpy as np
import cv2
import time
from scipy import signal
import threading

from scipy.fft import fft, fftfreq

import scipy.signal as sig

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


def applyFF(data, sampleFreq):
    if sampleFreq > 3:
        sos = sig.iirdesign(.66, .5, 1.0, 40.0, fs=sampleFreq, output='sos')
        return sig.sosfiltfilt(sos, data)
    else:
        return data

def getFaceXYHWAndEyeXYHW(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Only take one face, the first
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) < 1:
        return None
    (x, y, w, h) = faces[0]

    # Crop out faces and detect eyes in that window.
    roi_gray = gray[y:y + h, x:x + w]
    eyes, numDetects = eye_cascade.detectMultiScale2(roi_gray, minNeighbors=10)
    if len(numDetects) < 2:
        return None

    # Change eye coords to be in image coordinates instead of face coordinates
    eyes[0][0] += x
    eyes[1][0] += x
    eyes[0][1] += y
    eyes[1][1] += y

    return [faces[0], eyes[0], eyes[1]]

def getFace(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Only take one face, the first
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) < 1:
        return None

    return faces[0]


dataLen = 120
camTimes = [0]*dataLen
intensities = []
x = list(range(len(intensities)))


def getHR():
    fs = 1 / (sum(camTimes) / dataLen)
    tmpIntens = sig.detrend(applyFF(intensities, fs))
    freqs, pows = signal.welch(tmpIntens, fs=fs, nperseg=256)
    bpm = round(freqs[np.argmax(pows)] * 60, 2)
    if(bpm > 50 and bpm < 150):
        print("output BPM: ", bpm, fs)
    return bpm

def getHeadboxFromHead(face):
    return face[0] + face[2] // 4, face[1] + face[3] // 2, face[0] + 3 * face[2] // 4, face[1] + face[3] // 2 + 50

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

def readIntensity(intensities, curFrame, cropBoxBounds):
    now = 0

    eyeleft = 0
    headTop = 0
    eyeright = 0
    eyeTop = 0
    while True:

        ret, frame = cap.read()

        scaleFactor = 0.4
        frame = cv2.resize(frame,(-1,-1), fx=scaleFactor, fy=scaleFactor)

        # tmp = getFaceXYHWAndEyeXYHW(frame) # Haar outputs [x, y, w, h] format
        face = getFace(frame)
        if face is not None:
        # if tmp != None:
            # face, eye1, eye2 = tmp
            # eyeleft, headTop, eyeright, eyeTop\
            # tmpHeadbox = getHeadbox(face, eye1, eye2)
            tmpHeadbox = getHeadboxFromHead(face)
            
            a = .4
            eyeleft = int(tmpHeadbox[0]*a + (1-a)*eyeleft)
            headTop = int(tmpHeadbox[1]*a + (1-a)*headTop)
            eyeright = int(tmpHeadbox[2]*a + (1-a)*eyeright)
            eyeTop = int(tmpHeadbox[3]*a + (1-a)*eyeTop)

            offsetY = (tmpHeadbox[2]-tmpHeadbox[0])
            x1=tmpHeadbox[0]+5
            x2=tmpHeadbox[2]-5
            y1=tmpHeadbox[1]-offsetY
            y2=tmpHeadbox[3]-offsetY-30
            
            #headTOP = y1, eyeTop = y2, eyeLeft = x1, eyeright =x2


            #ROI = frame[headTop:eyeTop, eyeleft:eyeright, 1]
            ROI = frame[y1:y2, x1:x2, 1]
            intensity = ROI.mean()
            # intensity = np.median(ROI) # works, but quite chunky.

            intensities.append(intensity)

            # Draw the forehead box:
            # curFrame[0] = cv2.rectangle(frame, (eyeleft, headTop),
            #                             (eyeright, eyeTop), (0, 255, 0), 1)
            cropBoxBounds[0] = [y1 + 2, y2 - 2, x1 + 2, x2 - 2]


            curFrame[0] = cv2.rectangle(frame, ( x1 , y1), ( x2 , y2) , (0,0,255), 1)

            if (len(intensities) > dataLen):
                intensities.pop(0)

            camTimes.append(time.time() - now)
            now = time.time()
            camTimes.pop(0)

cropBoxBounds = [0]
curFrame = [0]
t1 = threading.Thread(target = readIntensity, daemon=True, args=(intensities, curFrame, cropBoxBounds))
t1.start()

time.sleep(1)
while True:
    frame = curFrame[0]
    bb = cropBoxBounds[0]
    ROI = frame[bb[0]:bb[1], bb[2]:bb[3], 1]
    getHR()
    cv2.imshow("yea", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break