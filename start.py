import serial
import time
import ImageAnalysis

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

input_string = ser.readline().decode("utf-8").strip()
if input_string:
    print(input_string)
    
    
def send(message):
    ser.write((message+"\n").encode())
    input_string = ser.readline().decode("utf-8").strip()
    return input_string
    
    
#imageAnalysis = ImageAnalysis.ImageAnalysis()

while True:
    print(send("fwd"))
    
    time.sleep(1)
    
    print(send("rgt"))
    
    time.sleep(1)
    
    print(send("lft"))
    
    time.sleep(1)
    
