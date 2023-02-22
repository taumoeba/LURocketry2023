# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
import digitalio
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

kit = MotorKit(i2c=board.I2C())

while True:
    # forward is clockwise
    res = kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    print(res)
    #led.value = True
    #time.sleep(0.5)
    #led.value = False
    time.sleep(0.01)