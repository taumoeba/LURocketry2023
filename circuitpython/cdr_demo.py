# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
import digitalio
import pulseio
from adafruit_motor import stepper
from adafruit_motor import servo
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

bigPWM = pulseio.PWMOut(board.D13, frequency=50)
smallPWM = pulseio.PWMOut(board.D11, frequency=50)

bigServo = servo.ContinuousServo(bigPWM, min_pulse=750, max_pulse=2250)
smallServo = servo.Servo(smallPWM, min_pulse=750, max_pulse=2250)

"""
while True:
    # forward is clockwise. for payload, backward is "up"
    res = kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    #print(res)
    #led.value = True
    #time.sleep(0.5)
    #led.value = False
    time.sleep(0.01)
"""

# extend payload using stepper
curr = time.time()
while time.time() - curr <= 10:
    steps = kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    time.sleep(0.01)

# flip up camera
smallServo.angle = 90

# rotate camera
curr = time.time()
bigServo.throttle = 0.1
while time.time() - curr <= 2:
    time.sleep(0)
bigServo.throttle = 0

# rotate camera back
curr = time.time()
bigServo.throttle = -0.1
while time.time() - curr <= 2:
    time.sleep(0)
bigServo.throttle = 0

# flip camera back down
smallServo.angle = 0

# retract payload using stepper
curr = time.time()
while time.time() - curr <= 10:
    steps = kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    time.sleep(0.01)
