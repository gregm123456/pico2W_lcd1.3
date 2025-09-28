<!--
Guidance for AI coding agents working in this workspace.
This workspace currently contains only supporting documents for the Waveshare "Pico LCD 1.3" demos (C/MicroPython/LVGL). There is no project code yet.
Update this file as the repository gains source code.
-->

# Quick context

- Purpose: hardware demos and examples for Waveshare Pico LCD 1.3 (ST7789VW) targeting Raspberry Pi Pico / Pico2 (RP2040 / RP2350). The supporting docs describe C demos (pico-sdk + cmake), MicroPython examples, and LVGL-based GUI examples.
- Current layout (docs only): `supporting_documents/` contains Waveshare HTML/PDF guides. No `c/`, `examples/` or `lib/` source folders are present yet in this repo.

# What you should know before editing or generating code

- Builds: C demos use the Raspberry Pi pico-sdk with CMake. Typical workflow (from Waveshare docs): set `PICO_SDK_PATH`, run cmake with `-DPICO_BOARD` / `-DPICO_PLATFORM`, then `make -jN`. The resulting firmware is a `.uf2` file and is copied to the Pico mount (e.g. `/media/pi/RPI-RP2/`).

- Key build commands (copyable):

```bash
cd c/build
export PICO_SDK_PATH=/absolute/path/to/pico-sdk
# For Pico (RP2040)
cmake -DPICO_BOARD=pico -DPICO_PLATFORM=rp2040 ..
# For Pico2 (RP2350)
cmake -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350 ..
make -j9
cp main.uf2 /media/pi/RPI-RP2/    # or the appropriate removable mount
```

- MicroPython workflow: flash the appropriate `.uf2` firmware to the device (hold BOOT button while connecting), then use Thonny to run `Pico-LCD-1.3.py` examples. Thonny on Pi may need upgrade via `sudo apt upgrade thonny`.

- VSCode Pico: the docs recommend the `pico-vscode` extension and configuring `PICO_SDK_PATH`, CMake/Ninja paths, and the toolchain. CMake cache variable `set(PICO_BOARD pico CACHE STRING "Board type")` is used in some demos to switch boards.

# macOS (VSCode) — building and loading code onto a Pico 2W from this machine

This repository is developed on a Mac with VSCode. If you have the Pico 2W connected via USB to your Mac, include explicit instructions in code and docs that explain how to build, flash, and manage code from this environment.

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

Build (C) for Pico 2W (RP2350) from the repo structure used by Waveshare demos:

```bash
mkdir -p c/build
cd c/build
export PICO_SDK_PATH=~/pico-sdk   # ensure this points to your cloned SDK
cmake -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350 ..
make -j$(sysctl -n hw.ncpu)
```

Flashing / copying the resulting UF2 to the Pico 2W:

- Using VSCode + pico-vscode extension: configure the extension paths (CMake, Ninja, toolchain) and use the extension's "Flash"/"Run" action to deploy `main.uf2` directly to the board. Make sure `PICO_SDK_PATH` is configured in the extension settings or your environment.
- Manual (Finder / Terminal): put the Pico into UF2 boot mode: hold the BOOT button while connecting the USB cable, then release. The board mounts as a removable drive (check `/Volumes`). Copy `main.uf2` to that volume. Example (adjust the volume name if it differs):

```bash
# Check mounted volumes to find the Pico drive name
ls /Volumes
# Copy UF2 to the mounted Pico volume (usually RPI-RP2)
cp main.uf2 /Volumes/RPI-RP2/
```

Notes and troubleshooting for macOS:
- The mounted name can vary; if you don't see `RPI-RP2` check `ls /Volumes` or use Finder. For Pico2 the volume name may differ; confirm it before copying.
- If the drive doesn't appear, try holding BOOT longer or reconnecting the USB cable. Verify the cable supports data (some charging cables do not).
- You can also use the pico-vscode extension to flash without manually copying files.

MicroPython on Mac:
- To use MicroPython on the Pico 2W, download the appropriate MicroPython UF2 (Waveshare links are in `supporting_documents`) and copy it to the mounted drive as above. Use Thonny for interactive editing and deployment.
- Note from Waveshare docs: Pico2 firmware compatibility can be picky; prefer the firmware images linked in the supporting docs.

Development notes to include in code/docs for developers:
- Always document which `PICO_BOARD` value to use (e.g. `pico2`) and where to set `PICO_SDK_PATH` in local environment and in VSCode settings.
- When adding C demos, include a short "How to build on macOS" snippet in the demo README showing the commands above and how to flash (`cp /Volumes/RPI-RP2/`).
- For MicroPython examples, include the exact UF2 firmware the example was tested with and the Thonny / port setup steps.

# Which Python runtime should we use?

Short answer: for the "most full-featured Python" experience on a Pico 2W, prefer MicroPython.

Why MicroPython?
- Closest to CPython semantics for embedded use while offering low-level hardware access (machine, rp2/PIO, etc.).
- Native module support: you can write performance- or hardware-critical code in C/C++ and expose it as a MicroPython module.
- Broad community support for RP2-series boards and many examples/demos use MicroPython (the Waveshare docs reference MicroPython examples).
- More flexible for integrating with the C pico-sdk (if you need very high performance or advanced peripherals like DMA + LVGL flush paths).

When to consider CircuitPython instead
- CircuitPython (Adafruit) is excellent for beginner-friendly development: easy USB mass-storage deploy, many ready-to-use device libraries (the "CircuitPython Bundle"), and a very simple developer workflow.
- CircuitPython is fantastic for rapid prototyping and when you want rich sensor libraries without writing C. However, it's less convenient if you need tight timing, PIO assembly, or custom C modules.

Hybrid / advanced approaches
- If you need absolute performance for rendering or DMA-driven LVGL flushes, implement those paths in C (pico-sdk) and call them from MicroPython as native extensions; use MicroPython for glue and rapid iteration.
- The RP2 family (Pico/Pico2) supports multiple cores at the MCU level — you can run code on both cores using the pico-sdk (C). MicroPython's direct symmetric multicore support is limited; advanced multicore designs are easiest when you implement a C-side worker on core1 and expose a communication API to MicroPython.
- If the board includes a separate wireless coprocessor (some Pico W/2W variants include a WiFi chip), that chip runs its own firmware and is a separate architecture—you interact with it via sockets/driver APIs. Running Python simultaneously on both chips is only possible if the coprocessor itself supports a Python runtime (rare).

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
