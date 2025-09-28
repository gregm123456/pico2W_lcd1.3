cmake_minimum_required(VERSION 3.13)

set(PICO_BOARD pico2 CACHE STRING "Board type")
set(PICO_SDK_PATH $ENV{PICO_SDK_PATH} CACHE STRING "PICO_SDK_PATH")

project(pico_lcd_demo C CXX ASM)

# Try to include the SDK import/init file from a couple of known names/locations.
# Some pico-sdk versions provide pico_sdk_import.cmake, others provide
# pico_sdk_init.cmake at the SDK root. Prefer an explicit include from
# PICO_SDK_PATH when available, otherwise fall back to CMake's include search.
if(PICO_SDK_PATH AND EXISTS "${PICO_SDK_PATH}/pico_sdk_import.cmake")
    include("${PICO_SDK_PATH}/pico_sdk_import.cmake")
elseif(PICO_SDK_PATH AND EXISTS "${PICO_SDK_PATH}/pico_sdk_init.cmake")
    include("${PICO_SDK_PATH}/pico_sdk_init.cmake")
else()
    include(pico_sdk_import.cmake)
endif()

pico_sdk_init()

add_executable(pico_lcd_demo
    src/main.c
    lib/Config/DEV_Config.c
)

target_link_libraries(pico_lcd_demo pico_stdlib hardware_spi)

pico_add_extra_outputs(pico_lcd_demo)
