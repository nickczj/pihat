# Pinout

Phase 1 follows Pimoroni `inky` wiring for zero-code-change display support. Waveshare demo wiring is reference-only for this board.

## EEPROM Roles

There are two EEPROM roles because Raspberry Pi HAT+ detection and Pimoroni `inky` detection use different buses.

| Role | Bus / pins | Address | Purpose | Notes |
|---|---:|---:|---|---|
| HAT+ ID EEPROM | GPIO0 ID_SD, GPIO1 ID_SC | HAT+ allowed ID address | Raspberry Pi firmware board identification and overlays | Nothing else may connect to GPIO0/1 except the ID EEPROM and required pull-ups. |
| `inky` display EEPROM | GPIO2 SDA1, GPIO3 SCL1 | `0x50` | Pimoroni `inky.auto.auto()` display identification | Shares the Qw/ST bus; any Qw/ST device at `0x50` conflicts unless the display EEPROM is disabled or moved in a later revision. |

## 7.3 Inch Panel Interface

| Pi GPIO | Physical pin | Signal | Destination |
|---:|---:|---|---|
| GPIO8 | 24 | SPI0 CE0 / `CS` | Panel `CS` |
| GPIO10 | 19 | SPI0 MOSI / `SDI` | Panel `SDI` |
| GPIO11 | 23 | SPI0 SCLK / `SCK` | Panel `SCK` |
| GPIO22 | 15 | `D/C` | Panel data/command |
| GPIO27 | 13 | `RESET` | Panel reset |
| GPIO17 | 11 | `BUSY` | Panel busy input |
| 3V3 | 1 or 17 | `3.3V` | Panel logic/power input |
| GND | any GND pin | `GND` | Common return |

The DESPI-C73 8-pin breakout order is documented as `3.3V`, `GND`, `SDI`, `SCLK`, `CS`, `D/C`, `RES`, `BUSY`. The HAT routes those signals to the 50-pin FPC-side circuit rather than exposing the 8-pin header as the primary interface.

## Buttons

Buttons are rear-mounted for enclosure protection.

| Button | Pi GPIO | Physical pin | Pull |
|---|---:|---:|---|
| A | GPIO5 | 29 | Software pull-up |
| B | GPIO6 | 31 | Software pull-up |
| C | GPIO16 | 36 | Software pull-up |
| D | GPIO24 | 18 | Software pull-up |

These match the Pimoroni 7.3 inch Spectra 6 example assignments. Phase 2 must revisit button C because Pimoroni's 13.3 inch driver uses GPIO16 as the second display chip-select.

## Qw/ST Connectors

Two JST-SH 4-pin Qw/ST connectors are connected to GPIO2/GPIO3, 3.3V, and GND. They intentionally share the `inky` EEPROM bus. Address `0x50` is reserved by this board while the EEPROM is populated/enabled.

## Phase 2 Warning

The initial research assumption was that the 13.3 inch board should expose a four-data-line QSPI Linux interface. Pimoroni's `inky` driver for the 13.3 inch Spectra 6 display instead uses SPI with two chip-selects. Phase 2 should follow the driver-compatible dual-CS wiring unless there is a deliberate software change.

