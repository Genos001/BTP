import re
import cv2
import time
import shlex
import imutils
import subprocess
import numpy as np
import RPi.GPIO as GPIO
from imutils import contours
from subprocess import Popen, PIPE
from imutils.perspective import four_point_transform




btn_pin = 15
mode = 1
st_time = -1
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
Try = 0;
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
# mixer.init()


print("start")
def speakup(val):
    subprocess.call(['mpg321']+['/home/pi/BTP/music/'+ val +'.mp3'])
    return

#speakup('tone4')
speakup('welcome')


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
            low_green = np.array([70, 157, 138])
            high_green = np.array([152, 255, 255])
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)
            val = cv2.countNonZero(green_mask)

            if(val>max_val):
                max_val = val
                warped = warped_0
                output = output_0
                err = 1

    return warped, output, err

def num_det():
    roi = image[150:450, 150:490]
    #cv2.imshow('CAMERAa',roi)
    #cv2.rectangle(img, (150,150), (490,450), (0,255,0), 1)
    warped, output, err = bird_view(image)
    if(err==0):
        print("screen not found",Try)
        if(Try>2):
            speakup('noscreenfound')
        else:
            num_det(Try)
        #if(True):
        return;
        
    #cv2.imshow('imag',output)
    height, width, channels = output.shape
    x0=int(width/6)+3
    y0=5
    x1=width-8
    y1=height-10
    output = output[y0:y1, x0:x1]
    try:
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY) 
        output = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
    except:
        print("adaptive threshold error ",tries)
        if(tries>0):
            num_det(tries)
        elif(tries==0):
            speakup('error')
            tries=tries-1;
        return

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
    temp = "".join(re.findall(r'\d+', out))
    
    length = len(temp)
    if(length < 3):
        print("seg fault try again ",tries)
        if(tries>0):
            num_det(tries)
        elif(tries==0):
            speakup('error')
            tries=tries-1;
        return

    indices = [0,length-2,length]
    parts = [temp[i:j] for i,j in zip(indices, indices[1:]+[None])]
    
    print(temp)

    speakup(str(parts[0]))
    speakup('p'+str(parts[1]))
    speakup('grams')


def start_func():



while True:
    success, image = cap.read()
    time.sleep(0.1)
    if (GPIO.input(btn_pin) == False):
        time.sleep(0.02)
        if (GPIO.input(btn_pin) == False):
            time.sleep(0.4)
            if (GPIO.input(btn_pin) == True):
                
                success, image = cap.read() 
                num_det()
                print("----------------------------------")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #cv2.imshow('CAMERA',image)
        
cap.release()

cv2.destroyAllWindows()

#cv2.imwrite(r'C:\Users\viish\Desktop\nat_out\NRE4'+ str(i) +'.jpg', output)
