import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

#Ultrasonik
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 4
GPIO_ECHO = 17
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
counter = 0

#lcd
lcd = CharLCD('PCF8574', 0x27)

#button
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)

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

try:
    while True:
        lcd.clear()
        dist = int(distance())
        distm = dist / 100
        distmm = dist * 10
        print(dist)
        button_state = GPIO.input(27)
        
        if button_state == False:
            counter += 1
            print(counter)
            print('Button Pressed...')
            
        if counter == 1:
            lcd.write_string(f"Jarak cm: {dist}")
            time.sleep(1) 
        elif counter == 2:
            print(counter)
            print('Button Pressed...')
            lcd.write_string(f"Jarak m: {distm}")
            time.sleep(1) 
        elif counter == 3:
            print(counter)
            print('Button Pressed...')
            lcd.write_string(f"Jarak mm: {distmm}")
            time.sleep(1) 
        else:
            counter = 1
            
except KeyboardInterrupt:
  GPIO.cleanup()