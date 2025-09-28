#ifndef DEV_CONFIG_H
#define DEV_CONFIG_H

#include <stdint.h>

#define UBYTE   uint8_t
#define UWORD   uint16_t
#define UDOUBLE uint32_t

// Pin definitions (Waveshare Pico-LCD-1.3 defaults)
#define LCD_BL_PIN     13
#define LCD_RESET_PIN  12
#define LCD_DC_PIN     8
#define LCD_CS_PIN     9
#define LCD_SCLK_PIN   10
#define LCD_MOSI_PIN   11

// Keys (bitmask)
#define KEY_A     0x0001
#define KEY_B     0x0002
#define KEY_X     0x0004
#define KEY_Y     0x0008
#define KEY_UP    0x0010
#define KEY_DOWN  0x0020
#define KEY_LEFT  0x0040
#define KEY_RIGHT 0x0080
#define KEY_CTRL  0x0100

void DEV_Module_Init(void);
void DEV_Module_Exit(void);
void DEV_Digital_Write(uint32_t Pin, uint8_t Value);
uint8_t DEV_Digital_Read(uint32_t Pin);
void DEV_SPI_WriteByte(uint8_t Value);

uint16_t LCD_XINXX_Read_KEY(void);

#endif // DEV_CONFIG_H
