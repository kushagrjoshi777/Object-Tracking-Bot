# IP Address of the ESP32 for sending data
ESP32_IP = 'http://192.168.63.34'

import cv2 #Import the open cv library for image processing
import numpy as np #import the numpy library for array manipulation that is array of data for images
import math #import math library for mathematical calucalations
import requests #Import requests library to send HTTP get requests to ESP32

KNOWN_WIDTH = 15 #Known Width of the ball in cms
FOCAL_LENGTH = 3200 #Focal length of the camera with respect to 640x480 frame

def calculate_distance(focal_length, real_width, pixel_width):  #Define function to calculate distance of the object from the bot
    return round(((real_width * focal_length) / pixel_width)/5)*5 #Formula to calculate distance which is rounded off to the nearest 5

cap = cv2.VideoCapture(1) #Create the video capture object initialized with the index of the second camera connected that is 1

 
lower_bound = np.array([100, 150, 0]) #Define the lower bounds for the hsv values of blue color
upper_bound = np.array([140, 255, 255]) #Define the upper bounds for the hsv values of color blue

counter=0 #counter variable to keep in check to send only one http request when no object is detected
while True: #Create an infinte loop
    succ, frame = cap.read() #Capture one frame from the camera
    # frame=cv2.flip(frame,0)
    if not succ: #if frame capture failed:
        break #Break from this loop

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Use this function to convert the frame from the BGR 
    #color format to HSV format which is better for color detection

    mask = cv2.inRange(hsv, lower_bound, upper_bound) #Create a binary image mask that isolates the 
    #detected pixels(blue) as white color and represents the other pixels as black

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find the boundaries of all 
    #the detected white areas in the mask , the second arguements is so that no child contour is detected
    #The third arguement minimizes the points required to create that boundary 
    

    if contours: #check if the contours list is empty or not
        largest_contour = max(contours, key=cv2.contourArea) #Find the largest contour in the contours list, 
        #We use the key parameter to tell the max function to apply the conourArea function to each member of 
        #the contour list for comparison

        x, y, w, h = cv2.boundingRect(largest_contour) #Get the  x,y coordinates of the upper left corner of 
        #the smallest rectangle bounding the max contour as well as the width and height of the rectangle 

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #Draw the bounding rectangle on the frame we captured, 
        #Second arguement defines the upper left corner of the rectangle and the third arguement is for the bottom right corner,
        #fourth arguement is the rgb value for the rectangle it displays 
        #fifth Arguement is the thickness of the lines of the rectangle

        center_x = round((x + w / 2) / 10) * 10 #Get the x coordinate of the centre of the bounding rectangle rounded to nearest 10
        center_y = round((y + h / 2) / 10) * 10 #Get the x coordinate of the centre of the bounding rectangle rounded to nearest 10

 
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1) #Drawing a circle on the frame,
        #Second arguement is the coordinates of the circle to be drawn , Third arguement is the radius in pixels to be drawn
        #4th arguement is the rgb color of the circle
        #5th arguement specifies that the circle has to be drawn
        
        distance = calculate_distance(FOCAL_LENGTH, KNOWN_WIDTH, w) #Calculate the distance of the object
        x_offset=center_x

        url = f"{ESP32_IP}/offset?x_offset={x_offset}&distance={distance}" #Define the url with x_offset and distance as query paramteres to send to ESP32
        response=requests.get(url) #Send get requests to ESP32
 
        cv2.putText(frame, f"Center: ({center_x}, {center_y})", (x, y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) #Dsiplay the centre x & y coordinates on the frame 
                    #At coordinates (x,y-20) with the specified font and font scaling value (0.6) with RGB value for white 
                    #With the thickness of the text at 2 pixels
        cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) #Same format as above with distance displayed rounded off to 2 decimals
        #print("coordinates are: ", center_x, center_y)
        counter=0 #Set the counter to 0
    else: #If no contours detected
        if counter==0: #If counter is 0
            counter=counter+1 #Increase the counter value
            x_offset , distance = 0 , 0 #Set the x_offset and distance to 0
            url=f"{ESP32_IP}/offset?x_offset={x_offset}&distance={distance}" ##Define the url with x_offset and distance as query paramteres to send to ESP32
            response=requests.get(url) #Send get requests to the ESP32
            
    cv2.imshow("Color Tracking", frame) #Dsiplay the frame with the rectangle , circle , centre coordinates and distance displayed
    cv2.imshow("mask",mask) #display the mask to see which objects are detected
    
    if cv2.waitKey(1) == ord('q'): #Stops the program flow for one millisecond to check if q is presses
        break #breaks from the loop


cap.release() #release the video capture devices
cv2.destroyAllWindows() #close all the openCV windows