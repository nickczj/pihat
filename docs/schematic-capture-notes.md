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

Initial schematic text extraction from the DESPI-C73 PDF shows these values and nets that must be verified visually during KiCad capture:

| Ref | Value / net |
|---|---|
| `Q1` | `Si1308EDL` |
| `D2`, `D3`, `D4` | `MBR0530` |
| `L1` | `10uH 1A` |
| `C2` | `47uF 25V` |
| `C3`, `C5`, `C6` | `10uF 25V` |
| `R2` | `1M` |
| `R4`, `R5` | `0` |
| `R10` | `1` |
| `L3`, `L4` | `L0603 120 100MHz` ferrite beads |
| Header nets | `3V3`, `GND`, `SDI`, `SCLK`, `CS`, `D/C`, `RES`, `BUSY` |
| Test/boost nets | `PREVGH`, `PREVGL`, `VCOM`, `VPH`, `PREVGH1`, `PREVGL1`, `VCOM1` |

## Intentional Phase 1 Deviations

- The host-side 8-pin header becomes Pi HAT routing to the 40-pin connector.
- GPIO assignments follow Pimoroni `inky`, not Waveshare demo examples.
- The HAT+ ID EEPROM and the `inky` EEPROM are separate blocks on separate I2C buses.
- Qw/ST connectors share bus 1 with the `inky` EEPROM and must avoid address `0x50`.

Every schematic deviation should also be placed as a KiCad schematic note before layout.

## Capture Assets

- `docs/capture-checklist-7in3.md` defines the net naming and capture order.
- `kicad/spectra6-hat-7in3/capture-bom-seed.csv` lists the first schematic refs, candidate KiCad symbols/footprints, and source/status for each part.

Use the CSV as a checklist while capturing the real schematic. Do not treat `TBD` footprints or `needs_visual_verify` rows as orderable BOM entries.
