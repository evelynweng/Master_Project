# import packages

import numpy as np
import argparse
import cv2
import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model


def detect_mask(image_in):
    # load openCV's pretrained face detector model

    # print("loading face detector")
    configPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
    faceModelPath = os.path.sep.join(["face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
    faceDetector = cv2.dnn.readNet(configPath, faceModelPath)
    
    # load trained mask detector model

    # print("loading mask detector")
    maskDetector = load_model('mask_detector/mask_detector.model')

    # load input image
    image = cv2.imread(image_in)
    # get the image height and width
    (h, w) = image.shape[:2]

    # create a 3x3 blob and preprocess using RGB mean subtraction
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # run the preprocessed blob through the face detector network
    # print("performing face detection")
    faceDetector.setInput(blob)
    detections = faceDetector.forward()

    # loop through all detections
    for i in range(0, detections.shape[2]):
        # get the confidence of face presence
        confidence = detections[0, 0, i, 2]

        # ensure face confidence is above 0.95 threshold
        if confidence > 0.95:
            # compute bounding box of the face and its coordinates
            boundingBox = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = boundingBox.astype("int")

            # make sure bounding box does not lie outside frame, set to 0 and +/- 1 if necessary
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract face ROI, convert from BGR to RGB channel order, resize and preprocess
            face = image[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            face = np.expand_dims(face, axis=0)

            # pass preprocessed face through mask detection model
            (mask, noMask) = maskDetector.predict(face)[0]

            # return result
            maskDetected = True if mask > noMask else False
            # probability = max(mask, noMask) * 100
            
            return maskDetected
        
#result = detect_mask('images/example_01.jpg')
#print(result)