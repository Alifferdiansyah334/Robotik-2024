import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D27, use_pulseio=False)

GPIO.setmode(GPIO.BCM)

#Ultrasonik Pin Setup
GPIO_TRIGGER = 4
GPIO_ECHO = 17

counter = 0

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

# Set up the LCD using the address found with i2cdetect
lcd = CharLCD('PCF8574', 0x27)

try:
    while True:

        # Clear the display
        lcd.clear()

        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        
        
        # Get Distance From Ultrasonik Function
        dist = int(distance())

        # Print To Terminal 
        print(f"Jarak = {dist} cm")

        # Print to LCD Converted Value Of Distance
        lcd.write_string(f"Jarak : {dist}")
        lcd.crlf()
        lcd.write_string(f"Suhu : {temperature_c} C")
        time.sleep(1)  

except KeyboardInterrupt:
    GPIO.cleanup()