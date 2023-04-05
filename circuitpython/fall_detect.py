# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import math
import busio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
import adafruit_bmp3xx
import pwmio

# To use LSM6DS33, comment out the LSM6DSOX import line
# and uncomment the next line
# from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS

# To use ISM330DHCX, comment out the LSM6DSOX import line
# and uncomment the next line
# from adafruit_lsm6ds.lsm330dhcx import ISM330DHCX as LSM6DS

# To use LSM6DS3TR-C, comment out the LSM6DSOX import line
# and uncomment the next line
# from adafruit_lsm6ds.lsm6ds3 import LSM6DS3 as LSM6DS

#from adafruit_lis3mdl import LIS3MDL

i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c = busio.I2C(board.SCL, board.SDA)
#accel_gyro = LSM6DS(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
#mag = LIS3MDL(i2c)

GRAVITY = 9.80665
direction = 0 # -1=down, 0=stationary, 1=up
flight_stage = 0 # 0=on pad, 1=ascending, 2=descending, 3=landed, 4=extending, 5=taking pics
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2
bmp.sea_level_pressure = 1013.25 # 1 atmosphere, millibars
ground_alt = bmp.altitude # meters
alt_queue = [ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt]
last_alt_avg = ground_alt
iterator = 0
mean_alt = ground_alt
last_mean_alt = mean_alt
buzzer = pwmio.PWMOut(board.D6, variable_frequency=True)
buzzer.frequency = 440
OFF = 0
ON = 2**15
tstamp = time.time()

while True:
    #acceleration = accel_gyro.acceleration
    #gyro = accel_gyro.gyro
    alt = bmp.altitude
    alt2 = alt - ground_alt
    #magnetic = mag.magnetic
    #print("Acceleration: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*acceleration))
    #print("Gyro          X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*gyro))
    #print("Magnetic      X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*magnetic))
    #print(acceleration[0]+GRAVITY)
    """ ALTITUDE USING ACCELEROMETER (OLD)
    if acceleration[0]+GRAVITY > 0.5: # ascending
        direction_queue[iterator] = 1
    elif acceleration[0]+GRAVITY < -0.5: # descending
        direction_queue[iterator] = -1
    #else:
    #    direction_queue[iterator] = 0
    mean = 0
    for i in range(len(direction_queue)):
        mean += direction_queue[i]
    last_dir = direction
    if mean > 0:
        direction = 1
    if mean < 0:
        direction = -1
    if last_dir != direction:
        print(direction_queue)
        if(direction == 1):
            print("Ascending!")
        else: 
            print("Descending!")
    if iterator < 9:
        iterator += 1
    else:
        iterator = 0
    """
    
    alt_queue[iterator] = alt;
        
    if iterator < 9:
        iterator += 1
    else:
        iterator = 0
        last_mean_alt = mean_alt
        mean_alt = 0
        for i in range(10):
            mean_alt += alt_queue[i]
        mean_alt = mean_alt/10
        if mean_alt - last_mean_alt > 1:
            direction = 1 # ascending
        elif mean_alt - last_mean_alt < -1:
            direction = -1 # descending
        else:
            direction = 0 # stationary
    
    print("")
    print(alt2) # difference from ground
    print(mean_alt-last_mean_alt) # difference from last time
    print(direction)
    print(alt_queue)
    buzzer.frequency = 262
    #if mean_alt-last_mean_alt > 3:
    if direction == 1:
        print("Ascending!")
        buzzer.duty_cycle = ON
        buzzer.frequency = 440
    #elif mean_alt-last_mean_alt < -3:
    elif direction == -1:
        print("Descending!")
        buzzer.duty_cycle = ON
        buzzer.frequency = 392
    
    if time.time()-tstamp > 3:
        buzzer.duty_cycle = ON
        tstamp = time.time()
    
    time.sleep(0.1)
        
    buzzer.duty_cycle = OFF
