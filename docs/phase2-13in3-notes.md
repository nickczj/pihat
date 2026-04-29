# Phase 2: 13.3 Inch Notes

Phase 2 is deferred until the 7.3 inch board works end-to-end.

## Cross-Checks Captured Now

Waveshare's 13.3 inch HAT+ material confirms:

- 1600 x 1200 resolution.
- Around 19 second full refresh in vendor examples.
- 24-hour refresh guidance.
- Fragile FPC handling and full-screen refresh expectations.
- 60-pin FPC panel interface.
- Schematic support for multiple serial modes through `BS0`/`BS1`.

Pimoroni `inky` driver compatibility is the controlling software decision for this project. The current 13.3 inch driver uses SPI with two chip-selects:

| Signal | GPIO |
|---|---:|
| `RESET` | GPIO27 |
| `BUSY` | GPIO17 |
| `D/C` | GPIO22 |
| `MOSI` | GPIO10 |
| `SCLK` | GPIO11 |
| `CS0` | GPIO26 |
| `CS1` | GPIO16 |

That means the Phase 1 GPIO16 button assignment cannot be reused unchanged on a 13.3 inch Pimoroni-compatible board.

## Phase 2 Design Direction

- Use a 60-pin 0.5 mm FPC connector.
- Prefer a 4-layer PCB because of board size and signal integrity margin.
- Follow Pimoroni dual-CS SPI if zero-code-change `inky` compatibility remains the goal.
- Keep the two-EEPROM architecture: HAT+ ID EEPROM on GPIO0/GPIO1 and `inky` EEPROM on GPIO2/GPIO3 at `0x50`.
- Re-check whether a shared carrier plus panel adapter is worth the complexity after the 7.3 inch bring-up.

