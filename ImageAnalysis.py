import cv2
import numpy as np
import threading
import os
import time
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import sys

class ImageAnalysis:
    
    def __init__(self):
        
        #os.system("libcamera-vid -t 1")
        #time.sleep(1)
        
        self.position = "none"
        self.mid_x = 0
        self.faceSize = 1000000000

        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        options = ObjectDetectorOptions(
          num_threads=2,
          score_threshold=0.3,
          max_results=3,
          enable_edgetpu=False)
        self.detector = ObjectDetector(model_path="efficientdet_lite0.tflite", options=options)

        # self.thread = threading.Thread(target=self.start)
        # self.thread.start()
        self.start()

    # Crop the image on all sides by a given amount
    def crop(self, image, amount):
        return image[:, amount:-amount]

    def getPosition(self):
        pos = self.position
        self.position = "none"
        return pos
    
    def getFaceSize(self):
        return self.faceSize

    def change_brightness(self, img, value=50):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v,value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img


    def detectFaces(self, frame, leftBound, rightBound):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        #faces = self.detector.detect_faces(frame)

        #faces = [el['box'] for el in faces]


        biggestFace = [0, (0,0), (0,0)]

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if w*h > biggestFace[0]:
                biggestFace[0] = w*h
                biggestFace[1] = (x, y)
                biggestFace[2] = (w, h)
        
        if biggestFace[0] > 1000:
                
            self.faceSize = biggestFace[0]
            
            cv2.rectangle(frame, biggestFace[1], (biggestFace[1][0] + biggestFace[2][0], biggestFace[1][1] + biggestFace[2][1]), (0, 255, 0), 2)

            if leftBound > (biggestFace[1][0] + (biggestFace[2][0]/2)):
                #print("Left" + np.random.randint(0, 100).__str__())
                self.position = "left"
            elif rightBound < (biggestFace[1][0] + (biggestFace[2][0]/2)):
                #print("Right" + np.random.randint(0, 100).__str__())
                self.position = "right"
            else:
                self.position = "center"
        else:
            self.postion = "none"
        
        

    def findArea(self, bounding_box):
        return (bounding_box[2] - bounding_box[0]) * (bounding_box[3] - bounding_box[1])


    def detectPeople(self, frame, leftBound, rightBound):
        detections = self.detector.detect(frame)
            
        frame = utils.visualize(frame, detections)
        
        #print(detections)
        
        self.maxPerson = None
        
        for detection in detections:
            if detection.categories[0].label == "person":
                #print("Found person")
                #print(detection.bounding_box)
                bounding_box = list(detection.bounding_box)
                #print(bounding_box)
                        
                confidence = detection.categories[0].score
                
                if (not self.maxPerson) or (confidence > self.maxPerson[1]):
                    self.maxPerson = [bounding_box, confidence]
                    cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (0,255,0))
        
        
        if self.maxPerson is None:
            self.postion = "none"
            return
        
        
        bounding_box = self.maxPerson[0]
        
        self.mid_x = bounding_box[0] + ((bounding_box[2] - bounding_box[0])/2)
        
        
        if leftBound > (self.mid_x):
            #print("Left" + np.random.randint(0, 100).__str__())
            self.position = "left"
        elif rightBound < (self.mid_x):
            #print("Right" + np.random.randint(0, 100).__str__())
            self.position = "right"
        else:
            self.position = "center"
                
        
            

    def start(self):
        
        while True:
            ret, frame = self.camera.read()

            #frame = self.crop(frame, 150)

            # frame = self.change_brightness(frame, value=100)

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #frame = cv2.resize(frame, (640,480))
            
            
            self.leftBound = int(((frame.shape[1]/2) - frame.shape[1]/12.5))
            self.rightBound = int(((frame.shape[1]/2) + frame.shape[1]/12.5))

            cv2.rectangle(frame, (self.leftBound, -10), (self.rightBound, int(frame.shape[0]+10)), (0, 0, 255), 2)

            
            #self.detectFaces(frame, leftBound, rightBound)
            
            self.detectPeople(frame, self.leftBound, self.rightBound)
            

            cv2.putText(frame, self.position, (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            outputFrame = cv2.resize(frame, (1440,1080))
            
            cv2.imshow('frame', outputFrame)
            
            # time.sleep(0.1)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.camera.release()
        cv2.destroyAllWindows()
        sys.exit()
    


if __name__ == "__main__":
    imageAnalysis = ImageAnalysis()