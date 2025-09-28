Pico 2W + LCD 1.3 — Developer README

This repository currently holds supporting documents and demos for the Waveshare Pico LCD 1.3 (ST7789VW) driving a Raspberry Pi Pico / Pico2 (RP2040 / RP2350).

Goal
- Provide clear, macOS + VSCode instructions so developers can build, flash and manage firmware for a Pico 2W that is assembled inside a case with the Waveshare LCD 1.3 mounted and external buttons connected. Examples and tests should target the LCD and its buttons (not the Pico 2W on-board LEDs which may be inaccessible in the case).

Quick macOS setup (Homebrew)

```bash
# Install base tools
brew update
brew install cmake ninja git python3 arm-none-eabi-gcc
```

Get the pico-sdk and set PICO_SDK_PATH (add to your shell rc):

```bash
git clone https://github.com/raspberrypi/pico-sdk.git ~/pico-sdk
echo 'export PICO_SDK_PATH=~/pico-sdk' >> ~/.bash_profile
source ~/.bash_profile
```

Build (C) for Pico 2W (RP2350) — project layout assumed as Waveshare demos

```bash
mkdir -p c/build
cd c/build
export PICO_SDK_PATH=~/pico-sdk
cmake -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350 ..
make -j$(sysctl -n hw.ncpu)
```

Flashing the UF2 to the Pico 2W

- VSCode: install `pico-vscode` extension, configure paths (CMake, Ninja, toolchain) and use "Flash"/"Run" in the extension.
- Manual (Finder or Terminal): hold BOOT while connecting the Pico, it will mount as a removable drive. Copy `main.uf2` into the mounted volume (name may be `RPI-RP2` or similar):

```bash
ls /Volumes
cp main.uf2 /Volumes/RPI-RP2/
```

MicroPython notes
- Prefer MicroPython for Python-first demos (best CPython-like experience). Use Thonny for deployment and interactive REPL.
- Flash the proper MicroPython UF2 for Pico2 (see `supporting_documents/` for Waveshare recommended firmware images).

VSCode-first MicroPython workflow (no Thonny required)

You can manage MicroPython development entirely from VSCode. The recommended approach is to create a local virtual environment, install `mpremote` (the MicroPython remote tool) and related tools, and use the VSCode terminal + extensions for editing and REPL access.

1) Create and activate a venv (bash/zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2) Install developer tools in the venv:

```bash
pip install mpremote pyserial
# optional helpers: adafruit-ampy, rshell
pip install adafruit-ampy
```

3) Recommended VSCode extensions

- Python (ms-python.python)
- C/C++ (ms-vscode.cpptools) — if you will add C demos
- CMake Tools (ms-vscode.cmake-tools)
- pico-vscode (raspberry-pi.pico-vscode) — for C/C++ build integration and flashing UF2
- Optional: Pymakr or PlatformIO serial monitor if you prefer their UI for serial

4) Common `mpremote` commands (replace the device path with your board's):

```bash
# Start a REPL on the Pico (auto-detect usually works)
mpremote repl

# Run a single script directly
mpremote run main.py

# Push a local directory to the board (sync - deletes remote files not present locally)
mpremote fs sync . /

# Copy a single file
mpremote cp main.py :/main.py

# Use the raw repl for interactive debugging
mpremote rawterm
```

Notes about firmware flashing (MicroPython UF2)
- To install or update the MicroPython firmware (the UF2), you still need to put the Pico in UF2 boot mode and copy the UF2 to the mounted volume (manual copy in Finder or `cp` in terminal). This is a one-time operation per firmware change — `mpremote` talks to the running MicroPython runtime and does not install UF2 images.

When to still use Thonny
- Thonny is convenient for quickly flashing UF2 and using an integrated file browser/REPL for beginners. If you prefer VSCode and `mpremote`, Thonny is not required.

Notes on C builds and dual workflows
- If you need native performance (LVGL DMA flushes, PIO, multicore C workers), you'll use the pico-sdk + CMake toolchain and build from VSCode (pico-vscode or CMake Tools). The build/flash path for C projects still uses UF2 copying or the pico-vscode flashing action.


Wiring / Pins (Waveshare demo defaults — reference only)
- VCC -> VSYS
- GND -> GND
- DIN (MOSI) -> GP11
- CLK (SCK) -> GP10
- CS -> GP9
- DC -> GP8
- RST -> GP12
- BL -> GP13
- Buttons / joystick: GP15/17/19/21, GP2/GP18/GP16/GP20/GP3 (varies per module)

Developer guidance
- Examples should use the LCD and buttons for user-visible testing. Document the exact pin mapping used in each example's README.
- When adding low-level changes, prefer adding/modifying `DEV_Config.c/.h` to keep hardware I/O abstracted.
- For LVGL/UIs: follow LVGL double-buffering and DMA flush patterns (see Waveshare docs in `supporting_documents/`).

Files of interest (in Waveshare demos)
- `c/` — C demos and CMake build
- `examples/src/`, `examples/inc/` — LVGL and other example apps
- `lib/Config/DEV_Config.c(.h)` — hardware abstraction layer
- `lib/lvgl/` — LVGL sources (v8.x expected in demos)

Next steps
- I can create a minimal C skeleton and a matching MicroPython example that draws to the LCD and reads the buttons (they will use the pin mapping above). You said you'd like the README first — when you confirm this looks good I'll add the examples.

Issues / caveats
- Pico2 firmware compatibility can be picky — prefer Waveshare-provided UF2 builds for MicroPython when running their examples.
- If the Pico is mounted inside a 3D printed case and the Pico's onboard LEDs are inaccessible, ensure examples target the LCD and external buttons only.

Contact / more info
- See `supporting_documents/Pico LCD 1.3 - Waveshare Wiki.html` for full wiring diagrams, LVGL notes, and example download links.
