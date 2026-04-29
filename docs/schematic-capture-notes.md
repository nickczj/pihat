# Schematic Capture Notes

These notes are the current capture ledger for translating the reference circuits into KiCad. They are not a substitute for ERC and a human schematic review against the PDFs.

## 7.3 Inch Reference

Authoritative source: Good Display DESPI-C73 schematic `DESPI-C73-20220728-SCH.pdf`, saved as `reference/despi-c73-schematic-20220728.pdf`.

Confirmed from the official Good Display product page:

| Item | Value |
|---|---|
| Board role | Peripheral boost circuit and 50-pin panel adapter |
| Display interface | 50-pin, 0.5 mm FPC |
| Host interface | SPI |
| Operating voltage | 3.3 V |
| Key parts | SI1308EDL, MBR0530 |
| Diagnostic feature | Reserved boost detection points |

Schematic text extraction plus visual PDF review shows these values and nets that must be carried into KiCad capture:

| Ref | Value / net |
|---|---|
| `Q1` | `Si1308EDL` |
| `Q2` | `Si2301` |
| `D1`, `D2`, `D3`, `D4` | `MBR0530` |
| `L1`, `L2` | `10uH 1A` |
| `C1`, `C2`, `C15` | `4.7uF/25V` |
| `C3`, `C4`, `C5`, `C6`, `C8`, `C9`, `C10`, `C17`, `C18`, `C19` | `10uF/25V` |
| `C7`, `C16` | `0.47uF/25V` |
| `C11`, `C13`, `C14`, `C20`, `C21`, `C22` | `1uF/25V` |
| `C12` | `2.2uF/25V` |
| `C23` | `100uF/6.3V` |
| `C24` | `0.1uF/25V` |
| `R1`, `R2` | `1M` |
| `R3`, `R4` | `0.22ohm` |
| `R5`, `R6`, `R8`, `R9`, `R11`, `R12` | `0ohm` |
| `R7` | `NC` |
| `R10` | `1ohm` |
| `L3`, `L4` | `L0603 120 100MHz` ferrite beads |
| Header nets | `3V3`, `GND`, `SDI`, `SCLK`, `CS`, `D/C`, `RES`, `BUSY` |
| Test/boost nets | `PREVGH`, `PREVGL`, `VCOM`, `VPH`, `PREVGH1`, `PREVGL1`, `VCOM1` |
| FPC pins | See `docs/despi-c73-reference-map.md` |

## Intentional Phase 1 Deviations

- The host-side 8-pin header becomes Pi HAT routing to the 40-pin connector.
- GPIO assignments follow Pimoroni `inky`, not Waveshare demo examples.
- The HAT+ ID EEPROM and the `inky` EEPROM are separate blocks on separate I2C buses.
- Qw/ST connectors share bus 1 with the `inky` EEPROM and must avoid address `0x50`.

Every schematic deviation should also be placed as a KiCad schematic note before layout.

## Capture Assets

- `docs/capture-checklist-7in3.md` defines the net naming and capture order.
- `docs/despi-c73-reference-map.md` records the official DESPI-C73 host header, FPC pin map, and visible part values.
- `kicad/spectra6-hat-7in3/capture-bom-seed.csv` lists the first schematic refs, candidate KiCad symbols/footprints, and source/status for each part.

Use the CSV as a checklist while capturing the real schematic. Do not treat `TBD` footprints or `needs_visual_verify` rows as orderable BOM entries.

## KiCad Capture Status

Completed in `kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_sch`:

- Official KiCad Raspberry Pi HAT-style 40-pin header block.
- HAT+ ID EEPROM block on GPIO0/GPIO1 only, based on the Raspberry Pi HAT template pattern.
- Separate Pimoroni-compatible `inky` EEPROM block on `I2C1_SDA`/`I2C1_SCL` at address `0x50`.
- Two Qw/ST connectors sharing bus 1, with `0x50` reserved for the `inky` EEPROM.
- Four rear button symbols on `BTN_A`, `BTN_B`, `BTN_C`, and `BTN_D`.
- A virtual DESPI-C73 host-net handoff block, `J5`, for the eight SPI/control/power nets.

Still pending:

- Replace virtual `J5` with the real 50-pin FPC connector from the DESPI-C73 schematic.
- Capture the DESPI-C73 boost/test network and all verified values.
- Assign final footprints, manufacturer part numbers, LCSC/JLCPCB fields, and reviewed BOM data.
- Review remaining ERC warnings. Current ERC has zero errors; warnings are isolated labels on unused Pi GPIOs and imported-template symbol mismatch warnings.
