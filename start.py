import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

input_string = ser.readline().decode("utf-8").strip()
if input_string:
    print(input_string)
    
    
def send(message):
    ser.write((message+"\n").encode())
    input_string = ser.readline().decode("utf-8").strip()
    print(input_string)
    
    
while True:
    print(send("fwd"))
    
    time.sleep(5)
    
