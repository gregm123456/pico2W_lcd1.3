#include "DEV_Config.h"
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"

void DEV_Module_Init(void) {
    // Initialize pins used by display
    gpio_init(LCD_BL_PIN);
    gpio_set_dir(LCD_BL_PIN, GPIO_OUT);

    gpio_init(LCD_RESET_PIN);
    gpio_set_dir(LCD_RESET_PIN, GPIO_OUT);

    gpio_init(LCD_DC_PIN);
    gpio_set_dir(LCD_DC_PIN, GPIO_OUT);

    gpio_init(LCD_CS_PIN);
    gpio_set_dir(LCD_CS_PIN, GPIO_OUT);

    // Configure SPI
    spi_init(spi0, 2000 * 1000); // 2 MHz for safe default
    gpio_set_function(LCD_SCLK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(LCD_MOSI_PIN, GPIO_FUNC_SPI);

    // Turn on backlight by default
    DEV_Digital_Write(LCD_BL_PIN, 1);
}

void DEV_Module_Exit(void) {
    DEV_Digital_Write(LCD_BL_PIN, 0);
}

void DEV_Digital_Write(uint32_t Pin, uint8_t Value) {
    gpio_put(Pin, Value);
}

uint8_t DEV_Digital_Read(uint32_t Pin) {
    return gpio_get(Pin);
}

void DEV_SPI_WriteByte(uint8_t Value) {
    uint8_t tx = Value;
    spi_write_blocking(spi0, &tx, 1);
}

uint16_t LCD_XINXX_Read_KEY(void) {
    uint16_t KEY_Value = 0;
    // Sample implementation for A/B only — extend as needed
    gpio_init(15);
    gpio_set_dir(15, GPIO_IN);
    gpio_pull_up(15);
    if (gpio_get(15) == 0) KEY_Value |= KEY_A;

    gpio_init(17);
    gpio_set_dir(17, GPIO_IN);
    gpio_pull_up(17);
    if (gpio_get(17) == 0) KEY_Value |= KEY_B;

    return KEY_Value;
}
