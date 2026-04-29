# 7.3 Inch Schematic Capture Checklist

Use KiCad 10.0.1. Capture values only from the saved reference PDFs/pages or from a documented datasheet-equivalent selection.

## Capture Order

- [x] Pi HAT connector and power rails.
- [x] HAT+ ID EEPROM on GPIO0/GPIO1 only.
- [x] Pimoroni `inky` EEPROM on GPIO2/GPIO3 bus 1 at `0x50`.
- [x] Two Qw/ST connectors on GPIO2/GPIO3.
- [x] Four rear buttons on GPIO5, GPIO6, GPIO16, GPIO24.
- [x] 7.3 inch virtual host interface nets: `CS`, `SDI`, `SCLK`, `D/C`, `RES`, `BUSY`, `3V3`, `GND`.
- [ ] 50-pin FPC connector and DESPI-C73 panel-side nets.
- [ ] DESPI-C73 boost/test network.
- [x] Schematic notes documenting current intentional deviations from DESPI-C73 and Waveshare wiring.
- [ ] Footprints, manufacturer/LCSC fields, and BOM review.

## Pi-Side Net Names

Use these net names consistently in KiCad:

| Net | Pi GPIO / source | Destination |
|---|---|---|
| `EPD_CS` | GPIO8 / SPI0 CE0 | Panel FPC `CS` |
| `EPD_SDI` | GPIO10 / SPI0 MOSI | Panel FPC `SDI` |
| `EPD_SCLK` | GPIO11 / SPI0 SCLK | Panel FPC `SCLK` |
| `EPD_DC` | GPIO22 | Panel FPC `D/C` |
| `EPD_RESET` | GPIO27 | Panel FPC `RES` |
| `EPD_BUSY` | GPIO17 | Panel FPC `BUSY` |
| `I2C1_SDA` | GPIO2 | `inky` EEPROM, Qw/ST SDA |
| `I2C1_SCL` | GPIO3 | `inky` EEPROM, Qw/ST SCL |
| `ID_SD` | GPIO0 | HAT+ ID EEPROM SDA only |
| `ID_SC` | GPIO1 | HAT+ ID EEPROM SCL only |
| `BTN_A` | GPIO5 | Rear button A |
| `BTN_B` | GPIO6 | Rear button B |
| `BTN_C` | GPIO16 | Rear button C |
| `BTN_D` | GPIO24 | Rear button D |

## ERC Expectations

- Power pins must have explicit power symbols or power flags as needed.
- HAT+ ID nets must not connect to Qw/ST or the `inky` EEPROM.
- Bus 1 EEPROM address pads should encode `0x50`.
- All DESPI-C73 test rails should have visible net names and test pads if the reference board exposes them.
- Any unconnected FPC pins must be marked no-connect only after checking the DESPI-C73 schematic and panel datasheet.
