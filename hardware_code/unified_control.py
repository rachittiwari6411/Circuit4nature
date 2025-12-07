#!/usr/bin/env python3
import os
import time
import sys
import termios
import tty
import select

class _MockGPIO:
    BCM = None
    OUT = None
    def setmode(self, mode):
        return None
    def setwarnings(self, flag):
        return None
    def setup(self, pin, mode):
        return None
    def output(self, pin, val):
        return None
    def cleanup(self):
        return None

try:
    import RPi.GPIO as GPIO
    SIMULATE = False
except Exception:
    SIMULATE = True
    GPIO = _MockGPIO()

try:
    import Adafruit_DHT
except Exception:
    Adafruit_DHT = None

if os.environ.get('SIMULATE', '').lower() in ('1', 'true', 'yes'):
    SIMULATE = True
    GPIO = _MockGPIO()

if not SIMULATE:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

DRIVER1_LEFT_IN1, DRIVER1_LEFT_IN2 = 17, 27
DRIVER1_RIGHT_IN3, DRIVER1_RIGHT_IN4 = 23, 24

DRIVER2_LEFT_IN1, DRIVER2_LEFT_IN2 = 5, 6
DRIVER2_RIGHT_IN3, DRIVER2_RIGHT_IN4 = 12, 13

DHT_PIN = 21
DHT_SENSOR = Adafruit_DHT.DHT22 if Adafruit_DHT else None

motor_pins = [DRIVER1_LEFT_IN1, DRIVER1_LEFT_IN2, DRIVER1_RIGHT_IN3, DRIVER1_RIGHT_IN4,
              DRIVER2_LEFT_IN1, DRIVER2_LEFT_IN2, DRIVER2_RIGHT_IN3, DRIVER2_RIGHT_IN4]

if not SIMULATE:
    try:
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
    except Exception as e:
        print(f"GPIO setup error: {e}")
        print("Falling back to simulation mode")
        SIMULATE = True
        GPIO = _MockGPIO()

driver1_state = [0, 0, 0, 0]
driver2_state = [0, 0, 0, 0]

def set_driver1(l1, l2, r1, r2):
    global driver1_state
    driver1_state = [l1, l2, r1, r2]
    GPIO.output(DRIVER1_LEFT_IN1, l1)
    GPIO.output(DRIVER1_LEFT_IN2, l2)
    GPIO.output(DRIVER1_RIGHT_IN3, r1)
    GPIO.output(DRIVER1_RIGHT_IN4, r2)

def set_driver2(in1, in2, in3, in4):
    global driver2_state
    driver2_state = [in1, in2, in3, in4]
    GPIO.output(DRIVER2_LEFT_IN1, in1)
    GPIO.output(DRIVER2_LEFT_IN2, in2)
    GPIO.output(DRIVER2_RIGHT_IN3, in3)
    GPIO.output(DRIVER2_RIGHT_IN4, in4)

def stop_all():
    set_driver1(0, 0, 0, 0)
    set_driver2(0, 0, 0, 0)

def forward():
    set_driver1(1, 0, 1, 0)

def backward():
    set_driver1(0, 1, 0, 1)

def turn_left():
    set_driver1(0, 1, 1, 0)

def turn_right():
    set_driver1(1, 0, 0, 1)

def motor_up_left():
    set_driver2(1, 0, 0, 0)

def motor_down_left():
    set_driver2(0, 1, 0, 0)

def motor_up_right():
    set_driver2(0, 0, 1, 0)

def motor_down_right():
    set_driver2(0, 0, 0, 1)

def motor_stop():
    set_driver2(0, 0, 0, 0)

def read_temperature():
    if SIMULATE or Adafruit_DHT is None:
        return None
    try:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            return temperature
        return None
    except Exception:
        return None

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
        if rlist:
            key = sys.stdin.read(1)
            return key.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

if __name__ == "__main__":
    stop_all()
    
    try:
        while True:
            key = getch()
            temperature = read_temperature()
            
            if key == 'w':
                forward()
            elif key == 's':
                backward()
            elif key == 'a':
                turn_left()
            elif key == 'd':
                turn_right()
            elif key == '1':
                motor_up_left()
            elif key == '2':
                motor_down_left()
            elif key == '3':
                motor_up_right()
            elif key == '4':
                motor_down_right()
            elif key == ' ':
                stop_all()
            elif key == 'q':
                break
            
            temp_str = f"Temp: {temperature:.1f}C" if temperature else "Temp: N/A"
            d1_str = f"D1:{driver1_state}" 
            d2_str = f"D2:{driver2_state}"
            print(f"{d1_str} {d2_str} {temp_str}", end='\r')
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        pass
    finally:
        stop_all()
        if not SIMULATE:
            GPIO.cleanup()
