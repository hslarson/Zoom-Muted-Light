from PIL import ImageGrab
import pytesseract
import numpy as np
import cv2 as cv
import keyboard
import serial
import time
import json


#Load the Config File
try:
    with open("config.json") as file:
        config = json.load(file)
except:
    print("Error: config.json Not Found")
    exit()


#Global Constants
pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]
timeout = config["timeout_hours"]*3600
arduino_baud = 115200
text_min_width = 120
text_min_height = 18

#State Variables
last_state = True #Muted
found_size = False
last_time = time.monotonic()

running = True


#Sends a message to Arduino
def sendToArduino(msg):
    try:
        #Muted or not muted message
        if type(msg) == bool:
            if msg:
                arduino.write(str.encode('1'))
            else:
                arduino.write(str.encode('0'))
        
        #Tell the Arduino to turn off
        elif msg == 2:
            arduino.write(str.encode('2'))
    except:
        print("Error: Arduino Disconnected")

#Asks the User if They Want to End the Program
def endProgram(e):
    global running

    print("\nAre You Sure You Want To Exit?")
    print("(Press Enter to Exit. Press Any Other Key to Continue)")

    time.sleep(.25)
    if keyboard.read_hotkey() == 'enter':
        running = False
        print("Exiting...")
        return
    else:
        print("Continuing...")
        return

#Install Listener for ESC Key
keyboard.on_press_key('esc', endProgram)


#Find which port the arduino is on
for i in range(10):
    try:
        port = 'COM' + str(i)
        arduino = serial.Serial(port, arduino_baud, timeout=.1)
    except:
        pass
    else:
        print("\nFound an Arduino on " + port)
        break
else:
    print("Error: No Arduino Found")
    exit()


#Display initial banner
print("Starting Program\n")
while(running):
    #Take a screenshot
    src = np.asarray( ImageGrab.grab() )
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    src = cv.threshold(src, 220, 255, cv.THRESH_TOZERO)[1]

    #Search for rectangular formations in the thresholded image
    rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))
    dilation = cv.dilate(src, rect_kernel, iterations=1)

    #Search through the rectangles for the desired text
    contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        #Crop the text
        x,y,w,h = cv.boundingRect(cnt)
        if w < text_min_width or h < text_min_height:
            continue
        
        #Identify text
        crop = src[y:y+h, x:x+w]
        out = pytesseract.image_to_string(crop)

        #If you have the option to mute, it means you're unmuted
        if "Mute My Audio" in out:
            last_state = False
        elif "Unmute My Audio" in out:
            last_state = True
        else:
            continue

        last_time = time.monotonic()
        sendToArduino(last_state)

    #Check Timeout Clock
    if time.monotonic() > last_time + timeout:
        print("Timed Out")
        running = False

#Tell the arduino to turn off

sendToArduino(2)
arduino.close()
print("\nProgram Exited Successfully. Goodbye!\n\n")