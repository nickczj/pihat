# Progress

Last updated: 2026-04-29.

## Current State

The repository is in Phase 1 schematic capture. It is not ready for fabrication.

The project standard is KiCad 10.0.1. The Phase 1 schematic now contains real KiCad blocks for the Pi 40-pin header, HAT+ ID EEPROM, Pimoroni-compatible `inky` EEPROM, two Qw/ST connectors, four rear buttons, and a virtual DESPI-C73 host-net handoff block. The PCB is still a 174 x 123 mm outline placeholder. The real 50-pin FPC and DESPI-C73 boost/test network still need to be captured from the official schematic with visual pin-by-pin verification before layout.

## Completed

- [x] Initialized a local Git repository.
- [x] Scaffolded the project layout from `AGENTS.md`.
- [x] Added root project files: `README.md`, `LICENSE`, `.gitignore`, `pyproject.toml`, and `Makefile`.
- [x] Imported `devbisme/RPi_Hat_Template` symbol/footprint assets into `kicad/shared/`.
- [x] Downloaded Phase 1 reference material into `reference/`, including DESPI-C73 schematic/spec, GDEP073E01 datasheet mirror, Raspberry Pi HAT+ spec, Waveshare 13.3 inch manual/schematic, Good Display usage guidelines, and Pimoroni source snapshots.
- [x] Indexed references in `reference/sources.md`.
- [x] Generated and verified `reference/SHA256SUMS`.
- [x] Cross-checked Pimoroni `inky` EEPROM format and GPIO assignments against commit `07035b30d2a1`.
- [x] Documented the two-EEPROM architecture: HAT+ ID EEPROM on GPIO0/GPIO1 and `inky` EEPROM on GPIO2/GPIO3 bus 1 at `0x50`.
- [x] Documented the Phase 1 Pimoroni-compatible 7.3 inch pinout.
- [x] Documented the Phase 2 13.3 inch dual-CS SPI correction from Pimoroni `inky`.
- [x] Added `firmware/eeprom-flash/flash_eeprom.py` for the 29-byte Pimoroni `EPDType` payload.
- [x] Added unit tests for 7.3 inch, 7.3 inch AC override, 13.3 inch future payloads, version parsing, and EEPROM address prefixes.
- [x] Added a HAT+ EEPROM template directory for the Raspberry Pi `eeptools` flow.
- [x] Added systemd timer templates for the 24-hour refresh requirement.
- [x] Added KiCad starter files for `kicad/spectra6-hat-7in3/`.
- [x] Added a Phase 2 placeholder directory for `kicad/spectra6-hat-13in3/`.
- [x] Added an OpenSCAD enclosure envelope placeholder.
- [x] Found and used local KiCad CLI at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.
- [x] Verified local KiCad CLI version `10.0.1`.
- [x] Standardized the repo on KiCad `10.0.1` in `.kicad-version`.
- [x] Upgraded the Phase 1 schematic and PCB files with KiCad 10.0.1 CLI.
- [x] Added `docs/capture-checklist-7in3.md` for Phase 1 schematic capture order and net naming.
- [x] Added `docs/despi-c73-reference-map.md` with the official DESPI-C73 host header, FPC pin map, and visible part values.
- [x] Added `kicad/spectra6-hat-7in3/capture-bom-seed.csv` as a source-backed capture/BOM seed.
- [x] Added `docs/procurement.md` with the current GDEP073E01 sourcing check.
- [x] Confirmed the Phase 1 GDEP073E01 panel is already in hand.
- [x] Replaced the KiCad capture-prep sheet with real Pi-side/control schematic blocks.
- [x] Captured the official KiCad Raspberry Pi HAT-style 40-pin header and HAT+ ID EEPROM pattern.
- [x] Captured the separate bus-1 `inky` EEPROM, Qw/ST connectors, and rear buttons.
- [x] Added a virtual DESPI-C73 8-pin host-net block for `3V3`, `GND`, `EPD_SDI`, `EPD_SCLK`, `EPD_CS`, `EPD_DC`, `EPD_RESET`, and `EPD_BUSY`.
- [x] Corrected DESPI-C73 capture values from the official schematic preview: C2 is `4.7uF/25V`, R3/R4 are `0.22ohm`, and the second switcher leg around Q2/D1/L2 is now tracked.
- [x] Ran ERC on the current KiCad schematic: 0 errors, 18 warnings. Remaining warnings are isolated labels on unused Pi GPIOs and library-symbol mismatch warnings from the imported template symbols.
- [x] Ran DRC on the current KiCad prep PCB outline: 0 violations, 0 unconnected items.
- [x] Exported the current schematic PDF, gerbers, and drill files from the current shell.

## Not Done

- [ ] Add the exact Good Display GDEP133C02 datasheet for Phase 2.
- [ ] Add the exact Spectra 6-specific design notice if it is separate from Good Display's general e-paper usage guidelines.
- [ ] Capture the real DESPI-C73 50-pin FPC and boost/test network in KiCad from the official PDF.
- [ ] Identify final JLCPCB/LCSC orderable equivalents for every DESPI-C73 part.
- [ ] Add schematic symbols, footprints, manufacturer part numbers, and BOM fields.
- [ ] Lay out and route the real 7.3 inch PCB.
- [ ] Export BOM and placement CSV.
- [ ] Review generated gerbers visually after the real layout exists.
- [ ] Order, assemble, and bring up hardware.

## Next Steps

1. Visually verify `reference/despi-c73-schematic-20220728.pdf` and replace the virtual J5 host-net block with the real 50-pin FPC connector plus DESPI-C73 boost/test network.
2. Use `docs/capture-checklist-7in3.md` and `kicad/spectra6-hat-7in3/capture-bom-seed.csv` as the remaining capture checklist.
3. Pick JLCPCB/LCSC parts for the EEPROM, FPC connector, diodes, MOSFET, inductor, ferrites, passives, buttons, and Qw/ST connectors.
4. Assign final footprints and BOM fields.
5. Run ERC until the real schematic has no errors and only reviewed/suppressed intentional warnings.
6. Update the PCB from schematic, then place the board around the 174 x 123 mm outline, FPC access, Pi clearance, rear button access, and enclosure constraints.
7. Route as a 2-layer prototype, then run DRC against 5/5 mil minimum rules.
8. Export schematic PDF, gerbers, drill, BOM, and placement files with `make kicad-export`.
9. Review fabrication outputs before ordering.
