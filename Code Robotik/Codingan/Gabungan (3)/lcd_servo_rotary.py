# --> Semua import
import RPi.GPIO as GPIO

# --> Import untuk LCD I2C untuk LCD I2C
from RPLCD.i2c import CharLCD
import time

# --> Alamat untuk LCD
lcd = CharLCD('PCF8574', 0x27)

# --> PIN Untuk Rotary Encoder
CLK_PIN = 18
DT_PIN = 15 
SW_PIN = 14 

# --> Deklarasi untuk variable searah dan berlawanan dengan jarum jam
DIRECTION_CW = 0
DIRECTION_CCW = 1

# --> inisialisasi duty untuk derajat servo 2 sampai 12 (2 = 0, 12 = 180)
duty = 2

# --> Variabel counter untuk menghitung nilai rotary
counter = 0
direction = DIRECTION_CW
CLK_state = 0
prev_CLK_state = 0

# --> Inisialisasi state awal button
button_pressed = True
prev_button_state = GPIO.HIGH

# --> Untuk setup pin untuk rotary
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --> Untuk setup pin servo dan frekuensi servo
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50)

# --> Untuk memulai servo
servo1.start(0)

prev_CLK_state = GPIO.input(CLK_PIN)

# --> Fungsi untuk konversi nilai derajat servo dari 2 sampai 12 menjadi 0 sampai 180
def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)
    
    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)

try:
    while True:

        # --> Clear lcd untuk kondisi awal
        lcd.clear()
        
        # --> Logic untuk rotary searah jarum dan berlawanan dengan jarum jam
        CLK_state = GPIO.input(CLK_PIN)

        if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                counter -= 5
                direction = DIRECTION_CCW
            else:
                counter += 5
                direction = DIRECTION_CW

            print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE",
                  "- count:", counter)
            
            counterstr = str(counter)
            setAngle(counter)
            lcd.write_string(f'Nilai Counter:{counterstr}')

            time.sleep(0.5)
        prev_CLK_state = CLK_state

        # --> Logic untuk rotary button 
        button_state = GPIO.input(SW_PIN)
        if button_state != prev_button_state:
            time.sleep(0.01)
            if button_state == GPIO.LOW:
                lcd.write_string('Button Pressed')
                counter = 0
                setAngle(duty)
                time.sleep(1) 
                button_pressed = True
            else:
                button_pressed = False
        prev_button_state = button_state

except KeyboardInterrupt:
    GPIO.cleanup()