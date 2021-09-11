import cv2, re, imutils, subprocess
import numpy as np
import RPi.GPIO as GPIO
import subprocess, shlex, time
from imutils import contours
from subprocess import Popen, PIPE
from imutils.perspective import four_point_transform


btn_pin = 15
st_time = -1
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
Try = 0;
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
count = 0



def speakup(val):
    subprocess.call(['mpg321']+['/home/pi/BTP/music/'+ val +'.mp3'])
    return 


#speakup('tone5')
speakup('welcome')
speakup('colordetectionmode')


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




def func_mode1(v):
    if(v>1000):
        speakup('tryagain')
        return
    print(" ",v)
    
    # roi = img[150:350, 200:400]
    roi = img[5:255, 150:490]
    #cv2.imshow('CAMERAa',roi)
    #cv2.rectangle(img, (150,50), (490,300), (0,255,0), 1)

    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    low_pink = np.array([138-v, 120-v, 100-v])
    high_pink = np.array([165+v, 255+v, 186+v])
    pink_mask = cv2.inRange(hsv_frame, low_pink, high_pink)
    pink = cv2.countNonZero(pink_mask)

    low_vio = np.array([115-v, 15-v, 90-v])
    high_vio = np.array([145+v, 170+v,200+v])
    vio_mask = cv2.inRange(hsv_frame, low_vio, high_vio)
    vio = cv2.countNonZero(vio_mask)
    
    low_whe = np.array([20-v, 71-v, 116-v])
    high_whe = np.array([22+v, 100+v,140+v])
    whe_mask = cv2.inRange(hsv_frame, low_whe, high_whe)
    whe = cv2.countNonZero(whe_mask)
    
    low_bla = np.array([70-v, 15-v, 2-v])
    high_bla = np.array([138+v, 120+v,60+v])
    bla_mask = cv2.inRange(hsv_frame, low_bla, high_bla)
    bla = cv2.countNonZero(bla_mask)
    
    low_bla = np.array([0, 0, 5])
    high_bla = np.array([2+v, 75+v,75+v])
    bla_mask = cv2.inRange(hsv_frame, low_bla, high_bla)
    bla += cv2.countNonZero(bla_mask)


    low_yell = np.array([18-v, 92-v, 102-v])
    high_yell = np.array([30+v, 203+v, 190+v])
    yell_mask = cv2.inRange(hsv_frame, low_yell, high_yell)
    yell = cv2.countNonZero(yell_mask)

    low_green = np.array([35-v, 95-v, 56-v])
    high_green = np.array([73+v, 255,139+v])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.countNonZero(green_mask)


    low_blue = np.array([95-v, 60-v, 91-v])
    high_blue = np.array([110+v, 220+v, 200+v])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.countNonZero(blue_mask)


    low_red = np.array([170-v, 130-v, 130-v])
    high_red = np.array([179+v, 255, 250])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.countNonZero(red_mask)

    low_ora = np.array([4-v, 20-v, 140-v])
    high_ora = np.array([8+v, 216+v, 210+v])
    ora_mask = cv2.inRange(hsv_frame, low_ora, high_ora)
    ora = cv2.countNonZero(ora_mask)
    
    low_whi = np.array([0, 0, 118-v])
    high_whi = np.array([165+v, 39+v, 176+v])
    whi_mask = cv2.inRange(hsv_frame, low_whi, high_whi)
    whi = cv2.countNonZero(whi_mask)
    
    low_bro = np.array([5-v, 100-v, 55-v])
    high_bro = np.array([22+v, 235+v, 110+v])
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

    if(margin < 200 and whi >=50000 ):
        new='white'
        print(whi)
    if(margin < 200 and whi< 50000 ):
        #new='newcolor'
        func_mode1(1+2*v)
        return
    
    print(new)
    speakup(new) 

#speakup('pass')
while True:
    success, img = cap.read()
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
            #print(count)
            if(count==1):
                #print(mode)
                if(mode):
                    #print("m1")
                    func_mode1(0)
                else:
                    #print("m2")
                    image=img
                    num_det()

            else:
                mode = not mode
                if(mode):
                    print("changed mode 1")
                    speakup('colordetectionmode')

                else:
                    print("changed mode 2")
                    speakup('numberdetector')
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





