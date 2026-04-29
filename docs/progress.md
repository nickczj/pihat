# Progress

Last updated: 2026-04-29.

## Current State

The repository is ready for Phase 1 schematic capture work. It is not ready for fabrication.

The KiCad files currently validate as a project shell only: the schematic is a capture-prep sheet and the PCB is a 174 x 123 mm outline placeholder. The real circuit still needs to be captured from the DESPI-C73 schematic and reviewed before layout.

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
- [x] Ran ERC on the current KiCad prep schematic: 0 violations.
- [x] Ran DRC on the current KiCad prep PCB outline: 0 violations, 0 unconnected items.
- [x] Exported the current schematic PDF, gerbers, and drill files from the prep shell.

## Not Done

- [ ] Confirm the final KiCad major version for collaborators. Current local CLI is KiCad 10.0.1; original plan assumed KiCad 8 or 9.
- [ ] Confirm current GDEP073E01 panel availability and shipping window.
- [ ] Add the exact Good Display GDEP133C02 datasheet for Phase 2.
- [ ] Add the exact Spectra 6-specific design notice if it is separate from Good Display's general e-paper usage guidelines.
- [ ] Capture the real 7.3 inch schematic in KiCad from the DESPI-C73 PDF.
- [ ] Identify final JLCPCB/LCSC orderable equivalents for every DESPI-C73 part.
- [ ] Add schematic symbols, footprints, manufacturer part numbers, and BOM fields.
- [ ] Lay out and route the real 7.3 inch PCB.
- [ ] Export BOM and placement CSV.
- [ ] Review generated gerbers visually after the real layout exists.
- [ ] Order, assemble, and bring up hardware.

## Next Steps

1. Decide whether the repo should standardize on KiCad 10.0.1, since that is the installed CLI, or install KiCad 8/9 to match the original plan.
2. Open `kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_pro` in KiCad and replace the capture-prep notes with the real schematic blocks.
3. Capture the Pi-side circuit first: 40-pin header, HAT+ ID EEPROM, `inky` EEPROM, Qw/ST connectors, rear buttons, and power pins.
4. Capture the DESPI-C73 panel-side circuit next, using only values verified from the official schematic/datasheet.
5. Pick JLCPCB/LCSC parts for the EEPROM, FPC connector, diodes, MOSFET, inductor, ferrites, passives, buttons, and Qw/ST connectors.
6. Assign footprints and run ERC until the real schematic is clean.
7. Place the board around the 174 x 123 mm outline, FPC access, Pi clearance, rear button access, and enclosure constraints.
8. Route as a 2-layer prototype, then run DRC against 5/5 mil minimum rules.
9. Export schematic PDF, gerbers, drill, BOM, and placement files with `make kicad-export`.
10. Review fabrication outputs before ordering.

