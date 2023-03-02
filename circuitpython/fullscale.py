# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
# Todo:
# - Read, interpret data from IMU
# - Save data to SD card
# - Camera
import time
import board
import digitalio
import pulseio
from adafruit_motor import stepper
from adafruit_motor import servo
from adafruit_motorkit import MotorKit
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
import adafruit_sdcard
import busio
import microcontroller
import storage
import os


kit = MotorKit(i2c=board.I2C())

SD_CS = board.D25 # Potentially change

bigPWM = pulseio.PWMOut(board.D13, frequency=50)
smallPWM = pulseio.PWMOut(board.D11, frequency=50)

bigServo = servo.ContinuousServo(bigPWM, min_pulse=750, max_pulse=2250)
smallServo = servo.Servo(smallPWM, min_pulse=750, max_pulse=2250)

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
path="/sd"

i2c = board.I2C()  # uses board.SCL and board.SDA
accel_gyro = LSM6DS(i2c)

starttime = time.monotonic()

fileCount = 0
for file in os.listdir(path):
    fileCount = fileCount + 1
    
""" IMU & SD stuff
acceleration = accel_gyro.acceleration
    gyro = accel_gyro.gyro

    with open("/sd/imu_data_%d.txt" %fileCount, "a") as f:
        led.value = True  # turn on LED to indicate we're writing to the file
        currenttime = str(time.monotonic() - starttime)
        f.write(currenttime+","+str(acceleration[0])+","+str(acceleration[1])+","+str(acceleration[2])+","+str(gyro[0])+","+str(gyro[1])+","+str(gyro[2])+"\n")
        led.value = False  # turn off LED to indicate we're done
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
