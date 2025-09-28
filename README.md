Pico 2W + LCD 1.3 — Developer README

This repository contains examples and documentation for using a Waveshare LCD 1.3 (ST7789VW) with a Raspberry Pi Pico / Pico2 (RP2040 / RP2350). The documentation below describes the recommended macOS + VSCode developer workflow, how to build and flash C firmware, and how to manage MicroPython examples using mpremote.

Overview
- Recommended workflows
    - MicroPython-first development (fast iteration): edit locally in VSCode, use `mpremote` from a macOS terminal to run or install scripts, and keep a self-contained `main.py` on the device for persistent demos.
    - C demos (pico-sdk + CMake): use the pico-sdk when you need native performance (LVGL DMA flushes, PIO, multicore C).</n+
Prerequisites (macOS)
- Install base developer tools with Homebrew:

```bash
brew update
brew install cmake ninja git python3 arm-none-eabi-gcc
```

- Clone the pico-sdk and set `PICO_SDK_PATH` in your shell rc (example for bash):

```bash
git clone https://github.com/raspberrypi/pico-sdk.git ~/pico-sdk
echo 'export PICO_SDK_PATH=~/pico-sdk' >> ~/.bash_profile
source ~/.bash_profile
```

MicroPython (recommended for examples)
- The repository provides MicroPython examples under `micropython/` including `standalone_main.py`, a self-contained demo that initializes the ST7789 display and responds to two buttons. The self-contained script is the recommended starting point because it runs without needing extra files on the device.
- To install or update the MicroPython firmware (UF2), put the Pico into UF2 boot mode (hold BOOT while connecting) and copy the UF2 file to the mounted volume (e.g. `/Volumes/RPI-RP2`). `mpremote` talks to the running MicroPython runtime and does not install UF2 images.

VSCode-first MicroPython workflow
- Use a Python virtual environment and install developer tools:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install mpremote pyserial
```

- Recommended VSCode extensions
    - Python (ms-python.python)
    - C/C++ (ms-vscode.cpptools) — if adding C demos
    - CMake Tools (ms-vscode.cmake-tools)
    - pico-vscode (raspberry-pi.pico-vscode) — for C/C++ build integration and flashing UF2

Core mpremote examples (use the explicit device path on macOS)
- Identify your device node (example):

```bash
ls /dev/cu.* | grep usb
# example result: /dev/cu.usbmodem1301
```

- Start a REPL on the detected device:

```bash
mpremote connect /dev/cu.usbmodem1301 repl
```

- Run a local script directly from the host (does not persist on the device):

```bash
mpremote connect /dev/cu.usbmodem1301 run micropython/standalone_main.py
```

- Install the self-contained demo as `main.py` on the device (persists and auto-runs on power-up):

```bash
# Recommended robust method: use mpremote exec to write the file on the board
python3 - <<'PY'
from pathlib import Path
import subprocess
content = Path('micropython/standalone_main.py').read_text()
exec_cmd = (
        "with open('main.py','w') as f: f.write({!r}); print('main.py installed')".format(content)
)
subprocess.run(['mpremote', 'connect', '/dev/cu.usbmodem1301', 'exec', exec_cmd], check=True)
PY
```

After this, `main.py` will run automatically when the Pico is powered (for example, from a USB battery).

Files and examples
- `micropython/standalone_main.py` — self-contained demo (recommended for quick starts and persistent demos).
- `micropython/main.py` and `micropython/st7789.py` — modular example + driver (useful for development where you want separate driver and app files).
- `c/` — C demos and CMake build files (use pico-sdk when you need low-level performance).

Wiring / Pins (Waveshare defaults)
- VCC -> VSYS
- GND -> GND
- DIN (MOSI) -> GP11
- CLK (SCK) -> GP10
- CS -> GP9
- DC -> GP8
- RST -> GP12
- BL -> GP13
- Buttons: typical examples use GP15 (KEY_A) and GP17 (KEY_B)

C build / flash (quick)
- Build C demos (example for Pico 2W / RP2350):

```bash
mkdir -p c/build
cd c/build
export PICO_SDK_PATH=~/pico-sdk
cmake -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350 ..
make -j$(sysctl -n hw.ncpu)
```

- Flash the resulting UF2 by putting the Pico into UF2 boot mode (hold BOOT while connecting) and copying `main.uf2` to the mounted volume:

```bash
cp main.uf2 /Volumes/RPI-RP2/
```

Developer guidance and conventions
- Prefer self-contained `main.py` demos for persistence and for devices that will be powered without the host attached.
- For multi-file development, keep drivers (e.g., `st7789.py`) and application code separate under `micropython/` to make iteration easier.
- When adding hardware-specific C code, centralize board I/O in `DEV_Config.c/.h` to keep examples portable.

Where to look for reference
- `supporting_documents/Pico LCD 1.3 - Waveshare Wiki.html` — wiring diagrams, LVGL notes, and example downloads.

Contact / contributions
- When contributing, document which board variant you used (Pico vs Pico2) and any changes to the pin mapping. Include short build and flash instructions in PR descriptions.
