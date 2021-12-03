import serial
import time
import ImageAnalysis

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
tempMove = ""
counter = 5

input_string = ser.readline().decode("utf-8").strip()
if input_string:
    print(input_string)
    
    
def send(message, moveTime):
    formattedMessage = (f"%s %s" % (message, moveTime))
    ser.write((formattedMessage+"\n").encode())
    input_string = ser.readline().decode("utf-8").strip()
    #print(input_string)
    return input_string
    
    
imageAnalysis = ImageAnalysis.ImageAnalysis()

def move(direction, moveTime):
    
    if direction == "right":
        send("rgt", moveTime)
    elif direction == "left":
        send("lft", moveTime)
    
    time.sleep((moveTime)/1000)
    

while True:

    result = imageAnalysis.getPosition()
    faceSize = imageAnalysis.getFaceSize()
    #print(result)
    moveTime = 10
    
    mid_x = imageAnalysis.mid_x
    #print(mid_x)
    
    
        
    if (result == "none") & (counter > 0):
            
        if (tempMove == "right" or tempMove == "left"):
            
            print("should keep moving", tempMove, counter)
            
            move(tempMove, moveTime)
                
            counter -= 1
    
        continue
    
    distance = 0
    if result == "right":
        distance = mid_x - imageAnalysis.rightBound
    elif result == "left":
        distance = imageAnalysis.leftBound - mid_x
    
    
    moveTime = int((moveTime * distance/30))
    print(moveTime)
    

    move(result, moveTime)
    tempMove = result
    counter = 2
        
    #if faceSize < 60000:
        #send("fwd",40)
    
    
    # print(send("fwd"))
    
    # time.sleep(1)
    
    # print(send("rgt"))
    
    # time.sleep(1)
    
    # print(send("lft"))
    
    # time.sleep(1)
    
