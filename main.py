import cv2, re, imutils, subprocess
import numpy as np
import RPi.GPIO as GPIO
import subprocess, shlex, time
from imutils import contours
from subprocess import Popen, PIPE
from imutils.perspective import four_point_transform


buttonpin = [10,11,12]
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

GPIO.setmode(GPIO.BOARD)
for i in buttonpin:
    GPIO.setup(i, GPIO.IN)

# Low HSV values
LowDict={
    "phred1" : [0, 25, 125],
    "phred2" : [145, 45, 95],
    "phblue1": [30, 40, 64],
    "phblue2": [161,20,60],
    "red":     [170,130,130],
    "brown":   [5,100,55],
    "blueblack1": [70,15,2],
    "blueblack2": [0,0,5],
    "green":   [35,95,56],
    "orange":  [4,20,140],
    "violet":  [115,15,90],
    "pink":    [138,120,100],
    "white":   [0,0,119],
    "yellow":  [18,92,102],
    "wheatish":[20,71,116],
    "blue":    [95,60,91],
    "ngreen":  [70,157,138]
}
# High HSV values
HighDict={
    "phred1" : [13, 250, 250],
    "phred2" : [180, 250, 250],
    "phblue1": [134, 208, 201],
    "phblue2": [179,45,128],
    "red":     [179,255,250],
    "brown":   [22,235,110],
    "blueblack1": [138,120,60],
    "blueblack2": [2,75,75],
    "green":   [73,255,139],
    "orange":  [8,216,210],
    "violet":  [145,170,200],
    "pink":    [165,255,186],
    "white":   [165,39,176],
    "yellow":  [30,203,190],
    "wheatish":[22,100,140],
    "blue":    [110,220,200],
    "ngreen":  [152,255,255]    
}

AllCol = ["red","brown","green","blueblack1","blueblack2","pink","orange","yellow","wheatish","blue","violet"]
AllPhCol = ["phred1","phred2","phblue1","phblue2"]

"""
#######################################################################################################################
                                                        Main Code
#######################################################################################################################
"""



def speakup(val):
    subprocess.call(['mpg321']+['/home/pi/BTP/music/'+ val +'.mp3'])
    return 

speakup('welcome')

def CountPixel( col, hsv_frame, v=0 ):
    lef = np.array( [ LowDict[col][0] - v,LowDict[col][1] - v,LowDict[col][2] - v ])
    rig = np.array( [ HighDict[col][0] + v, HighDict[col][1] + v, HighDict[col][2] + v ])
    colmask = cv2.inRange(hsv_frame, lef, rig)
    return cv2.countNonZero(colmask)

while True:
    success, img = cap.read()
    time.sleep(0.1)
    roi = img[5:265, 150:490]
    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    if(GPIO.input(buttonpin[0]== False)):
        speakup('colordetector')

        # roi = img[5:265, 150:490]
        # hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        if(GPIO.input(buttonpin[1]== False)):
            speakup('colordetectionmode')

            if(GPIO.input(buttonpin[1]== False)):
                PhDetectionMode(hsv_frame)

        if(GPIO.input(buttonpin[2]== False)):
            speakup('phdetectionmode')

            if(GPIO.input(buttonpin[1]== False):
                ColorDetectionMode(hsv_frame)
    else:
        speakup('numberdetector')

        if(GPIO.input(buttonpin[1]== False) || GPIO.input(buttonpin[2]== False)):
            time.sleep(0.01)
            if(GPIO.input(buttonpin[1]== False) || GPIO.input(buttonpin[2]== False)):
                NumberDetector(hsv_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #cv2.imshow('CAMERA',img)
        
cap.release()
cv2.destroyAllWindows()




"""
#######################################################################################################################
                                                        Color Detector
#######################################################################################################################
"""


def PhDetectionMode(hsv_frame):
    result = "nopaperfound"
    pixcount = 100
    for i in AllPhCol:
        currpixcount = CountPixel(i,hsv_frame) 
        if(pixcount < currpixcount):
            result = i
            pixcount = currpixcount

    print(result)
    speakup(result)


def ColorDetectionMode(hsv_frame):
    result = "white"
    pixcount = 250
    minpixcount = pixcount
    v=0
    if(CountPixel("white",hsv_frame,v) > 50000):
        speakup(result)
        return 

    while True:
        for i in AllCol:
            currpixcount = CountPixel(i,hsv_frame,v) 
            if(pixcount < currpixcount):
                result = i
                pixcount = currpixcount
        if(pixcount > minpixcount):
            break
        v=1+2*v;

    speakup(result)


"""
#######################################################################################################################
                                                        Number Detector
#######################################################################################################################
"""



def bird_view(image, hsv_frame):
    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 220, 92, 255)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None

    # loop over the contours
    val=0, max_val=-1, warped=0, output=0, err = 0
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the contour has four vertices, then we have found the display
        if len(approx) == 4:
            displayCnt = approx
            warped_0 = four_point_transform(gray, displayCnt.reshape(4, 2))
            output_0 = four_point_transform(image, displayCnt.reshape(4, 2))
            val = CountPixel( "ngreen", hsv_frame, v=0 ):
            if(val>max_val):
                max_val = val
                warped = warped_0
                output = output_0
                err = 1

    return warped, output, err

def NumberDetector(hsv_frame):
    roi = image[150:450, 150:490]
    #cv2.imshow('CAMERAa',roi)
    #cv2.rectangle(img, (150,150), (490,450), (0,255,0), 1)
    warped, output, err = bird_view(image,hsv_frame)
    if(err==0):
        print("screen not found")
        speakup('noscreenfound')
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
        print("adaptive threshold error")
        speakup("tryagain")
        return

    kernel = np.ones((4,4),np.uint8)
    output = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((2,2),np.uint8)
    output = cv2.erode(output,kernel,iterations = 1)
    cv2.imwrite(r'/home/pi/a.jpg', output)

    cmd = "ssocr --number-digits=-1 --charset=digits -T a.jpg"
    process = Popen(shlex.split(cmd), stdout=PIPE)
    (out, err)=process.communicate()
    #print(err)
    #digits
    out=out.decode("utf-8") 
    temp = "".join(re.findall(r'\d+', out))
    
    length = len(temp)
    if(length < 3):
        print("seg fault try again")
        speakup('error')
        return

    indices = [0,length-2,length]
    parts = [temp[i:j] for i,j in zip(indices, indices[1:]+[None])]

    print(temp)
    speakup(str(parts[0]))
    speakup('p'+str(parts[1]))
    speakup('grams')



