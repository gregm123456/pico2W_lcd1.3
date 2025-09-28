<!--
Guidance for AI coding agents working in this workspace.
This workspace currently contains only supporting documents for the Waveshare "Pico LCD 1.3" demos (C/MicroPython/LVGL). There is no project code yet.
Update this file as the repository gains source code.
-->


# Quick context

- Purpose: hardware demos and examples for Waveshare Pico LCD 1.3 (ST7789VW) targeting Raspberry Pi Pico / Pico2 (RP2040 / RP2350). The repository contains MicroPython examples and a minimal C skeleton for developers working on macOS with VSCode.

# What you should know before editing or generating code

- C builds: C demos use the Raspberry Pi pico-sdk with CMake. Set `PICO_SDK_PATH` and use `cmake` / `make` to build a `.uf2` file which you flash by copying it to the Pico's UF2 mount or using the pico-vscode extension.

- MicroPython workflow: prefer MicroPython for fast iteration and demos. Use `mpremote` from the host to run scripts, manage files, or write a persistent `main.py` on the device.

# macOS (VSCode) — building and loading code onto a Pico 2W from this machine

This repository is developed on macOS with VSCode. When connected via USB, the Pico exposes a serial device node (e.g. `/dev/cu.usbmodemXXXX`). The documentation and examples below assume macOS/bash usage.

Minimum developer setup (Homebrew recommended):

```bash
# Install build tools (Homebrew required)
brew update
brew install cmake ninja git python3 arm-none-eabi-gcc
```

Get the pico-sdk and set the environment variable in your shell (add to `~/.bash_profile` / `~/.bashrc`):

```bash
git clone https://github.com/raspberrypi/pico-sdk.git ~/pico-sdk
echo 'export PICO_SDK_PATH=~/pico-sdk' >> ~/.bash_profile
source ~/.bash_profile
```

Build (C) for Pico 2W (RP2350):

```bash
mkdir -p c/build
cd c/build
export PICO_SDK_PATH=~/pico-sdk
cmake -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350 ..
make -j$(sysctl -n hw.ncpu)
```

Flashing / copying the resulting UF2 to the Pico 2W:

- Using VSCode + pico-vscode extension: configure the extension paths (CMake, Ninja, toolchain) and use the extension's "Flash"/"Run" action to deploy `main.uf2` directly to the board.
- Manual (Finder / Terminal): put the Pico into UF2 boot mode by holding BOOT while connecting the USB cable; the board mounts as a removable drive (check `/Volumes`). Copy `main.uf2` to that volume.

MicroPython on macOS:

- To use MicroPython on the Pico 2W, flash the appropriate MicroPython UF2 (see `supporting_documents/` for recommended images). After the board is running MicroPython, use `mpremote` to manage files and run code.

Development notes to include in code/docs for developers:

- Document which `PICO_BOARD` value to use (e.g. `pico2`) and where to set `PICO_SDK_PATH` in local environment and in VSCode settings.
- When adding C demos, include a short "How to build on macOS" snippet in the demo README showing the commands above and how to flash (`cp /Volumes/RPI-RP2/`).

# Which Python runtime should we use?

Short answer: prefer MicroPython for examples and demos in this repository.

Practical recommendation for this repo

- Default to MicroPython for Python-first demos and examples. Document the exact MicroPython UF2 used (filename and version) in each example's README.
- If you add C examples (LVGL, DMA, multicore), include a short note explaining how the heavy-lift C pieces integrate with the MicroPython interface (function names, expected arguments, and how to flash both parts).

# Project-specific patterns and conventions (from docs)

- Hardware abstraction: demos encapsulate low-level IO in `DEV_Config.c/.h` (functions to look for later):
  - `DEV_Module_Init()` / `DEV_Module_Exit()`
  - `DEV_Digital_Write(pin, value)` / `DEV_Digital_Read(pin)`
  - `DEV_SPI_WriteByte(value)`

- LVGL integration:
  - LVGL v8.* is expected under `lib/lvgl` in the upstream demos.
  - Display buffers use double-buffering: `lv_disp_draw_buf_init(&disp_buf, buf0, buf1, size)`.
  - The display flush callback uses DMA and must call `lv_disp_flush_ready(&disp_drv)` when DMA completes.
  - LVGL timing: `lv_tick_inc(ms)` is called from a repeating timer (e.g. 5ms) and `lv_timer_handler()`/`lv_task_handler()` is called in the main loop.

- Input handling: keys/joystick are read as bitmasks. Examples define KEY macros (e.g. `KEY_A = 0x0001`) in `lib/Config/DEV_Config.h` and read as a 16-bit mask.

# Where to look when you need examples

- `supporting_documents/Pico LCD 1.3 - Waveshare Wiki.html` — walkthrough of wiring, build commands, LVGL notes, and file locations used in Waveshare demos. Use it as the primary reference until actual source files are added.
- Upstream demo packages referenced in the docs (useful remote resources):
  - https://files.waveshare.com/wiki/common/Pico_code.7z
  - Waveshare LVGL demos (RP2040-LCD-LVGL.zip)

# Guidance for the AI agent when creating code or PRs

- Keep edits small and focused: when adding device-specific code, add an abstraction layer (`DEV_*` functions) rather than scattering direct GPIO/SPI calls.
- Default to the conventions described above: use `PICO_SDK_PATH` env var, honor `PICO_BOARD`/`PICO_PLATFORM`, integrate LVGL via draw buffers and proper flush/dma completion calls.
- When generating examples, include wiring comments (pin numbers from the docs) and a quick test script that draws a solid color or simple text.

# If you need to add tests or CI

- There are no tests in this workspace yet. If adding CI, prefer lightweight validation steps that do not require actual hardware, e.g.:
  - Static checks for C (clang-format, compile with `-DCOMPILE_TEST=ON` using pico-sdk mocks), or simple Python linting for MicroPython examples.

# Minimal PR checklist for contributors (to include in PR descriptions)

- Reference which target board was used (Pico vs Pico2). Set `PICO_BOARD` accordingly.
- Add/modify `DEV_Config.*` when changing hardware I/O; keep the interface stable.
- For LVGL changes, describe buffer sizes and refresh rate changes and where `lv_tick_inc` is called.

---
If you want, I can now: (A) commit this file to the repo (create `.github/copilot-instructions.md`) or (B) show you a short preview to tweak before committing. You previously asked me to create it — tell me if you'd like any additional examples or wording changed before I commit.
