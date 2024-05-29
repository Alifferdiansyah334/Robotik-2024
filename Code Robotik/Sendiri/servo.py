# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
#servo1.stop()

# keatas enting
print ("Waiting for 2 seconds")
time.sleep(2)

#Let's move the servo!
print ("Rotating 180 degrees in 10 steps")

# Define variable duty
duty = 2

# Loop for duty values from 2 to 12 (0 to 180 degrees)
while duty <= 12:
    servo1.ChangeDutyCycle(duty) #untuk mengubah derajat servo
  
    time.sleep(0.05)
    servo1.ChangeDutyCycle(0) #biar servo gk oleng/mengurangi jitter
    time.sleep(0.05)
  
    duty = duty + 1

# Wait a couple of seconds
time.sleep(2)

# Turn back to 90 degrees
print ("Turning back to 90 degrees for 2 seconds")
servo1.ChangeDutyCycle(7)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
time.sleep(1.5)

#turn back to 0 degrees
print ("Turning back to 0 degrees")
servo1.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)

#fungsi untuk mengubah derajat 
def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)
    
    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)

#Clean things up at the end
servo1.stop()
GPIO.cleanup()