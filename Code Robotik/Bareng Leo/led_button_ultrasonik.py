import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False) 


# Led Setup
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# -> Ultrasonik Function
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 

while True:

    button_state = GPIO.input(22)

    dist = int(distance())
    print (f"Jarak = {dist} cm" )
    print(type(dist))
    time.sleep(0.5)

    if button_state == False  and dist <= 10:
        GPIO.output(13, GPIO.HIGH)
    elif button_state == False and dist >= 20:
        print("button Press")
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)
    elif button_state == False and dist >= 30:
        print("button Press")
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)
    else:    
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)
        