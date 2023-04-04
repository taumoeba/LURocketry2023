import time
import board
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
import adafruit_bmp3xx
import digitalio
import pulseio
from adafruit_motor import stepper
from adafruit_motor import servo
from adafruit_motorkit import MotorKit

i2c = board.I2C()  # uses board.SCL and board.SDA
accel_gyro = LSM6DS(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

kit = MotorKit(i2c=board.I2C())
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
bigPWM = pulseio.PWMOut(board.D13, frequency=50)
bigServo = servo.ContinuousServo(bigPWM, min_pulse=750, max_pulse=2250)

GRAVITY = 9.80665
direction = 0 # -1=down, 0=stationary, 1=up
flight_stage = 0 # 0=on pad, 1=ascending, 2=descending, 3=landed, 4=extending, 5=taking pics
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2
bmp.sea_level_pressure = 1013.25 # 1 atmosphere, millibars
ground_alt = bmp.altitude # meters
alt_queue = [ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt, ground_alt]
last_alt_avg = ground_alt
iter = 0

while True:
    acceleration = accel_gyro.acceleration
    gyro = accel_gyro.gyro
    alt = bmp.altitude
    alt2 = alt - ground_alt
    
    alt_queue[iter] = alt;
    last_mean_alt = mean_alt
    mean_alt = 0
    for i in range(10):
        mean_alt += alt_queue[alt]
    mean_alt = mean_alt/10
    if mean_alt - last_mean_alt > 1:
        direction = 1 # ascending
    elif mean_alt - last_mean_alt < -1:
        direction = -1 # descending
    else:
        direction = 0 # stationary
        
    if iter < 9:
        iter += 1
    else:
        iter = 0
    
    if flight_stage==0: # on pad
        if direction==1 and mean_alt - last_mean_alt > 5:
            flight_stage = 1
        else:
            time.sleep(0.1)
    elif flight_stage==1: # ascending
        if direction==-1 and mean_alt - last_mean_alt < -5:
            flight_stage = 2
    elif flight_stage==2: # descending
        if direction==0:
            flight_stage = 3
    elif flight_stage==3: # landed
        time.sleep(10) # make sure everything has settled down
    elif flight_stage==4: # extending
        # extend payload using stepper
        curr = time.time()
        while time.time() - curr <= 5400: # 90 mins, check
            steps = kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.001)
    elif flight_stage==5: # taking pics
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
        
        # take pics
        

