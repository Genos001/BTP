from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
#from PIL import Image
from pygame import mixer
import shlex
from subprocess import Popen, PIPE
import re
# import pyttsx3



btn_pin = 15
st_time = -1
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# engine = pyttsx3.init('espeak')
# engine.setProperty('rate', 130)
# engine.setProperty('volume',1.0)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
mixer.init()



def bird_view(image):
    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 220, 92, 255)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None

    # loop over the contours
    val=0 
    max_val=-1
    warped=0
    output=0
    err = 0
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the contour has four vertices, then we have found
        # the display
        if len(approx) == 4:
            displayCnt = approx
            warped_0 = four_point_transform(gray, displayCnt.reshape(4, 2))
            output_0 = four_point_transform(image, displayCnt.reshape(4, 2))

            hsv_frame = cv2.cvtColor(output_0, cv2.COLOR_BGR2HSV)
            low_green = np.array([70, 229, 188])
            high_green = np.array([152, 255, 255])
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)
            val = cv2.countNonZero(green_mask)

            if(val>max_val):
                max_val = val
                warped = warped_0
                output = output_0
                err = 1


            # break
    # warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    # output = four_point_transform(image, displayCnt.reshape(4, 2))
    return warped, output, err

while True:
    success, image = cap.read()
    time.sleep(0.1)
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.02)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.4)
            if (GPIO.input(btn_pin) == True):

                warped, output, err = bird_view(image)
                if(err==0):
                    print("screen not found try again")
                    mixer.music.load('music/' + "noscreenfound" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    mixer.music.load('music/' + "tryagain" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)

                    continue
                
                height, width, channels = output.shape
                x0=int(width/6)+3
                y0=5
                x1=width-8
                y1=height-10
                output = output[y0:y1, x0:x1]
                try:
                    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                except:
                    print("error")
                #cv2.rectangle(output, (x0,y0), (x1,y1), (0,255,0), 1)
                
                # output = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                #         cv2.THRESH_BINARY, 11, 2)
                try:
                    print("applying adp")
                    output = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                                      cv2.THRESH_BINARY, 11, 2)
                except:
                    print("adaptive threshold error")
                    mixer.music.load('music/' + "error" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)

                    mixer.music.load('music/' + "tryagain" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)

                #cv2.imshow('output',output)
                kernel = np.ones((4,4),np.uint8)
                output = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)
                kernel = np.ones((2,2),np.uint8)
                output = cv2.erode(output,kernel,iterations = 1)
                cv2.imwrite(r'/home/pi/a.jpg', output)
                #cv2.imshow('output2',output)
            
                cmd = "ssocr --number-digits=-1 --charset=digits -T a.jpg"
                process = Popen(shlex.split(cmd), stdout=PIPE)
                (out, err)=process.communicate()
                print(err)
                #digits
                out=out.decode("utf-8") 
                temp = ",".join(re.findall(r'\d+', out))
                
                length = len(temp)
                if(length < 3):
                    print("seg fault try again")
                    mixer.music.load('music/' + "error" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)

                    mixer.music.load('music/' + "tryagain" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    continue

                indices = [0,length-2,length]
                parts = [temp[i:j] for i,j in zip(indices, indices[1:]+[None])]
                
                print(temp)
                print(parts)

                mixer.music.load('music/' + str(parts[0]) +'.mp3')
                channel = mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(0.1) 

                mixer.music.load('music/p' + str(parts[1]) +'.mp3')
                channel = mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(0.1)

                mixer.music.load('music/' + "grams" +'.mp3')
                channel = mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(0.1)

                # engine.say(parts[0]) 
                # engine.runAndWait()
                
                # engine.setProperty('rate', 250)
                # engine.say('point') 
                # engine.runAndWait()
                
                # engine.say(parts[1]) 
                # engine.runAndWait()
                
                # engine.say(parts[2]) 
                # engine.runAndWait()
                
                # engine.say('gram') 
                # engine.runAndWait()
                #exit_code = process.wait()


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #img = cv2.flip(image,1)
    
    #cv2.imshow('CAMERA',image)
        
cap.release()

cv2.destroyAllWindows()



# image = cv2.imread('../Images_to_test/z ('+str(i)+').jpeg')

# bigger = cv2.resize(image, (400, 600)) 
# # cv2.imshow('output',bigger)



# # kernel = np.ones((2,2),np.uint8)
# # output = cv2.erode(output,kernel,iterations = 1)
# #output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
# cv2.imshow('out'+str(i),output)
# #cv2.imwrite(r'C:\Users\viish\Desktop\nat_out\NRE4'+ str(i) +'.jpg', output)

# cv2.waitKey()
