import cv2
import numpy as np
import pandas as pd
import time
import RPi.GPIO as GPIO
# import pyttsx3
from pygame import mixer




btn_pin = 15
mode = 1 # 1 for color and 0 for ph
st_time = -1
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
prev_result = "nill"
count = 0

engine = pyttsx3.init('espeak')
engine.setProperty('rate', 160)
engine.setProperty('volume',1.0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
mixer.init()
engine.say('Hello Boys') 
engine.runAndWait()

def func_mode2():

    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

     # Red color
    low_red = np.array([0, 60, 105])
    high_red = np.array([21, 187, 175])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    Red = cv2.countNonZero(red_mask)

    # Blue color
    low_blue = np.array([70, 58, 15])
    high_blue = np.array([125, 235, 190])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    Blue = cv2.countNonZero(blue_mask)

    # ph color
    low_green = np.array([16, 40, 86])
    high_green = np.array([35, 180, 205])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    Ph = cv2.countNonZero(green_mask)

    if(Red > Blue and Red > 50):
        print("red")
        mixer.music.load('music/' + "red" +'.mp3')
        channel = mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        # engine.say('red') 
        # engine.runAndWait() 

    elif(Blue > Red and Blue> 50 ):
        print("blue")
        mixer.music.load('music/' + "blue" +'.mp3')
        channel = mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        # engine.say('blue') 
        # engine.runAndWait() 

    elif(Ph > 2000 ):
        print("ph paper ",Ph )
        mixer.music.load('music/' + "phpaper" +'.mp3')
        channel = mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        # engine.say('paper detected') 
        # engine.runAndWait() 

    else:
        print("no")
        mixer.music.load('music/' + "nopaperfound" +'.mp3')
        channel = mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        # engine.say('no paper detected') 
        # engine.runAndWait() 



def func_mode1():

    
    roi = img[150:350, 200:400]
    #cv2.imshow('CAMERAa',roi)

    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

     # Red color
    low_pink = np.array([138, 50, 60])
    high_pink = np.array([166, 255, 186])
    pink_mask = cv2.inRange(hsv_frame, low_pink, high_pink)
    pink = cv2.countNonZero(pink_mask)

    low_vio = np.array([94, 21, 9])
    high_vio = np.array([165, 134, 217])
    vio_mask = cv2.inRange(hsv_frame, low_vio, high_vio)
    vio = cv2.countNonZero(vio_mask)


    low_yell = np.array([25, 65, 95])
    high_yell = np.array([47, 125, 195])
    yell_mask = cv2.inRange(hsv_frame, low_yell, high_yell)
    yell = cv2.countNonZero(yell_mask)

    low_green = np.array([30, 163, 46])
    high_green = np.array([67, 227,179])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.countNonZero(green_mask)


    low_blue = np.array([91, 185, 121])
    high_blue = np.array([129, 255, 201])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.countNonZero(blue_mask)


    low_red = np.array([155, 150, 155])
    high_red = np.array([180, 255, 250])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.countNonZero(red_mask)

    new = max(pink, green, yell, red, blue, vio)
    print (new)
    if new==pink:
        print("pink")
        new = "pink"
    elif new==green:
        print("green")
        new = "green"
    elif new==yell:
        print("yellow")
        new = "yellow"
    elif new==red:
        print("red")
        new = "red"
    elif new==blue:
        print("blue")
        new = "blue"
    else:
        print("vio")
        new = "violet"
    #print (new)
    mixer.music.load('music/' + new +'.mp3')
        channel = mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
    # engine.say(new) 
    # engine.runAndWait() 

mixer.music.load('music/' + "press" +'.mp3')
channel = mixer.music.play()
while mixer.music.get_busy():
            time.sleep(0.1)

while True:
    success, img = cap.read()
    cv2.rectangle(img, (200,150), (400,350), (0,255,0), 1) 
    time.sleep(0.1)
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.01)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.3)
            if (GPIO.input(btn_pin) == True):
                count+=1
                if(st_time==-1):
                    st_time = time.time()

    if(st_time!=-1):
        if(time.time()-st_time>1 and time.time()-st_time<1.5):
            print(count)
            if(count==1):
                print(mode)
                if(mode):
                    print("m1")
                    func_mode1()
                else:
                    print("m2")
                    func_mode2()

            else:
                mode = not mode
                if(mode):
                    print("changed mode 1")
                    mixer.music.load('music/' + "colordetectionmode" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    # engine.say('color detection mode') 
                    # engine.runAndWait() 

                else:
                    print("changed mode 2")
                    mixer.music.load('music/' + "paperdetectionmode" +'.mp3')
                    channel = mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    # engine.say('paper detection mode') 
                    # engine.runAndWait() 
            count=0
            st_time=-1;

        if(time.time()-st_time>1.5):
            count=0
            st_time=-1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

    #img = cv2.flip(img,1)
    
    cv2.imshow('CAMERA',img)
        
cap.release()

cv2.destroyAllWindows()

