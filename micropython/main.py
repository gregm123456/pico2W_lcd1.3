"""
SPDX-License-Identifier: MIT
Copyright (c) 2025 Greg Merritt <gregm123456>

Minimal MicroPython example for Waveshare Pico LCD 1.3 (ST7789) on Pico 2W.
- Draws a simple color bar and text.
- Reads two buttons (KEY_A, KEY_B) and toggles the screen color when pressed.

This script is written to be mpremote-friendly. From macOS in a venv with mpremote installed:

# Copy file to the board
mpremote connect serial://auto fs put micropython/main.py :/main.py
# Or run it directly
mpremote connect serial://auto run :/main.py

Adjust pins if your wiring differs. This example assumes the Waveshare module is seated directly on the Pico header using the Waveshare default pin mapping.
"""

from machine import Pin, SPI
import time

# --- Pin mapping (Waveshare defaults when module is seated on header) ---
LCD_SCLK = 10   # GP10
LCD_MOSI = 11   # GP11
LCD_CS   = 9    # GP9
LCD_DC   = 8    # GP8
LCD_RESET= 12   # GP12
LCD_BL   = 13   # GP13

KEY_A_PIN = 15  # GP15
KEY_B_PIN = 17  # GP17

# Import the local st7789 driver
try:
    from st7789 import ST7789
    st7789_available = True
except ImportError:
    try:
        import st7789
        st7789_available = True
    except ImportError:
        st7789_available = False
        print("st7789 driver not found — skipping display init")

# Helper: initialize SPI + display driver if available
def init_display():
    # Use SPI1 with explicit pin assignments for Waveshare LCD 1.3
    spi = SPI(1, baudrate=40000000, sck=Pin(LCD_SCLK), mosi=Pin(LCD_MOSI))
    dc = Pin(LCD_DC, Pin.OUT)
    cs = Pin(LCD_CS, Pin.OUT)
    rst = Pin(LCD_RESET, Pin.OUT)
    bl = Pin(LCD_BL, Pin.OUT)

    # Reset sequence
    rst.value(0)
    time.sleep_ms(50)
    rst.value(1)
    time.sleep_ms(50)

    # Turn on backlight
    bl.value(1)

    if not st7789_available:
        return None

    disp = ST7789(spi, 240, 240, reset=rst, cs=cs, dc=dc, rotation=0)
    disp.init()
    return disp

# Simple pattern draw
def draw_test(disp, color_index=0):
    colors = [0xF800, 0x07E0, 0x001F, 0xFFE0, 0xF81F, 0x07FF]
    if disp is None:
        print(f"Would draw color {colors[color_index % len(colors)]:04x}")
        return
    w = 240
    h = 240
    c = colors[color_index % len(colors)]
    # fill screen with color
    disp.fill(c)
    # write some text in inverse color
    inv = 0xFFFF ^ c & 0xFFFF
    try:
        disp.text("Pico 2W", 10, 10, inv)
        disp.text("ST7789 demo", 10, 30, inv)
    except Exception:
        pass

# Button setup (active-low expected on Waveshare button wiring)
key_a = Pin(KEY_A_PIN, Pin.IN, Pin.PULL_UP)
key_b = Pin(KEY_B_PIN, Pin.IN, Pin.PULL_UP)

# Main

disp = init_display()
color_idx = 0
last_a = key_a.value()
last_b = key_b.value()

draw_test(disp, color_idx)

print("Starting main loop. Press buttons to change color. Ctrl-C to stop.")
try:
    while True:
        a = key_a.value()
        b = key_b.value()
        # falling edge detection (pressed)
        if last_a == 1 and a == 0:
            color_idx += 1
            draw_test(disp, color_idx)
            print("KEY_A pressed")
        if last_b == 1 and b == 0:
            color_idx -= 1
            draw_test(disp, color_idx)
            print("KEY_B pressed")
        last_a = a
        last_b = b
        time.sleep_ms(50)
except KeyboardInterrupt:
    print("Stopped by user")
    if disp:
        try:
            disp.fill(0x0000)
        except Exception:
            pass
    # turn off backlight
    try:
        Pin(LCD_BL, Pin.OUT).value(0)
    except Exception:
        pass
