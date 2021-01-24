# Physical "Muted" Light for Zoom

#### How It Works:
- Searches ports for Arduino
- Takes periodic screenshots
- Measures the scale of the Zoom icons
- Scans for the Zoom "Muted/Unmuted" icons in each screenshot using OpenCV
- Sends the data to the Arduino if an icon is found
- Arduino displays lights according to the data it receives
- Arduino stores the last value of the mute button


#### Current Limitations
- Icon must be mostly visible to register
- Not very efficient
- Lots of dependencies
