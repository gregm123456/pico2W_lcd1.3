"""
Script to copy the standalone_main.py content to main.py on the device
using mpremote exec commands
"""

import sys
import os

# Read the standalone_main.py content
with open('micropython/standalone_main.py', 'r') as f:
    content = f.read()

# Escape the content for Python string literal
escaped_content = repr(content)

# Create the command to write the file on the device
write_command = f'''
with open('main.py', 'w') as f:
    f.write({escaped_content})
print("File main.py created successfully")
'''

print("Execute this command:")
print(f"mpremote connect /dev/cu.usbmodem1301 exec \"{write_command.strip()}\"")