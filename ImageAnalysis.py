import cv2
import numpy as np
import threading

class ImageAnalysis:
    
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def start(self):
        while True:
            ret, frame = self.camera.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            biggestFace = [0, (0,0), (0,0)]

            for (x, y, w, h) in faces:
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                if w*h > biggestFace[0]:
                    biggestFace[0] = w*h
                    biggestFace[1] = (x, y)
                    biggestFace[2] = (w, h)
            
            
            leftBound = int(frame.shape[1]/3)
            rightBound = int(frame.shape[1]*2/3)

            cv2.rectangle(frame, (leftBound, -10), (rightBound, int(frame.shape[0]+10)), (0, 0, 255), 2)

            if biggestFace[0] > 200:
                cv2.rectangle(frame, biggestFace[1], (biggestFace[1][0] + biggestFace[2][0], biggestFace[1][1] + biggestFace[2][1]), (0, 255, 0), 2)

                if leftBound > (biggestFace[1][0] + (biggestFace[2][0]/2)):
                    print("Left" + np.random.randint(0, 100).__str__())
                elif rightBound < (biggestFace[1][0] + (biggestFace[2][0]/2)):
                    print("Right" + np.random.randint(0, 100).__str__())


            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.camera.release()
        cv2.destroyAllWindows()
    


if __name__ == "__main__":
    imageAnalysis = ImageAnalysis()