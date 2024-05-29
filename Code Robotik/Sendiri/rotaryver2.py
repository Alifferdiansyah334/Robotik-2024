import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the rotary encoder
CLK = 17
DT = 18
SW = 27  # Optional, if you want to use the switch

# Setup the GPIO pins as input
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Optional

# Initialize variables
counter = 0
clkLastState = GPIO.input(CLK)

def rotary_encoder():
    global counter
    clkState = GPIO.input(CLK)
    dtState = GPIO.input(DT)

    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
        print(f"Counter: {counter}")

try:
    while True:
        rotary_encoder()
        clkLastState = GPIO.input(CLK)
        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()