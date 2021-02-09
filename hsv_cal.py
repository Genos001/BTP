#finding hsv range of target object(pen)
import cv2
import numpy as np
import time
# A required callback method that goes into the trackbar function.
def nothing(x):
    pass

# Initializing the webcam feed.
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,400)

# Create a window named trackbars.
cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of 
# H,S and V channels. The Arguments are like this: Name of trackbar, 
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
 
while True:
    
    # Start reading the webcam feed frame by frame.
    ret, frame = cap.read()
    if not ret:
        break
    # Flip the frame horizontally (Not required)
    frame = cv2.flip( frame, 1 ) 
    
    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get the new values of the trackbar in real time as the user changes 
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    
    # Filter the image and get the binary mask, where white represents 
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)
 
    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)#dtfyguhijokl;kjhgfgdxfcgvbjnkml,lmknjbvcvxcbbvnm,.,mbvnm,./////////////////////
    
    # Converting the binary mask to 3 channel image, this is just so 
    # we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # stack the mask, orginal frame and the filtered result
    stacked = np.hstack((mask_3,frame,res))
    
    # Show this stacked frame at 40% of the size.
    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
    
    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    # If the user presses `s` then print this array.
    if key == ord('s'):
        
        thearray = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
        print(thearray)
        
        # Also save this array as penval.npy
        np.save('hsv_value',thearray)
        break
    
# Release the camera & destroy the windows.    
cap.release()
cv2.destroyAllWindows()




"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

     # Red color
    low_red = np.array([0, 50, 100])
    high_red = np.array([43, 255, 225])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Blue color
    low_blue = np.array([86, 36, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Green color
    low_green = np.array([16, 40, 86])
    high_green = np.array([35, 180, 205])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)


    cv2.imshow("Frame", frame)
    cv2.imshow("Red", red)
    cv2.imshow("Blue", blue)
    cv2.imshow("Green", green)
    #.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break

"""
"""import cv2
import numpy as np
import pandas as pd
import RPi.GPIO as GPIO
import time
from pygame import mixer

btn_pin = 15
mode = True # 1 for color and 2 for ph
st_time = -1
index=["color_name","R","G","B"]
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
prev_result_mode2 = "nill"


GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
mixer.init()

def getColorName(R,G,B):
	if(mode):
		csv = pd.read_csv('colorsT10.csv', names=index, header=None,encoding='latin-1')
    else:
    	csv = pd.read_csv('colorsV3.csv', names=index, header=None,encoding='latin-1')
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname


def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    red_count=0 , blue_count=0 ,other=0 , prev_count=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = 2000
        areaMax = 15000
        if (area > areaMin and area < areMax and area > prev_area):
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #time.sleep(0.1)
            if len(approx)<4 or len(approx)>5:
                break

            print(len(approx))
			for i in range 9:
		        x , y , w, h = cv2.boundingRect(approx)
		        result = detect_color(x+10,y+10,x+w-20,y+h-20)
		        if(result == 0):
		        	red_count +=1
		        elif(result == 1):
		        	blue_count +=1
		        else:
		        	other +=1

		prev_area = cv2.contourArea(cnt)
		if(red_count > 3):
			if(prev_result_mode2 == "red"):
				#speak red again
			else:
				if(prev_result_mode2 != "nill"):
					#speak red
				else:
					#speak its red now
			prev_result_mode2 = "red"
		if(blue_count > 3):
			if(prev_result_mode2 == "blue"):
				#speak blue again
			else:
				if(prev_result_mode2 != "nill"):
					#speak blue
				else:
					#speak its blue now
			prev_result_mode2 = "blue"
		else:
			#speak no change
			prev_result_mode2 = "nill"





def detect_color(s1,s2,e1,e2):

    red = 0
    blue = 0
    white = 0
    ph = 0
    count = 0
    for x in range( s1, e1-1,10) :
        for y in range( s2 , e2-1,10) :
            count+=1
            if frameHeight <= x+10 or frameWidth <= y+10:
                break 
            roi = img[x:x+10, y:y+10]

            avg1 = np.average(roi, axis=0)
            avg2 = np.average(avg1, axis=0)
            avg2_int = avg2.astype(int)
            avg2_int = avg2_int[::-1]           #reversed for rgb 
           # avg2_int_tup = tuple(avg2_int)
            r = avg2_int[0]
            g = avg2_int[1]
            b = avg2_int[2]
           
            new = getColorName(r,g,b)
            if(new =='Red'): 
                red +=1
            elif(new== 'Blue'):
                blue +=1
            elif(new == 'Ph'):
                ph +=1
            else:
                white +=1

    print(red,"   ",blue,"    ",white,"     ",ph,"    ",count)


    if(red > blue and red > 10):
        print("Red detected")
        return 0
    elif(blue > red and blue> 10 ):
        print("Blue detected")
        return 1
    else:   
        print("..*******************....")
        return 2




def func_mode2():
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = 40
    threshold2 = 10
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil,imgContour)

def func_mode1():

    cv2.rectangle(img, (309,229), (329,249), (0,255,0), 1)       #pixel range = x ==> 0-639 and y == 0 - 479
    roi = img[230:249, 310:329]
    avg1 = np.average(roi, axis=0)
    avg2 = np.average(avg1, axis=0)
    avg2_int = avg2.astype(int)
    avg2_int = avg2_int[::-1]           #reversed for rgb 
   # avg2_int_tup = tuple(avg2_int)
    r = avg2_int[0]
    g = avg2_int[1]
    b = avg2_int[2]

    new = getColorName(r,g,b)

    mixer.music.load('ColorFiles(en)/' + new +'.mp3')
    mixer.music.play()
    #print(GPIO.input(btn_pin))
    time.sleep(0.5)



while True:
    count = 0
    success, img = cap.read()
	time.sleep(0.1)
    imgContour = img.copy()
    
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.01)
        if (GPIO.input(btn_pin) == False):
        	time.sleep(0.2)
        	if (GPIO.input(btn_pin) == True):
        		count+=1
        		if(st_time==-1):
        			st_time = time.time()

        		count +=1

	if(st_time!=-1):
		if(time.time()-st_time>1 and time.time()-st_time<1.5):
			if(count==1):
				if(mode):
					func_mode1()
				else:
					func_mode2()

			else:
				mode = not mode
				if(mode):
					#sound
				else:
					#sound


			count=0
			st_time=-1;

		if(time.time()-st_time>1.5):
			count=0
			st_time=-1

			
cap.release()

cv2.destroyAllWindows()

"""