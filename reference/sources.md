# Reference Sources

Sources were gathered on 2026-04-28. Files under `reference/vendor/` are copied source snapshots or adjacent vendor references, not authoritative hardware schematics for this project.

## Raspberry Pi

| Local file | Source | Purpose |
|---|---|---|
| `raspberry-pi-hat-plus-specification.pdf` | https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf | HAT+ EEPROM, GPIO0/GPIO1 restrictions, electrical/mechanical requirements. |

Important decision: GPIO0/GPIO1 are reserved for the HAT+ ID EEPROM and required pull-ups only.

## Good Display 7.3 Inch / DESPI-C73

| Local file | Source | Purpose |
|---|---|---|
| `reference-pages/good-display-despi-c73-product.html` | https://www.good-display.com/product/522.html | Official DESPI-C73 product page: 50-pin 0.5 mm SPI interface, 3.3 V operation, SI1308EDL and MBR0530 key parts. |
| `reference-pages/good-display-despi-c73-spec-page.html` | https://www.good-display.com/companyfile/1108.html | Official DESPI-C73 specification download page. |
| `reference-pages/good-display-despi-c73-schematic-page.html` | https://www.good-display.com/companyfile/1945.html | Official DESPI-C73 schematic download page. |
| `despi-c73-schematic-20220728.pdf` | https://v4.cecdn.yun300.cn/100001_1909185148/DESPI-C73-20220728-SCH.pdf | Authoritative 7.3 inch panel-side reference schematic. |
| `despi-c73-specification.pdf` | https://www.laskakit.cz/user/related_files/adapter_board_for_7-3_inch_e-paper_display_despi-c73.pdf | Mirror of DESPI-C73 specification PDF, used because Good Display download links can be session/referer sensitive. |
| `gdep073e01-datasheet.pdf` | https://www.laskakit.cz/user/related_files/gdep073e01-1-0.pdf | Mirror of GDEP073E01 datasheet, used until a stable direct Good Display PDF URL is added. |
| `reference-pages/good-display-gdep073e01-product.html` | https://www.good-display.com/product/533.html | Official GDEP073E01 product page snapshot. |
| `reference-pages/good-display-epaper-display-usage-guidelines-page.html` | https://www.good-display.com/companyfile/1620.html | Official Good Display usage-guidelines download page. |
| `epaper-display-usage-guidelines.pdf` | https://v4.cecdn.yun300.cn/100001_1909185148/ePaper%20Display%20Usage%20Guidelines.pdf | Good Display usage guidance for e-paper handling and refresh/storage practices. |

## Waveshare 13.3 Inch

| Local file | Source | Purpose |
|---|---|---|
| `reference-pages/waveshare-13in3-hat-plus-manual.html` | https://www.waveshare.com/wiki/13.3inch_e-Paper_HAT+_(E)_Manual | Official manual cross-check: resolution, refresh time, 24-hour guidance, FPC handling, demo behavior. |
| `waveshare-13in3-hat-plus-schematic.pdf` | https://files.waveshare.com/wiki/13.3inch%20e-Paper%20HAT%2B/13.3inch_e-Paper_HAT%2B.pdf | Official Waveshare 13.3 inch HAT+ schematic cross-check for Phase 2. |
| `reference-pages/waveshare-7in3-hat-e-manual.html` | https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(E)_Manual | Reference-only comparison for Waveshare demo wiring and handling notes. |

## Pimoroni `inky`

Pinned upstream commit: `07035b30d2a1251c197559502d2f026923c3ea3b`.

| Local file | Upstream path | Purpose |
|---|---|---|
| `vendor/pimoroni-inky-eeprom-07035b30d2a1.py` | https://github.com/pimoroni/inky/blob/07035b30d2a1251c197559502d2f026923c3ea3b/inky/eeprom.py | EEPROM structure and bus/address behavior. |
| `vendor/pimoroni-inky-e673-07035b30d2a1.py` | https://github.com/pimoroni/inky/blob/07035b30d2a1251c197559502d2f026923c3ea3b/inky/inky_e673.py | 7.3 inch Spectra 6 GPIO assignments. |
| `vendor/pimoroni-inky-el133uf1-07035b30d2a1.py` | https://github.com/pimoroni/inky/blob/07035b30d2a1251c197559502d2f026923c3ea3b/inky/inky_el133uf1.py | 13.3 inch Spectra 6 dual-CS GPIO assignments. |

Important decision: `inky` reads bus 1 address `0x50`; it does not use the Raspberry Pi HAT+ ID EEPROM bus for display identity.

## Phase 2 Adjacent References

| Local file | Source | Purpose |
|---|---|---|
| `vendor/seeed-13in3-e6-module-datasheet.pdf` | https://files.seeedstudio.com/wiki/Other_Display/1330-E6-epaper/13.3_E6_eInk_Display_module_Datasheet.pdf | Vendor-adjacent 13.3 inch E6 module datasheet cross-check only. Not a replacement for Good Display GDEP133C02. |

## Pending Exact References

- `gdep133c02-datasheet.pdf`: direct Good Display download was attempted but the CDN response was referer/throughput sensitive and did not complete reliably in this environment. Phase 2 must add the exact Good Display GDEP133C02 datasheet before schematic capture.
- E Ink Spectra 6-specific design notice: still needs a stable downloadable source added to `reference/` if Good Display publishes it separately from the general usage guidelines. The 24-hour refresh requirement remains tracked in docs and bring-up notes.
