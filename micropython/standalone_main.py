"""
Complete MicroPython example for Waveshare Pico LCD 1.3 (ST7789) on Pico 2W.
Self-contained with embedded ST7789 driver - no external imports needed.
"""

from machine import Pin, SPI
import time
from micropython import const

# ST7789 Commands
_SWRESET = const(0x01)
_SLPOUT = const(0x11)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_DISPON = const(0x29)

class ST7789:
    def __init__(self, spi, width, height, reset=None, cs=None, dc=None, rotation=0):
        self.spi = spi
        self.width = width
        self.height = height
        self.reset = reset
        self.cs = cs
        self.dc = dc
        self.rotation = rotation
        
    def init(self):
        """Initialize the display"""
        if self.reset:
            self.reset.value(0)
            time.sleep_ms(50)
            self.reset.value(1)
            time.sleep_ms(50)
            
        # Wake up display
        self._write_cmd(_SWRESET)
        time.sleep_ms(150)
        
        self._write_cmd(_SLPOUT)
        time.sleep_ms(10)
        
        # Set color mode to 16-bit
        self._write_cmd(_COLMOD)
        self._write_data(bytearray([0x05]))
        
        # Set memory access control (rotation)
        self._write_cmd(_MADCTL)
        self._write_data(bytearray([0x00]))
        
        # Display on
        self._write_cmd(_DISPON)
        time.sleep_ms(10)
        
    def _write_cmd(self, cmd):
        """Send command to display"""
        if self.cs:
            self.cs.value(0)
        if self.dc:
            self.dc.value(0)  # Command mode
        self.spi.write(bytearray([cmd]))
        if self.cs:
            self.cs.value(1)
            
    def _write_data(self, data):
        """Send data to display"""
        if self.cs:
            self.cs.value(0)
        if self.dc:
            self.dc.value(1)  # Data mode
        self.spi.write(data)
        if self.cs:
            self.cs.value(1)
            
    def _set_window(self, x0, y0, x1, y1):
        """Set the drawing window"""
        self._write_cmd(_CASET)  # Column address set
        self._write_data(bytearray([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        
        self._write_cmd(_RASET)  # Row address set
        self._write_data(bytearray([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        
        self._write_cmd(_RAMWR)  # Write to RAM
        
    def fill(self, color):
        """Fill entire screen with color (16-bit RGB565)"""
        self._set_window(0, 0, self.width - 1, self.height - 1)
        
        # Convert color to bytes
        color_hi = (color >> 8) & 0xFF
        color_lo = color & 0xFF
        
        # Create buffer for efficient writing
        line_buf = bytearray([color_hi, color_lo] * self.width)
        
        if self.cs:
            self.cs.value(0)
        if self.dc:
            self.dc.value(1)  # Data mode
            
        # Write all pixels
        for _ in range(self.height):
            self.spi.write(line_buf)
            
        if self.cs:
            self.cs.value(1)
            
    def text(self, string, x, y, color):
        """Basic text rendering (draws small rectangles for characters)"""
        char_width = 8
        char_height = 8
        
        for i, char in enumerate(string):
            char_x = x + i * char_width
            if char_x + char_width > self.width:
                break
                
            # Draw a small rectangle for each character
            self._set_window(char_x, y, char_x + char_width - 1, y + char_height - 1)
            
            color_hi = (color >> 8) & 0xFF
            color_lo = color & 0xFF
            char_buf = bytearray([color_hi, color_lo] * char_width)
            
            if self.cs:
                self.cs.value(0)
            if self.dc:
                self.dc.value(1)
                
            for _ in range(char_height):
                self.spi.write(char_buf)
                
            if self.cs:
                self.cs.value(1)

# --- Pin mapping (Waveshare defaults when module is seated on header) ---
LCD_SCLK = 10   # GP10
LCD_MOSI = 11   # GP11
LCD_CS   = 9    # GP9
LCD_DC   = 8    # GP8
LCD_RESET= 12   # GP12
LCD_BL   = 13   # GP13

KEY_A_PIN = 15  # GP15
KEY_B_PIN = 17  # GP17

# Helper: initialize SPI + display driver
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

    disp = ST7789(spi, 240, 240, reset=rst, cs=cs, dc=dc, rotation=0)
    disp.init()
    return disp

# Simple pattern draw
def draw_test(disp, color_index=0):
    colors = [0xF800, 0x07E0, 0x001F, 0xFFE0, 0xF81F, 0x07FF]  # Red, Green, Blue, Yellow, Magenta, Cyan
    color_names = ["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan"]
    
    if disp is None:
        print(f"Would draw color {colors[color_index % len(colors)]:04x} ({color_names[color_index % len(colors)]})")
        return
        
    c = colors[color_index % len(colors)]
    print(f"Drawing {color_names[color_index % len(colors)]} (0x{c:04x})")
    
    # Fill screen with color
    disp.fill(c)
    
    # Add some text in contrasting color
    text_color = 0xFFFF if c < 0x8000 else 0x0000  # White on dark, black on light
    try:
        disp.text("Pico2W", 10, 10, text_color)
        disp.text("LCD 1.3", 10, 30, text_color)
        disp.text("Press A/B", 10, 50, text_color)
    except Exception as e:
        print(f"Text drawing failed: {e}")

# Button setup (active-low expected on Waveshare button wiring)
key_a = Pin(KEY_A_PIN, Pin.IN, Pin.PULL_UP)
key_b = Pin(KEY_B_PIN, Pin.IN, Pin.PULL_UP)

# Main execution
print("Initializing display...")
try:
    disp = init_display()
    print("Display initialized successfully!")
except Exception as e:
    print(f"Display initialization failed: {e}")
    disp = None

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
            disp.fill(0x0000)  # Clear to black
        except Exception:
            pass
    # turn off backlight
    try:
        Pin(LCD_BL, Pin.OUT).value(0)
    except Exception:
        pass