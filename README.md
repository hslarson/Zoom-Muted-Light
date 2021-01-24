# Physical "Muted" Light for Zoom

#### How It Works:
- Takes frequent screenshots
- Measures the scale of the Zoom icons
- Scans for the Zoom "Muted/Unmuted" images in each screenshot using OpenCV
- Sends the data to the Ardino if an icon is found
- Ardino displays lights according to the data it receives
- Arduino stores the last value of the mute button


#### Current Limitations
- Icon must be mostly visible to resister
- Not very efficient
- Lots on dependencies
