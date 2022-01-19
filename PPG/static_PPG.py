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

dataLen = 120
camTimes = [0]*dataLen
intensities = []
x = list(range(len(intensities)))


def getHR():
    fs = 1 / (sum(camTimes) / dataLen)
    tmpIntens = sig.detrend(applyFF(intensities, fs))
    freqs, pows = signal.welch(tmpIntens, fs=fs, nperseg=256)
    bpm = round(freqs[np.argmax(pows)] * 60, 2)
    if(bpm > 50 and bpm < 150 or bpm == 0):
        print("output BPM: ", bpm, fs)
    return bpm

cap = cv2.VideoCapture(0)

def readIntensity(intensities, curFrame, cropBoxBounds):
    now = 0

    fixedX1 = 115
    fixedY1 = 80
    fixedX2 = 155
    fixedY2 = 100
    while True:

        ret, frame = cap.read()

        scaleFactor = 0.4
        frame = cv2.resize(frame,(-1,-1), fx=scaleFactor, fy=scaleFactor)

        ROI = frame[fixedY1:fixedY2, fixedX1:fixedX2, 1]
        intensity = ROI.mean()
        # intensity = np.median(ROI) # works, but quite chunky.

        intensities.append(intensity)

        # Draw the forehead box:
        # curFrame[0] = cv2.rectangle(frame, (eyeleft, headTop),
        #                             (eyeright, eyeTop), (0, 255, 0), 1)
        cropBoxBounds[0] = [fixedY1 + 2, fixedY2 - 2, fixedX1 + 2, fixedX2 - 2]


        curFrame[0] = cv2.rectangle(frame, ( fixedX1 , fixedY1), ( fixedX2 , fixedY2) , (0,0,255), 1)

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