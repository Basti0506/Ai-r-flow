# Ai(r)flow 🍃

## Overview ℹ️
This code is designed to perform real-time face detection using OpenCV on a connected camera feed. Additionally, it interfaces with a Raspberry Pi GPIO to control a fan based on the detected face's area.

## Requirements ➕
- Python 3
- OpenCV (`cv2`)
- tkinter
- Pillow (`PIL`)
- RPi.GPIO
- haarcascade_frontalface_default.xml (part of OpenCV)

## Usage ❓
- Ensure the Raspberry Pi GPIO setup is compatible and connected to a fan on PIN 8.
- Run the script in a Python environment.
- The GUI window will display the camera feed and detect faces in real-time.
- Detected faces will be outlined in a rectangle, and the fan speed will adjust based on face size.

### Buttons #️⃣
- **Start Camera:** Initiates the camera feed and face detection loop.
- **Toggle Mode:** Placeholder for potential future functionality.

### Menus 🗂️
- **Camera:** Allows switching between available cameras if multiple are connected.
- **Zoom:** Provides options for zooming in/out on the camera feed.

## Functionality ❗
- Upon starting the camera feed, the script continuously captures frames, detects faces using Haar cascades, and outlines them in the feed.
- The area of detected faces determines the fan's speed, with larger faces resulting in higher fan speeds.
- The GUI offers options to switch between cameras and zoom levels.
- Closing the GUI window will release the camera, stop the fan control, and clean up GPIO.

## Important Note 🛑
- Ensure proper GPIO connections and permissions before using the fan control functionality.

## Clean Up 🧹
- To stop the script, close the GUI window or terminate the Python process.
- Upon exiting, the script will release the camera, stop fan control, and clean up the GPIO pins.
