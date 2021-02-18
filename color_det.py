import cv2
import numpy as np
import pandas as pd
import time
import RPi.GPIO as GPIO
import subprocess
import shlex
#from pygame import mixer


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


GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
#mixer.init()



def speakup(val):
    subprocess.call(['mpg321']+['/home/pi/BTP/music/'+ val +'.mp3'])
    return 


#speakup('tone5')
speakup('welcome')
speakup('colordetectionmode')


def getColorName(R,G,B):
    index=["color_name","R","G","B"]
    csv = pd.read_csv('colorsV4.csv', names=index, header=None,encoding='latin-1')
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname


def func_mode2():
    roi = img[5:300, 150:490]
    # cv2.rectangle(img, (150,100), (490,350), (0,255,0), 1)
    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

     # Red color
    low_red = np.array([0, 25, 125])
    high_red = np.array([13, 250, 250])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    Red = cv2.countNonZero(red_mask)
    
    low_red = np.array([145, 45, 95])
    high_red = np.array([180, 250, 250])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    Red += cv2.countNonZero(red_mask)

    # Blue color
    low_blue = np.array([30, 40, 94])
    high_blue = np.array([154, 208, 201])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    Blue = cv2.countNonZero(blue_mask)
    
    low_blue = np.array([161,20,60])
    high_blue = np.array([179,45,128])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    Blue += cv2.countNonZero(blue_mask)

    # ph colorcd ..
    low_green = np.array([16, 40, 86])
    high_green = np.array([35, 180, 205])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    Ph = cv2.countNonZero(green_mask)
    print(Red," ", Blue)
    if(Red > Blue and Red > 200):
        print("red")
        speakup('red')

    elif(Blue > Red and Blue> 500 ):
        print("blue")
        speakup('blue') 

    elif(Ph > 2000 ):
        print("ph paper ",Ph )
        speakup('phpaper') 

    else:
        print("no")
        speakup('blue') 



def func_mode1(v):
    if(v>1000):
        speakup('tryagain')
        return
    
    # roi = img[150:350, 200:400]
    roi = img[5:255, 150:490]
    #cv2.imshow('CAMERAa',roi)
    #cv2.rectangle(img, (150,50), (490,300), (0,255,0), 1)

    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    low_pink = np.array([138-v, 120-v, 100-v])
    high_pink = np.array([165+v, 255+v, 186+v])
    pink_mask = cv2.inRange(hsv_frame, low_pink, high_pink)
    pink = cv2.countNonZero(pink_mask)

    low_vio = np.array([90-v, 55-v, 90-v])
    high_vio = np.array([145+v, 180+v,190+v])
    vio_mask = cv2.inRange(hsv_frame, low_vio, high_vio)
    vio = cv2.countNonZero(vio_mask)
    
    low_whe = np.array([20-v, 71-v, 116-v])
    high_whe = np.array([22+v, 100+v,140+v])
    whe_mask = cv2.inRange(hsv_frame, low_whe, high_whe)
    whe = cv2.countNonZero(whe_mask)
    
    low_bla = np.array([70-v, 20-v, 2-v])
    high_bla = np.array([138+v, 120+v,120+v])
    bla_mask = cv2.inRange(hsv_frame, low_bla, high_bla)
    bla = cv2.countNonZero(bla_mask)


    low_yell = np.array([18-v, 137-v, 102-v])
    high_yell = np.array([30+v, 203+v, 190+v])
    yell_mask = cv2.inRange(hsv_frame, low_yell, high_yell)
    yell = cv2.countNonZero(yell_mask)

    low_green = np.array([35-v, 95-v, 56-v])
    high_green = np.array([73+v, 255+v,139+v])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.countNonZero(green_mask)


    low_blue = np.array([95-v, 75-v, 91-v])
    high_blue = np.array([122+v, 220+v, 190+v])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.countNonZero(blue_mask)


    low_red = np.array([155-v, 140-v, 140-v])
    high_red = np.array([179+v, 255+v, 250+v])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.countNonZero(red_mask)

    low_ora = np.array([1-v, 60-v, 130-v])
    high_ora = np.array([8+v, 216+v, 210+v])
    ora_mask = cv2.inRange(hsv_frame, low_ora, high_ora)
    ora = cv2.countNonZero(ora_mask)
    
    low_whi = np.array([0, 0, 118-v])
    high_whi = np.array([165+v, 39+v, 176+v])
    whi_mask = cv2.inRange(hsv_frame, low_whi, high_whi)
    whi = cv2.countNonZero(whi_mask)
    
    low_bro = np.array([1-v, 150-v, 55-v])
    high_bro = np.array([12+v, 235+v, 136+v])
    bro_mask = cv2.inRange(hsv_frame, low_bro, high_bro)
    bro = cv2.countNonZero(bro_mask)

    margin = max(bla, pink, green, yell, red, blue, vio, ora, whe, bro)
    print (margin)
    if margin==pink:
        new = "pink"
    elif margin==green:
        new = "green"
    elif margin==yell:
        new = "yellow"
    elif margin==red:
        new = "red"
    elif margin==blue:
        new = "blue"
    elif margin==whe:
        new = "wheatish"
    elif margin==ora:
        new = "orange"
    elif margin==bla:
        new = "blueblack"
    elif margin==bro:
        new = "brown"
    else:
        new = "violet"
    #print (new)

    # cv2.rectangle(img, (309,229), (329,249), (0,255,0), 1)

    if(margin < 50 and whi >=25000 ):
        new='white'
        print(whi)
    if(margin < 50 and whi< 25000 ):
        #new='newcolor'
        func_mode1(1+2*v)
        return
    
    print(new)
    speakup(new) 

#speakup('pass')
while True:
    success, img = cap.read()
    #cv2.rectangle(img, (200,150), (400,350), (0,255,0), 1) 
    #cv2.rectangle(img, (150,5), (490,300), (0,255,0), 1)

    time.sleep(0.1)
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.01)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.2)
            # if (GPIO.input(btn_pin) == True):
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
                    func_mode1(0)
                else:
                    print("m2")
                    func_mode2()

            else:
                mode = not mode
                if(mode):
                    print("changed mode 1")
                    speakup('colordetectionmode')

                else:
                    print("changed mode 2")
                    speakup('paperdetectionmode')
            count=0
            st_time=-1;

        if(time.time()-st_time>1.5):
            count=0
            st_time=-1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
    #cv2.imshow('CAMERA',img)
        
cap.release()

cv2.destroyAllWindows()

