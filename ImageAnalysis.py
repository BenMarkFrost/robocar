import cv2

class ImageAnalysis:
    
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def start(self):
        while True:
            ret, frame = self.camera.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            leftBound = int(frame.shape[1]/3)
            rightBound = int(frame.shape[1]*2/3)

            cv2.rectangle(frame, (leftBound, -10), (rightBound, int(frame.shape[0]+10)), (0, 0, 255), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.camera.release()
        cv2.destroyAllWindows()
    


if __name__ == "__main__":
    imageAnalysis = ImageAnalysis()
    imageAnalysis.start()