KICAD_CLI ?= /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli

.PHONY: test eeprom-dry-run refs-check kicad-version kicad-erc kicad-drc kicad-export

test:
	python3 -m unittest discover -s firmware/eeprom-flash

eeprom-dry-run:
	python3 firmware/eeprom-flash/flash_eeprom.py --variant 7in3 --version 1.0 --dry-run

refs-check:
	sha256sum -c reference/SHA256SUMS

kicad-version:
	$(KICAD_CLI) version

kicad-erc:
	$(KICAD_CLI) sch erc kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_sch \
		--output kicad/spectra6-hat-7in3/outputs/erc.rpt

kicad-drc:
	$(KICAD_CLI) pcb drc kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_pcb \
		--output kicad/spectra6-hat-7in3/outputs/drc.rpt

kicad-export:
	mkdir -p kicad/spectra6-hat-7in3/outputs/gerbers
	$(KICAD_CLI) sch export pdf kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_sch \
		-o docs/schematic-7in3.pdf
	$(KICAD_CLI) pcb export gerbers kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_pcb \
		-o kicad/spectra6-hat-7in3/outputs/gerbers/
	$(KICAD_CLI) pcb export drill kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_pcb \
		-o kicad/spectra6-hat-7in3/outputs/gerbers/ \
		--excellon-separate-th
