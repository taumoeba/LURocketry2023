# LURocketry2023

Home to all the code written by the Lipscomb University Rocket Team for the 2023 NASA University Student Launch Initiative.

Payload microcontroller board: Adafruit Feather RP2040

Microcontroller for GPS/Radio boards: Adafruit Feather M0 Express

Required libraries for GPS/Radio boards:

- RadioHead http://www.airspayce.com/mikem/arduino/RadioHead/
(Note: Either delete RH_LoRaFileOps.cpp and RH_LoRaFileOps.h or just ignore the compilation warning this library gives you.)
- TinyGPS++ https://github.com/mikalhart/TinyGPSPlus
