# Object Tracking Robot
Object tracking robot repository

# Description
An automonomous bot that tracks a blue ball and follows behind it

The basic workflow of the bot is that a mobile phone is mounted on the bot itself and a local hotspot network is started on the phone. A laptop is connected to the network which gets the live feed from the bot and uses the OPENCV library to detect the biggest blue object found in the screen and sends the x-coordinate and distance to the ESP32-CAM integrated in the bot's circuit connected to the same network . Then the ESP32-CAM forwards those values to the arduino NANO (mounted on the bot as well) using UART connections . Then according to the x_offset from a strip of the screen that is predefined , signals are sent to the motor drivers to drive the motors accordingly.

# Softwares Used
1. VS Code (Laptop)
2. Arduino IDE (ESP32-CAM & Arduino NANO)

# Languages Used
1. Python (Object detection)
2. Embedded C (ESP32-CAM & Arduino NANO)

# Libraries Used
---------------------
PYTHON(VS CODE)
1. OpenCV
2. Numpy
3. Requests
---------------------
EMBEDDED C (ESP32-CAM)
1. WiFi
2. WebServer
---------------------


# Drive-Config
Two Wheel differential Drive

# Compnents used:
1. ESP32-CAM
2. Arduino NANO
3. LIPO Battery (12V)
4. 2x Buck Converters
   :12V - 5V
   :12V - 3.3V
5. Logic Level Converters (5V - 3.3V)
6. Cytron MDD20A
7. PMDC Offset motor (300RPM)
8. 2x Traction Wheels and 1x Castor wheel
9. 4x Aluminium channels with reinforced wood
10. 8x L bents/mounts
11. 2x Motor mounts
12. Wood Base
13. Phone stand
