from PIL import ImageGrab
import numpy as np
import cv2 as cv
import time
import serial
import keyboard


#Global Constants
match_thresh = 0.9
timeout = 1*60*60 #1 Hour
arduino_baud = 115200
muted_name = "muted.png"
talking_name = "talking.png"

#State Variables
last_state = True #Muted
found_size = False
last_time = time.monotonic()

running = True


#Slides a template over an image and returns a value from 0 to 1 indcating the quality of the best match
def applyTemplate(src, template):
    result = cv.matchTemplate(src, template, cv.TM_CCORR_NORMED)

    #Apply threshold
    best_find = np.unravel_index(np.argmax(result), result.shape)
    return result[best_find]


#Sends a message to Arduino
def sendToArduino(msg):
    #Muted or not muted message
    if type(msg) == bool:
        if msg:
            arduino.write(str.encode('1'))
        else:
            arduino.write(str.encode('0'))
    
    #Tell the Arduino to turn off
    elif msg == 2:
        arduino.write(str.encode('2'))


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


#Load the templates
muted_template   = cv.imread(muted_name, cv.IMREAD_GRAYSCALE)
talking_template = cv.imread(talking_name, cv.IMREAD_GRAYSCALE)

if type(muted_template) != np.ndarray or type(talking_template) != np.ndarray:
    print("Error: Failed to Load Templates")
    exit()


#Find which port the arduino is on
for i in range(10):
    try:
        port = 'COM' + str(i)
        arduino = serial.Serial(port, arduino_baud, timeout=.1)
    except:
        pass
    else:
        if arduino.is_open:
            print("\nFound an Arduino on " + port)
        else:
            print("Error: Failed to Connect to Arduino")
            exit()
        break
else:
    print("Error: No Arduino Found")
    exit()


#Display initial banner
print("\n==Starting Program. Press ESC to Quit==")
print("Testing Icon Sizes. You Can Help by Making Sure the Mute Button is Visible")

while(running):
    #Take a screenshot
    src = np.asarray( ImageGrab.grab() )
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    #Search the image for both templates
    muted = True
    for template in (muted_template, talking_template):
        
        #If the symbol size hasn't been established yet, try a bunch of scaled-down templates to see if anything matches
        if not found_size:
            first_match = 0
            match_strengths = []

            for i in range(20,60):
                temp_template = cv.resize(template, (0,0), fx=i/50, fy=i/50)

                #If we find a range of good scale values, save them
                strength = applyTemplate(src, temp_template)
                if strength > match_thresh:
                    match_strengths.append(strength)
                    
                    if not found_size:
                        first_match = i
                        found_size = True

                #Once we exit the good range, find the best in the range and set that as the scale
                elif found_size:
                    best_i = first_match + np.argmax(match_strengths)
                    print("Scale Set: ", best_i/50)

                    muted_template = cv.resize(muted_template, (0,0), fx=best_i/50, fy=best_i/50)
                    talking_template = cv.resize(talking_template, (0,0), fx=best_i/50, fy=best_i/50)

                    sendToArduino(muted)
                    last_time = time.monotonic()
                    break

        #Otherwise, search with the scaled template
        elif applyTemplate(src, template) > match_thresh:
            sendToArduino(muted)
            last_time = time.monotonic()
            break
        
        muted = False #Change flag to indicate talking

    #Check Timeout Clock
    if time.monotonic() > last_time + timeout:
        print("Timed Out")
        running = False
    else:
        time.sleep(.25)

#Tell the arduino to turn off
sendToArduino(2)
arduino.close()
print("\nProgram Exited Successfully. Goodbye!\n\n")
