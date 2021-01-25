# Physical "Muted" Light for Zoom

#### How It Works:
- Searches ports for Arduino
- Takes periodic screenshots
- Thresholds the image and finds rectangular shapes
- Uses Tesseract to search for the Zoom "Muted/Unmuted" text
- Sends the data to the Arduino if text is found
- Arduino displays lights according to the data it receives
- Arduino stores the last value of the mute button


#### Current Limitations
- Not very efficient
- Only works in primary monitor
- Mac and Windows only
- The Event Listener for ESC Key is Global


#### Software You'll Need
- Python 3
- Tesseract (Make sure you add file path to config.json)
- Arduino IDE


#### Pip Packages You'll Need
- numpy
- matplotlib
- opencv-python
- pyserial
- Pillow
- keyboard
- pytesseract
