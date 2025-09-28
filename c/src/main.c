#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "lib/Config/DEV_Config.h"

int main() {
    stdio_init_all();
    DEV_Module_Init();

    // Simple test: toggle backlight and reset
    DEV_Digital_Write(LCD_BL_PIN, 1);
    sleep_ms(500);
    DEV_Digital_Write(LCD_BL_PIN, 0);
    sleep_ms(500);
    DEV_Digital_Write(LCD_BL_PIN, 1);

    // Main loop: print button state
    while (true) {
        uint16_t keys = LCD_XINXX_Read_KEY();
        printf("KEYS: 0x%04x\n", keys);
        sleep_ms(500);
    }

    DEV_Module_Exit();
    return 0;
}
