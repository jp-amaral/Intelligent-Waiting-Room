from multiprocessing.sharedctypes import Value
import numpy as np
import cv2
import time
import sys
import socket
import json
import paho.mqtt.client as mqtt

# --------------------------------------------------------- CONFIG
broker_address = "192.168.160.19"
#Client instance
client = mqtt.Client("ppg-client-pub")

client.connect(broker_address, port=1883, keepalive=60)
# ---------------------------------------------------------
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
message = {'value': 0}

# Helper Methods
def buildGauss(frame, levels):
    pyramid = [frame]
    for level in range(levels):
        frame = cv2.pyrDown(frame)
        pyramid.append(frame)
    return pyramid
def reconstructFrame(pyramid, index, levels):
    filteredFrame = pyramid[index]
    for level in range(levels):
        filteredFrame = cv2.pyrUp(filteredFrame)
    filteredFrame = filteredFrame[:videoHeight, :videoWidth]
    return filteredFrame
def main():
    global value
    face = True
    # Webcam Parameters
    webcam = cv2.VideoCapture(0)
    realWidth = 640
    realHeight = 480
    videoWidth = int(realWidth/2)
    videoHeight = int(realHeight/2)
    videoChannels = 3
    videoFrameRate = 15
    webcam.set(3, realWidth)
    webcam.set(4, realHeight)

    # Output Videos
    # if len(sys.argv) != 2:
    #     originalVideoFilename = "original.mov"
    #     originalVideoWriter = cv2.VideoWriter()
    #     originalVideoWriter.open(originalVideoFilename, cv2.cv.CV_FOURCC('j', 'p', 'e', 'g'), videoFrameRate, (realWidth, realHeight), True)

    # outputVideoFilename = "output.mov"
    # outputVideoWriter = cv2.VideoWriter()
    # outputVideoWriter.open(outputVideoFilename, cv2.cv.CV_FOURCC('j', 'p', 'e', 'g'), videoFrameRate, (realWidth, realHeight), True)

    # Color Magnification Parameters
    levels = 3
    alpha = 150
    bpmfq = 15
    minFrequency = 1.0
    maxFrequency = 2.0
    bufferSize = 150
    bufferIndex = 0

    # Output Display Parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    loadingTextLocation = (20, 30)
    bpmTextLocation = (videoWidth//2 + 5, 30)
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2
    boxColor = (0, 255, 0)
    boxWeight = 3

    # Initialize Gaussian Pyramid
    firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
    firstGauss = buildGauss(firstFrame, levels+1)[levels]
    videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
    fourierTransformAvg = np.zeros((bufferSize))

    # Bandpass Filter for Specified Frequencies
    frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
    mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)

    # Heart Rate Calculation Variables
    bpmCalculationFrequency = bpmfq
    bpmBufferIndex = 0
    bpmBufferSize = 10
    bpmBuffer = np.zeros((bpmBufferSize))
    prevTime = 0
    i = 0
    count = 0
    calculated = 0
    while (True):
        ret, frame = webcam.read()
        count +=1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.15,6)
        if len(faces) == 0:
            face = False
        else:
            faceCount = 0
        if ret == False:
            break

        # if len(sys.argv) != 2:
        #     originalFrame = frame.copy()
            #originalVideoWriter.write(originalFrame)
            
        detectionFrame = frame[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):int(realWidth-videoWidth/2), :]

        # Construct Gaussian Pyramid
        videoGauss[bufferIndex] = buildGauss(detectionFrame, levels+1)[levels]
        fourierTransform = np.fft.fft(videoGauss, axis=0)

        # Bandpass Filter
        fourierTransform[mask == False] = 0

        # Grab a Pulse
        if bufferIndex % bpmCalculationFrequency == 0:
            i = i + 1
            for buf in range(bufferSize):
                fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
            hz = frequencies[np.argmax(fourierTransformAvg)]
            bpm = 60.0 * hz
            bpmBuffer[bpmBufferIndex] = bpm
            bpmBufferIndex = (bpmBufferIndex + 1) % bpmBufferSize

        # Amplify
        filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
        filtered = filtered * alpha

        # Reconstruct Resulting Frame
        #filteredFrame = reconstructFrame(filtered, bufferIndex, levels)
        outputFrame = detectionFrame #+ filteredFrame
        outputFrame = cv2.convertScaleAbs(outputFrame)

        bufferIndex = (bufferIndex + 1) % bufferSize

        frame[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):int(realWidth-videoWidth/2), :] = outputFrame

        if(count%20==0):
            value = int(calculated/20)
            #if value < 63: value = 65
            #print("-----refreshing-----")
            try:
                message['value'] = str(value)
                pickled_message = json.dumps(message)
                client.publish("ppg", pickled_message)
                print(json.loads(pickled_message))
                #print pickled_message decode
                # response = sock.recv(4096).decode()
                # print('Server response: {}'.format(response))
            except (socket.timeout, socket.error):
                print('Server error. Done!')
                sys.exit(0)
            calculated = 0
            #print(value)
        else:
            if bpmBuffer.mean() < 61:
                newValue = 61
            else:
                newValue = bpmBuffer.mean()
            calculated += newValue

        #Green rectangle in the middle of the frame (maybe changing this to follow the face?)
        #cv2.rectangle(frame, bpmTextLocation, (100,20), (0,0,0), -1)
        if not face:
            value = 0
            face = True
        if i > bpmBufferSize:
            cv2.putText(frame, "BPM: %d" % value, bpmTextLocation, font, fontScale, fontColor, lineType)
        else:
            pass
            #cv2.putText(frame, "Calculating BPM...", loadingTextLocation, font, fontScale, fontColor, lineType)

        #outputVideoWriter.write(frame)
        
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime
        #print(fps)

        if len(sys.argv) != 2:
            cv2.imshow("Webcam Heart Rate Monitor", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    webcam.release()
    cv2.destroyAllWindows()


main()
