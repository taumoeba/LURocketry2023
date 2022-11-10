import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
import adafruit_sdcard
import busio
import digitalio
import microcontroller
import storage

# Use any pin that is not taken by SPI
SD_CS = board.D25

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

i2c = board.I2C()  # uses board.SCL and board.SDA
accel_gyro = LSM6DS(i2c)

starttime = time.monotonic()

print("This is where the fun begins\n")

while True:
    acceleration = accel_gyro.acceleration
    gyro = accel_gyro.gyro

    with open("/sd/imu_data.txt", "a") as f:
        led.value = True  # turn on LED to indicate we're writing to the file
        currenttime = str(time.monotonic() - starttime)
        f.write(currenttime+","+str(acceleration[0])+","+str(acceleration[1])+","+str(acceleration[2])+","+str(gyro[0])+","+str(gyro[1])+","+str(gyro[2])+"\n")
        led.value = False  # turn off LED to indicate we're done

    time.sleep(1)
