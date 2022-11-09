#include <stdio.h>
#include "stdlib.h"
#include "hardware/i2c.h"

/// @brief Write data to a register of a I2C device
/// @param i2c i2c instance to use
/// @param addr i2c address of device
/// @param reg address of register
/// @param buf pointer to data to send
/// @param nbytes number of bytes to send
/// @return Returns: Number of bytes written, or PICO_ERROR_GENERIC if address not acknowledged, no device present.
int reg_write(i2c_inst_t *i2c,
                const uint addr,
                const uint8_t reg,
                uint8_t *buf,
                const uint8_t nbytes)
{
    int num_bytes_read = 0;
    uint8_t msg[nbytes+1];

    // Ensure caller is sending at least 1 byte
    if(nbytes<1) return 0;

    // Append register address to front of data packet
    msg[0] = reg;
    for(int i=0; i<nbytes; i++) msg[i+1] = buf[i];

    // Write data to register(s) over i2c
    i2c_write_blocking(i2c, addr, msg, (nbytes+1), false);

    return num_bytes_read;
}

/// @brief Read data from register of I2C device
/// @param i2c i2c instance to use
/// @param addr i2c address of device
/// @param reg address of register to read from
/// @param buf pointer to buffer to store data
/// @param nbytes number of bytes to be read
/// @return Returns: Number of bytes written, or PICO_ERROR_GENERIC if address not acknowledged, no device present.
int reg_read(i2c_inst_t *i2c,
                const uint addr,
                const uint8_t reg,
                uint8_t *buf,
                const uint8_t nbytes)
{
    int num_bytes_read = 0;

    // Ensure caller is asking for at least 1 byte
    if(nbytes<1) return 0;

    // Read data from registers over i2c
    i2c_write_blocking(i2c, addr, &reg, 1, true);
    num_bytes_read = i2c_read_blocking(i2c, addr, buf, nbytes, false);

    return num_bytes_read;
}

/* Usage Example
int16_t acc_x;
    int16_t acc_y;
    int16_t acc_z;
    float acc_x_f;
    float acc_y_f;
    float acc_z_f;

    // Pins
    const uint sda_pin = 16;
    const uint scl_pin = 17;

    // Ports
    i2c_inst_t *i2c = i2c0;

    // Buffer to store raw reads
    uint8_t data[6];

    // Initialize chosen serial port
    stdio_init_all();

    //Initialize I2C port at 400 kHz
    i2c_init(i2c, 400 * 1000);

    // Initialize I2C pins
    gpio_set_function(sda_pin, GPIO_FUNC_I2C);
    gpio_set_function(scl_pin, GPIO_FUNC_I2C);

    // Read device ID to make sure that we can communicate with the ADXL343
    reg_read(i2c, ADXL343_ADDR, REG_DEVID, data, 1);
    if (data[0] != DEVID) {
        printf("ERROR: Could not communicate with ADXL343\r\n");
        while (true);
    }

    // Read Power Control register
    reg_read(i2c, ADXL343_ADDR, REG_POWER_CTL, data, 1);
    printf("0xX\r\n", data[0]);

    // Tell ADXL343 to start taking measurements by setting Measure bit to high
    data[0] |= (1 << 3);
    reg_write(i2c, ADXL343_ADDR, REG_POWER_CTL, &data[0], 1);

    // Test: read Power Control register back to make sure Measure bit was set
    reg_read(i2c, ADXL343_ADDR, REG_POWER_CTL, data, 1);
    printf("0xX\r\n", data[0]);

    // Wait before taking measurements
    sleep_ms(2000);

    // Loop forever
    while (true) {

        // Read X, Y, and Z values from registers (16 bits each)
        reg_read(i2c, ADXL343_ADDR, REG_DATAX0, data, 6);

        // Convert 2 bytes (little-endian) into 16-bit integer (signed)
        acc_x = (int16_t)((data[1] << 8) | data[0]);
        acc_y = (int16_t)((data[3] << 8) | data[2]);
        acc_z = (int16_t)((data[5] << 8) | data[4]);

        // Convert measurements to [m/s^2]
        acc_x_f = acc_x * SENSITIVITY_2G * EARTH_GRAVITY;
        acc_y_f = acc_y * SENSITIVITY_2G * EARTH_GRAVITY;
        acc_z_f = acc_z * SENSITIVITY_2G * EARTH_GRAVITY;

        // Print results
        printf("X: %.2f | Y: %.2f | Z: %.2f\r\n", acc_x_f, acc_y_f, acc_z_f);

        sleep_ms(100);
    }

*/