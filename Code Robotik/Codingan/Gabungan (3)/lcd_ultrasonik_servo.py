import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import time

GPIO.setmode(GPIO.BCM)

# -> Servo Setup
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50)
servo1.start(0)
duty = 2

# -> Ultrasonik Pin Setup
GPIO_TRIGGER = 4
GPIO_ECHO = 17

# -> Ultrasonik Input Output setup
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

# --> Ultrasonik Converter Function
def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)
    
    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)


# Set up the LCD using the address found with i2cdetect
lcd = CharLCD('PCF8574', 0x27)

try:
    while True:
        
        # Clear the display
        lcd.clear()

        # Get Distance From Ultrasonik Function
        dist = int(distance())

        if dist <= 20:
            setAngle(180)
        elif dist >= 20:
            setAngle(0)
        else:
            setAngle(0)

        # Print To Terminal 
        print(f"Jarak = {dist} cm")
        time.sleep(0.5)

        # Convert Distance Value to String

        # Print to LCD Converted Value Of Distance
        lcd.write_string(f"Jarak : {dist}")
        time.sleep(1)  # Wait for 2 seconds

except KeyboardInterrupt:
    GPIO.cleanup()
