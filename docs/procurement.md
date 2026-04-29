# Procurement Notes

Last checked: 2026-04-29.

## Panel

| Item | Source checked | Result |
|---|---|---|
| GDEP073E01 7.3 inch Spectra 6 panel | https://buyepaper.com/products/gdep073e01 | Page lists the product at USD 42.14 and confirms the 50-pin FPC SPI specs, but the selected base `EPD` option shows `0 in stock` in page data. Treat panel availability as unresolved until Good Display confirms by email or checkout. |
| GDEP073E01 official product page | https://www.good-display.com/product/533.html | Confirms product identity and specs; not enough for shipping/stock confirmation. |

Action: email `buyepaper@good-display.com` or use checkout to confirm current stock and shipping to Singapore before ordering PCBs.

## Component Selection Rules

- Prefer JLCPCB Basic Parts when a stable equivalent exists.
- Use Extended Parts only when the loader fee is justified or hand assembly is planned.
- Use LCSC-stocked/DigiKey/Mouser parts for fragile or exact-match components such as FPC connectors if JLCPCB assembly stock is weak.
- Re-check all live stock at order time. The BOM seed is a capture aid, not an orderable BOM.

## Known Candidate Parts

| Function | Candidate | Status |
|---|---|---|
| 50-pin FPC | Hirose `FH12-50S-0.5SH` family | KiCad footprint exists. Contact side/orientation must be verified against the panel FPC before layout. |
| EEPROMs | `24LC256` / `CAT24C256`, SOIC-8 preferred for prototype | Need JLCPCB Basic/Extended review. |
| DESPI-C73 MOSFET | `Si1308EDL` class | Use the exact part or a datasheet-equivalent part only after verifying voltage, threshold, and Rds(on). |
| DESPI-C73 diodes | `MBR0530` class | Verify package and ratings against the DESPI-C73 schematic/datasheet before choosing a replacement. |
| Qw/ST connectors | JST-SH 1.0 mm 4-pin horizontal or vertical | Pick orientation after enclosure/button side is fixed. |
| Rear buttons | SMD tactile switch | Pick after enclosure clearance is known. |

