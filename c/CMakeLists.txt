cmake_minimum_required(VERSION 3.13)

set(PICO_BOARD pico2 CACHE STRING "Board type")
set(PICO_SDK_PATH $ENV{PICO_SDK_PATH} CACHE STRING "PICO_SDK_PATH")

project(pico_lcd_demo)

include(pico_sdk_import.cmake)

pico_sdk_init()

add_executable(pico_lcd_demo
    src/main.c
    lib/Config/DEV_Config.c
)

target_link_libraries(pico_lcd_demo pico_stdlib hardware_spi)

pico_add_extra_outputs(pico_lcd_demo)
