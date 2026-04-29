# DESPI-C73 Reference Map

Source: Good Display DESPI-C73 schematic `DESPI-C73-20220728-SCH.pdf`, saved as `reference/despi-c73-schematic-20220728.pdf`.

This is the working map for replacing the temporary virtual `J5` host-net block in the KiCad schematic. Values below are taken from the official schematic text extraction and visually checked against the rendered PDF preview on 2026-04-29. Do not treat this as a fabrication BOM until footprints, voltage/current ratings, and orderable MPNs are reviewed.

## Host Header P2

| P2 pin | DESPI-C73 net | Project net |
|---|---|---|
| 1 | `3V3` | `+3V3` |
| 2 | `GND` | `GND` |
| 3 | `SDI` | `EPD_SDI` |
| 4 | `SCLK` | `EPD_SCLK` |
| 5 | `CS` | `EPD_CS` |
| 6 | `D/C` | `EPD_DC` |
| 7 | `RES` | `EPD_RESET` |
| 8 | `BUSY` | `EPD_BUSY` |

## FPC P1 Pin Map

| P1 pin | Net / signal |
|---|---|
| 1 | `VPP` |
| 2 | `TFT_VCOM` |
| 3 | `FPL_VCOM` |
| 4 | `VDD` |
| 5 | `GDRH` |
| 6 | `RESEH` |
| 7 | `GDRL` |
| 8 | `RESEL` |
| 9 | `GDRC` |
| 10 | `RESEC` |
| 11 | `VPC` |
| 12 | `GND` |
| 13 | `VGL` |
| 14 | `VPH` |
| 15 | `VSH` |
| 16 | `VSH_LV` |
| 17 | `VSH_LV2` |
| 18 | `VSL` |
| 19 | `VSL_LV` |
| 20 | `VSL_LV2` |
| 21 | `GND` |
| 22 | `REFN` |
| 23 | `REFP` |
| 24 | `TSCL` |
| 25 | `TSDA` |
| 26 | `BS0` |
| 27 | `BS1` |
| 28 | `RST_N` |
| 29 | `BUSY_N` |
| 30 | `DC` |
| 31 | `CSB1` |
| 32 | `SCL` |
| 33 | `SI0` |
| 34 | `SI1` |
| 35 | `SI2` |
| 36 | `SI3` |
| 37 | `VDDD` |
| 38 | `VDD` |
| 39 | `GND` |
| 40 | `VDDIO` |
| 41 | `VCP2` |
| 42 | `CP2N` |
| 43 | `CP2P` |
| 44 | `VCP1` |
| 45 | `CP1N` |
| 46 | `CP1P` |
| 47 | `CGH1N` |
| 48 | `CGH1P` |
| 49 | `VGH` |
| 50 | `VCOMBD` |

## Parts Visible On Official Schematic

| Ref | Value |
|---|---|
| `Q1` | `Si1308EDL` |
| `Q2` | `Si2301` |
| `D1`, `D2`, `D3`, `D4` | `MBR0530` |
| `L1`, `L2` | `10uH 1A` |
| `L3`, `L4` | `L0603(120ohm@100MHz)` |
| `R1`, `R2` | `1M` |
| `R3`, `R4` | `0.22ohm` |
| `R5`, `R6`, `R8`, `R9`, `R11`, `R12` | `0ohm` |
| `R7` | `NC` |
| `R10` | `1ohm` |
| `C1`, `C2`, `C15` | `4.7uF/25V` |
| `C3`, `C4`, `C5`, `C6`, `C8`, `C9`, `C10`, `C17`, `C18`, `C19` | `10uF/25V` |
| `C7`, `C16` | `0.47uF/25V` |
| `C11`, `C13`, `C14`, `C20`, `C21`, `C22` | `1uF/25V` |
| `C12` | `2.2uF/25V` |
| `C23` | `100uF/6.3V` |
| `C24` | `0.1uF/25V` |
| `P1` | `FPC-50PIN` |
| `P2` | `8PINx2.54mm` |

## Capture Notes

- `P2` is not a physical connector on this HAT. Its eight nets are already represented by virtual `J5`; final capture should wire those nets directly into `P1` and the boost/test network.
- `SI1`, `SI2`, and `SI3` are present on the panel FPC but are not used by the Pimoroni-compatible 7.3 inch SPI pinout. Confirm whether they should be tied per DESPI-C73, left no-connect, or exposed as test pads before layout.
- `BS0` and `BS1` are strap pins in the DESPI-C73 schematic. Preserve the DESPI-C73 resistor options rather than hard-coding the bus mode until the panel datasheet has been checked against the reference schematic.
- The schematic exposes reserved boost/test nets `PREVGH`, `PREVGH1`, `PREVGL`, `PREVGL1`, `VCOM`, `VCOM1`, `GND`, and `GND1`. Add test pads only if they do not create panel insertion or enclosure clearance issues.
