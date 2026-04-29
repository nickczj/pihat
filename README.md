# Spectra 6 Raspberry Pi HAT

Open hardware preparation for a Raspberry Pi HAT that drives bare E Ink Spectra 6 panels, starting with the 7.3 inch Good Display GDEP073E01.

Phase 1 is intentionally scoped to the 7.3 inch board:

- Raspberry Pi 40-pin HAT/HAT+ mechanical and ID EEPROM pattern.
- Pimoroni `inky` compatible display wiring and EEPROM detection.
- 50-pin 0.5 mm FPC panel connector and DESPI-C73-derived panel-side support circuit.
- Rear-mounted buttons and two Qw/ST connectors on the user I2C bus.

The 13.3 inch GDEP133C02 / EL133UF1 work is captured as Phase 2 documentation only until the 7.3 inch board boots and refreshes reliably.

## Status

This repository is implementation prep, not fabrication release. The KiCad project shell and capture notes are present, but fabrication files must not be ordered until:

1. The schematic is completed against the official DESPI-C73 schematic and datasheets.
2. KiCad ERC is clean.
3. PCB layout is completed and DRC is clean against the selected manufacturer rules.
4. Gerbers, drill, BOM, and placement files are exported repeatably with `kicad-cli`.

Current progress is tracked in [docs/progress.md](docs/progress.md).

## Software Target

Python tooling targets Python 3.11+ and `inky==2.4.0`, cross-checked against Pimoroni `inky` commit `07035b30d2a1`.

## Layout

```text
kicad/
  shared/                  KiCad shared symbols/footprints and imported HAT template assets
  spectra6-hat-7in3/       Phase 1 KiCad project shell
  spectra6-hat-13in3/      Phase 2 placeholder notes
firmware/
  eeprom-flash/            Pimoroni-compatible EEPROM writer and HAT+ EEPROM notes
docs/                      Design decisions, pinout, bring-up, manufacturing notes
reference/                 Downloaded references, source index, checksums
enclosure/                 Phase 4 OpenSCAD placeholder
```

## Quick Checks

```bash
python3 -m unittest discover -s firmware/eeprom-flash
python3 firmware/eeprom-flash/flash_eeprom.py --variant 7in3 --version 1.0 --dry-run
sha256sum -c reference/SHA256SUMS
make kicad-version
make kicad-erc
make kicad-drc
```

KiCad export and ERC/DRC targets are documented in [docs/manufacturing.md](docs/manufacturing.md). The local CLI path is `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.
