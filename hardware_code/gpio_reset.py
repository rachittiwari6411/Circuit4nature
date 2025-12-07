#!/usr/bin/env python3
import sys
import os
import subprocess

# Kill any running Python scripts that might hold GPIO
print("Killing any running GPIO scripts...")
os.system("pkill -f 'python.*main.py' 2>/dev/null || true")
os.system("pkill -f 'python.*wasd' 2>/dev/null || true")
os.system("pkill -f 'python.*combined' 2>/dev/null || true")

import time
time.sleep(1)

try:
    import gpiod
    from gpiod import line
    
    CHIP_NAME = "/dev/gpiochip0"
    
    # Try to acquire and immediately release each pin
    all_pins = [5, 6, 12, 13, 17, 27, 23, 24, 21, 2, 3, 4, 14, 15, 18, 22, 25]
    for pin in all_pins:
        try:
            chip = gpiod.Chip(CHIP_NAME)
            settings = gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)
            req = chip.request_lines({pin: settings})
            req.release()
            chip.close()
            print(f"Released GPIO {pin}")
        except Exception as e:
            pass
    
    print("gpiod cleanup complete")
except Exception as e:
    print(f"gpiod cleanup: {e}")

try:
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    print("RPi.GPIO cleanup done")
except Exception as e:
    print(f"RPi.GPIO cleanup: {e}")

print("GPIO reset complete - try running your script now")
