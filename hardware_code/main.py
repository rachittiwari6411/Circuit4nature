#!/usr/bin/env python3
"""
Pothole bot drive - WASD keyboard control
Raspberry Pi 5 + L298N (GPIO 17,27,23,24)
W=forward, A=left, S=backward, D=right, Q=quit
"""

import gpiod
from gpiod import line
import time
import sys
import termios
import tty
import select

# GPIO pins
LEFT_IN1 = 17   # Left motor +
LEFT_IN2 = 27   # Left motor -
RIGHT_IN3 = 23  # Right motor +
RIGHT_IN4 = 24  # Right motor -

CHIP_NAME = "/dev/gpiochip0"

chip = gpiod.Chip(CHIP_NAME)
settings = gpiod.LineSettings(direction=line.Direction.OUTPUT)
lines = chip.request_lines({LEFT_IN1: settings, LEFT_IN2: settings, RIGHT_IN3: settings, RIGHT_IN4: settings})

def set_pins(left1, left2, right1, right2):
    values = {
        LEFT_IN1: line.Value.ACTIVE if left1 else line.Value.INACTIVE,
        LEFT_IN2: line.Value.ACTIVE if left2 else line.Value.INACTIVE,
        RIGHT_IN3: line.Value.ACTIVE if right1 else line.Value.INACTIVE,
        RIGHT_IN4: line.Value.ACTIVE if right2 else line.Value.INACTIVE,
    }
    lines.set_values(values)

def stop():
    set_pins(0, 0, 0, 0)

def forward():
    set_pins(1, 0, 1, 0)    # Both forward

def backward():
    set_pins(0, 1, 0, 1)    # Both backward - FIXED

def turn_left():
    set_pins(0, 1, 1, 0)    # Left BACKWARD + Right FORWARD = turn left

def turn_right():
    set_pins(1, 0, 0, 1)    # Left FORWARD + Right BACKWARD = turn right
    
def getch():
    """Non-blocking single key press"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            return key.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

if __name__ == "__main__":
    print("WASD bot control started!")
    print("W=forward, A=left, S=back, D=right, Q=quit")
    print("Press keys rapidly - 0.2s timeout per loop")
    
    try:
        while True:
            key = getch()
            
            if key == 'w':
                print("Forward!")
                forward()
            elif key == 's':
                print("Backward!")
                backward()
            elif key == 'a':
                print("Left!")
                turn_left()
            elif key == 'd':
                print("Right!")
                turn_right()
            elif key == 'q':
                print("Quitting...")
                break
            else:
                stop()
            
            time.sleep(0.2)  # Loop speed
            
    except KeyboardInterrupt:
        print("\nStopped by Ctrl+C")
    finally:
        stop()
        lines.release()
        chip.close()
