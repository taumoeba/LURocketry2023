# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "/home/super/pico/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(i2cTest C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(i2cTest i2cTest.c )

pico_set_program_name(i2cTest "i2cTest")
pico_set_program_version(i2cTest "0.1")

pico_enable_stdio_uart(i2cTest 1)
pico_enable_stdio_usb(i2cTest 1)

# Add the standard library to the build
target_link_libraries(i2cTest pico_stdlib)

# Add any user requested libraries
target_link_libraries(i2cTest
        hardware_i2c
        )

pico_add_extra_outputs(i2cTest)



