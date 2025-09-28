"""
Minimal ST7789 driver for MicroPython on Raspberry Pi Pico
Based on common ST7789 implementations, simplified for basic color fills and text
SPDX-License-Identifier: MIT
Copyright (c) 2025 Greg Merritt <gregm123456>
"""

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
        """Basic text rendering (placeholder - draws a small rectangle per character)"""
        # This is a very basic implementation - just draws small rectangles
        # Real text would need a font bitmap
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