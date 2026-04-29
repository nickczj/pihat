# Spectra 6 e-Paper Pi HAT — Project Context

This file is the entry point for working on this project with Codex. Read it first and treat it as the source of truth for design intent, constraints, and prior decisions. When something here conflicts with a quick-search result, **trust this file** and ask before deviating.

Current progress is tracked in `docs/progress.md`. Update that file whenever Phase 0/1 status changes.

---

## What we're building

An open-source Raspberry Pi HAT that drives a bare E Ink Spectra 6 e-paper panel (7.3" or 13.3" variants) for a battery-powered photo/art frame with optional Home Assistant dashboard duty.

**Why we're building it instead of buying:**
- No off-the-shelf single-PCB Pi HAT exists for the 7.3" Spectra 6 except Pimoroni's Inky Impression — and Pimoroni doesn't sell the bare PCB
- Waveshare ships a working 7.3" "HAT (E)" kit but it's a three-board sandwich (panel + 50→8 pin adapter + Universal Driver HAT) and they don't sell the 50-pin adapter separately
- For 13.3", Waveshare's HAT+ is the only single-board solution but is expensive and not open
- We want freedom to add features the commercial options don't have: on-board LiPo + power-cycling, custom button layout, a Pimoroni-style EEPROM so the `inky` library auto-detects it, and an outline tuned for our 3D-printed enclosure

**Build economics reality check:**
For a single frame, Pimoroni Inky Impression at ~$84 is cheaper than this DIY route once time is counted. This project is justified only when one or more of: building 3+ frames, want LiPo charging on-board, want a non-standard PCB outline, or want the learning experience. The user is aware of this — proceed without re-litigating.

---

## Hard constraints

| Constraint | Value | Source / why |
|---|---|---|
| Form factor | Raspberry Pi HAT (40-pin GPIO, HAT+ standard preferred) | User wants Pi Zero 2 W flexibility for image-source software (Immich, Google Photos, HA `media_source`) |
| Target SBC | Raspberry Pi Zero 2 W (with 40-pin headers soldered) | Smallest Pi that runs full Linux + Wi-Fi |
| Panels supported | 7.3" GDEP073E01 **and** 13.3" GDEP133C02, ideally on the same PCB family with two variants | User requested both options |
| Power input | USB-C 5V (Pi-side) **plus** optional onboard LiPo + power-cycling for >1 week battery life | Existing user requirement from photo frame discussion |
| Software target | Pimoroni `inky` Python library (auto-detects via I²C EEPROM) on Pi OS Bookworm | Most mature Spectra 6 software stack on Linux |
| Mass production | JLCPCB / PCBWay 2-layer or 4-layer, standard process | Cheap small-run prototypes |
| EDA tool | KiCad CLI 10.0.1 currently validated locally; final collaborator version still needs decision | User found local CLI at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`; original plan assumed KiCad 8 or 9 |
| 3D-printable enclosure | Designed in OpenSCAD or FreeCAD, sliced for Bambu P1S | User has the printer; simpler than commissioning external CAD |

---

## What NOT to do (failure modes from prior research)

- **Do not specify a TPS65185 PMIC.** Both Spectra 6 panels we target are *integrated-controller* panels — the boost converters and gate drivers live inside the panel itself on the COG. They want a clean 3.3V rail and SPI/QSPI signals. TPS65185 is for raw e-reader panels (EPDiy territory) and would be wrong architecturally and cost.
- **Do not try to drive 7.3" and 13.3" off literally the same PCB.** The 7.3" uses 50-pin SPI; the 13.3" uses 60-pin QSPI. Two PCB variants sharing a common motherboard + swappable adapter daughterboard is fine; one universal board is not.
- **Do not use the Waveshare "Universal e-Paper Driver HAT" pinout for the screen-side connector.** It's a 9-pin GH1.25 cable, not the 50-pin FPC the Spectra 6 panel terminates in. The Waveshare 7.3" kit handles this with a separate FPC adapter daughterboard that is not sold standalone.
- **Do not assume Spectra 6 supports partial refresh.** It does not. Full-screen refresh only, ~20–25 seconds end-to-end.
- **Do not reuse EPDiy's V7 PCB layout wholesale.** Useful as reference for ESP32-S3 power management *only*. The display interface is completely different (parallel bus + TPS65185 vs. serial SPI to integrated controller).
- **Do not invent the schematic.** The Good Display DESPI-C73 PDF schematic and Waveshare 13.3" HAT+ schematic are publicly published. Use them as the authoritative reference for the panel-side circuit. Schematic authorship of trivial breakout circuits is not copyrightable; we are reimplementing, not copying art.
- **Do not skip the I²C EEPROM.** Without it the Pimoroni `inky` library can't auto-detect the board, which negates the main software ergonomics win over the cheaper DESPI-C73-and-jumpers approach.

---

## Reference materials (read these before designing)

All saved or linked under `reference/`. If a link is dead, search for the title — they're all permanent enough that a fresh URL exists.

### Schematics (the actual recipe)
- **Good Display DESPI-C73 schematic PDF** — `good-display.com/companyfile/1108.html`. The reference circuit for the 7.3" panel side. ~15 components: FPC connector, boost circuit (small inductor + a few caps for the panel's V_DD rail), and the SPI breakout. **This is the authoritative source for the 7.3" panel-side schematic.**
- **Waveshare 13.3" e-Paper HAT+ (E) schematic** — published as PDF on the Waveshare wiki at `waveshare.com/wiki/13.3inch_e-Paper_HAT+_(E)_Manual`. Reference for the 60-pin QSPI variant.
- **Good Display GDEP073E01 datasheet** — pin definitions, command set, voltage requirements (3.3V logic, 2.3–3.6V tolerated)
- **Good Display GDEP133C02 datasheet** — same for 13.3" panel
- **E Ink Spectra 6 (E6) Design Notice** — Good Display application note. Specifies the 24-hour-refresh requirement to prevent retention.

### Open hardware to learn from (license-compatible)
- **`devbisme/RPi_Hat_Template`** (GitHub) — KiCad template with correct EEPROM circuit, 40-pin header, mounting holes, HAT+ outline. **Start here.**
- **`KiCad/kicad-templates/raspberrypi_hat`** — alternative starter template
- **`vroland/epdiy` and `vroland/epdiy-hardware`** (GitHub) — CC-BY-SA. Reference *only* for ESP32-S3 USB-C charging circuits, RTC integration, and JLCPCB-ready repository structure (Makefile-driven CI generates gerbers/BOM/placement). Architecturally wrong for the panel interface.
- **`SolderedElectronics/Inkplate-6-hardware` etc.** (GitHub) — open KiCad sources for production-quality e-paper PCBs. Reference for ESP32 power management. Same caveat — wrong panel interface.
- **`pimoroni/inky`** (GitHub, MIT) — Python driver. Read the EEPROM detection logic in `inky/eeprom.py` to understand what bytes our HAT must write into the 24LC* EEPROM for `inky` to auto-detect us as a Spectra 6 7.3" or 13.3".

### Build logs
- **`protivinsky/photoink`** (GitHub) — FireBeetle + GDEP073E01 + DESPI-C73 photo frame. Confirms 8-pin breakout works in practice. Pin assignments documented.
- **`Duocervisia/e-paper-esp32-frame`** (GitHub) — similar ESP32 build, with a useful note about cutting the FireBeetle low-power solder jumper.

### Connectors (KiCad library hits)
- 50-pin 0.5mm pitch FPC, top contact: **Hirose FH12-50S-0.5SH** — KiCad standard library has it as `Connector_FFC-FPC:Hirose_FH12-50S-0.5SH_*`. LCSC C82474.
- 60-pin 0.5mm pitch FPC for 13.3": Hirose FH12-60S-0.5SH or equivalent. KiCad library covers it; LCSC has stock.
- 24LC256 EEPROM in SOT-23 or SO-8 — pick whichever has best JLCPCB basic-parts availability at design time

---

## Architecture

### PCB family overview

We're building **two PCB variants** that share as much as possible:

```
spectra6-hat-7in3/    ← 7.3" GDEP073E01, 50-pin FPC, SPI
spectra6-hat-13in3/   ← 13.3" GDEP133C02, 60-pin FPC, QSPI
shared/               ← KiCad symbol/footprint libraries used by both
```

The shared block is the Pi HAT side — 40-pin header, EEPROM, mounting holes, optional power section, optional STEMMA QT, optional buttons. The differences are:

| | 7.3" variant | 13.3" variant |
|---|---|---|
| Panel | Good Display GDEP073E01 (800×480) | Good Display GDEP133C02 (1600×1200) |
| Connector | 50-pin 0.5mm FPC | 60-pin 0.5mm FPC |
| Bus | 4-wire SPI | QSPI (4 data lines) |
| PCB outline | ~174 × 123 mm (matches Pimoroni 7.3" for Ikea 180×130 frames) | ~297 × 210 mm (A4) |
| Refresh time | ~20–25 s | ~19 s (vendor) — confirm in testing |
| Layers | 2-layer should suffice | 4-layer recommended due to QSPI clock integrity |
| Boost circuit | Small (a few caps + inductor) per DESPI-C73 | Confirm against Waveshare 13.3" schematic; may need slightly more capacitance |

**Decision:** Phase 1 builds the 7.3" variant only. 13.3" is Phase 2 once the 7.3" boots and runs Pimoroni `inky` end-to-end. Don't bring up both at once.

### Block diagram (7.3" variant)

```
  ┌────────────────────────────────────────────────┐
  │           Raspberry Pi Zero 2 W                │
  │           (mounted under HAT)                  │
  └────────────────┬───────────────────────────────┘
                   │ 40-pin GPIO header
  ┌────────────────┴───────────────────────────────┐
  │                                                │
  │   ┌──────────────┐    ┌────────────────────┐   │
  │   │   24LC256    │    │  Optional: LiPo +  │   │
  │   │   EEPROM     │    │  Witty-Pi-style    │   │
  │   │  (HAT spec)  │    │  power management  │   │
  │   │   on I²C     │    │  (Phase 3)         │   │
  │   └──────────────┘    └────────────────────┘   │
  │                                                │
  │   ┌──────────────┐    ┌────────────────────┐   │
  │   │ Boost +      │    │  4× user buttons   │   │
  │   │ decoupling   │    │  (rear-mounted,    │   │
  │   │ for panel    │    │  Pimoroni-style)   │   │
  │   │ V_DD rail    │    │                    │   │
  │   └──────┬───────┘    └────────────────────┘   │
  │          │                                     │
  │   ┌──────┴───────────────────────────────┐     │
  │   │  50-pin 0.5mm FPC                    │     │
  │   │  (Hirose FH12-50S-0.5SH)             │     │
  │   └──────────────────────────────────────┘     │
  │                                                │
  │   2× STEMMA QT (Qw/ST) connectors on I²C       │
  └────────────────────────────────────────────────┘
                   │
                   │ FPC cable
  ┌────────────────┴───────────────────────────────┐
  │   GDEP073E01 7.3" Spectra 6 panel              │
  └────────────────────────────────────────────────┘
```

### Pi GPIO assignment (7.3" variant, follow Pimoroni Inky Impression for `inky` compatibility)

| Pi GPIO | BCM pin | Function | Notes |
|---|---|---|---|
| GPIO 8 | physical 24 | SPI0 CE0 (panel CS) | `inky` default |
| GPIO 11 | physical 23 | SPI0 SCLK | |
| GPIO 10 | physical 19 | SPI0 MOSI | |
| GPIO 22 | physical 15 | Panel D/C | |
| GPIO 27 | physical 13 | Panel RESET | |
| GPIO 17 | physical 11 | Panel BUSY (input) | |
| GPIO 2 | physical 3 | I²C SDA (EEPROM + STEMMA QT) | |
| GPIO 3 | physical 5 | I²C SCL (EEPROM + STEMMA QT) | |
| GPIO 5 | physical 29 | Button A | rear-mounted |
| GPIO 6 | physical 31 | Button B | |
| GPIO 16 | physical 36 | Button C | |
| GPIO 24 | physical 18 | Button D | |
| GPIO 0 | physical 27 | EEPROM SDA (HAT spec) | reserved per HAT spec — connect to the 24LC256 SDA only |
| GPIO 1 | physical 28 | EEPROM SCL (HAT spec) | reserved per HAT spec — connect to the 24LC256 SCL only |

**Watch out:** The HAT spec dedicates GPIO 0/1 as ID_SD/ID_SC for the EEPROM and *prohibits* anything else on those pins. The user-side I²C (for STEMMA QT) goes on GPIO 2/3.

### EEPROM contents

The Pimoroni `inky` library reads the EEPROM at I²C address 0x50 to identify the board. We want it to detect us as a Spectra 6 — the simplest path is to mimic the byte layout `pimoroni/inky` already knows about. Read `inky/eeprom.py` and `inky/_inky_impression.py` for the exact magic. Store: width (800 or 1600), height (480 or 1200), color profile (Spectra 6 = `7C` per Pimoroni's enum), PCB version, display variant.

We will *not* claim Pimoroni's vendor ID. We will set our own vendor string and trust the `inky` library to dispatch on the color/resolution fields.

---

## Bill of materials (initial estimate, 7.3" variant)

Costs are 1-off prototype, sourced JLCPCB basic parts where possible. Update once design is finalized.

| Item | Qty | Unit | Notes |
|---|---|---|---|
| GDEP073E01 7.3" Spectra 6 panel | 1 | ~$45 | from Good Display official AliExpress or buyepaper.com |
| Hirose FH12-50S-0.5SH | 1 | ~$2 | LCSC C82474 |
| 24LC256-I/SN EEPROM | 1 | ~$0.40 | LCSC C12064, address 0x50 |
| 2×20 pin 2.54mm female header | 1 | ~$0.50 | the Pi-side socket |
| Boost components per DESPI-C73 | ~10 | ~$1 | small inductor, ceramic caps, switching IC — copy values from PDF |
| 4× tactile buttons | 4 | $0.40 | rear-mounted SMD |
| 2× STEMMA QT JST-SH 4-pin | 2 | $1 | optional |
| PCB (JLCPCB 2-layer, 5pcs) | 1 | ~$8 | 174×123mm is in the cheap tier |
| **Estimated total** | | **~$60** | excluding panel, ~$15 for the HAT itself |

For comparison: Pimoroni Inky Impression 7.3" is ~$84 fully assembled. Our DIY HAT lands at ~$60 BOM but obviously requires assembly time. Three units batched would land closer to ~$50/unit including spare PCBs.

---

## Project layout

```
.
├── AGENTS.md                       ← this file
├── README.md                       ← public-facing project description
├── LICENSE                         ← CC-BY-SA-4.0 for hardware, MIT for any code
├── kicad/
│   ├── shared/                     ← symbol & footprint libraries
│   │   ├── shared.kicad_sym
│   │   └── shared.pretty/
│   ├── spectra6-hat-7in3/          ← Phase 1
│   │   ├── spectra6-hat-7in3.kicad_pro
│   │   ├── spectra6-hat-7in3.kicad_sch
│   │   ├── spectra6-hat-7in3.kicad_pcb
│   │   └── outputs/                ← gerbers, BOM CSV, placement CSV (CI-generated, gitignored)
│   └── spectra6-hat-13in3/         ← Phase 2 (placeholder until 7.3" works)
├── firmware/
│   ├── eeprom-flash/               ← Python scripts to program the 24LC256 over I²C
│   └── test-images/                ← dithered test patterns, color bars
├── enclosure/
│   ├── frame-7in3.scad             ← OpenSCAD source
│   └── exports/                    ← STLs sliced for Bambu P1S
├── docs/
│   ├── pinout.md
│   ├── eeprom-format.md
│   ├── boot-time-tuning.md         ← Pi Zero 2 W boot optimization for power-cycling
│   └── home-assistant-integration.md
└── reference/
    ├── despi-c73-schematic.pdf     ← Good Display reference, downloaded
    ├── gdep073e01-datasheet.pdf
    ├── gdep133c02-datasheet.pdf
    ├── waveshare-13in3-hat-plus-schematic.pdf
    └── e-ink-spectra-6-design-notice.pdf
```

---

## Phased plan

### Phase 0 — Setup and reference gathering (do first)
- [x] Clone/import `devbisme/RPi_Hat_Template` assets and confirm the starter project parses with KiCad CLI
- [x] Download Phase 1 PDFs/pages into `reference/` and generate `reference/SHA256SUMS`
- [x] Read `pimoroni/inky/inky/eeprom.py` and document the byte layout in `docs/eeprom-format.md`
- [ ] Confirm panel availability and shipping window from Good Display to Singapore
- [ ] Decide final KiCad version for collaborators. Local CLI is 10.0.1; original plan assumed 8 or 9.

### Phase 1 — 7.3" HAT
- [ ] Capture schematic from DESPI-C73 PDF as KiCad source. Prep notes exist in `docs/schematic-capture-notes.md` and the KiCad starter schematic.
- [ ] Add HAT EEPROM (24LC256 on GPIO 0/1) per HAT spec
- [ ] Add 4 buttons + 2 STEMMA QT
- [ ] Lay out PCB at ~174×123mm to fit Ikea 180×130 frame. Placeholder outline exists.
- [ ] DRC clean against JLCPCB 2-layer constraints (clearance 5/5 mil minimum). Prep-shell DRC passes only because the real layout is not captured yet.
- [ ] Export gerbers + BOM + placement, order 5 from JLCPCB. Prep-shell gerber/drill export works; BOM and placement remain blocked until schematic/layout capture.
- [ ] Hand-assemble 1 prototype
- [ ] Bring up: confirm panel powers, runs `inky` example, shows test image
- [ ] Write EEPROM via Python script; confirm `inky` auto-detects
- [x] Document Phase 0 decisions and Phase 1 prep status in `docs/`

### Phase 2 — 13.3" HAT
- [ ] Capture 13.3" schematic from Waveshare HAT+ PDF
- [ ] 4-layer PCB for QSPI signal integrity
- [ ] Confirm A4 outline (297×210 mm) — JLCPCB tier is more expensive at this size
- [ ] Bring up against Pimoroni Inky Impression 13.3" pinout for `inky` compatibility
- [ ] Same EEPROM detection flow

### Phase 3 — Battery + power-cycling (optional, after both panels work)
- [ ] Add LiPo connector + TP4056 charger or similar
- [ ] Add an external RTC + power-gate MCU (ATtiny85 or RP2040) modeled on Witty Pi 4 L3V7
- [ ] OR design carrier so PiSugar 3 mounts on the back
- [ ] Boot-time tuning for Pi Zero 2 W: target sub-15-second boot from cold

### Phase 4 — Enclosure and HA integration
- [ ] OpenSCAD enclosure with magnetic mount, designed for Bambu P1S
- [ ] Sample ESPHome and Pi Python configs for displaying HA Lovelace screenshots
- [ ] Integration with Immich, Google Photos, or HA `media_source`

---

## Coding/design conventions for Codex

When working on this project:

1. **Open the relevant SKILL.md first.** If creating PCB outputs, gerbers, or working with KiCad files, check what skills are available. There is no built-in skill for KiCad as of writing — proceed carefully and have me check the schematic before any PCB layout work.
2. **Never push designs without DRC clean.** Treat DRC errors as build failures.
3. **For schematic capture from a PDF reference:** Recreate the schematic faithfully but call out any deviation as a comment/text annotation on the schematic itself, not just in commit messages.
4. **All numeric values come from the datasheet, not from "common values for similar circuits."** If a capacitor's value isn't specified in DESPI-C73 or the panel datasheet, flag it and ask before guessing.
5. **Use the kicad-cli for export and CI.** Don't rely on GUI-only operations for repeatable artifacts. Generate gerbers, drill files, BOM CSV, and placement CSV from the command line so JLCPCB orders are reproducible.
6. **Component selection priority:** JLCPCB Basic Parts > JLCPCB Extended Parts (assembly cost ladder matters even if we hand-assemble) > LCSC stocked > Digikey/Mouser. Avoid no-stock parts even if "perfect" on paper.
7. **Keep the panel on a removable cable.** The panel is fragile and expensive. Never solder it directly. Always FPC connector on the HAT.
8. **For firmware/scripts, target Python 3.11+ and the `pimoroni/inky` library version pinned in `pyproject.toml`.** Do not fork `inky`; if changes are needed, propose them upstream and patch locally with a documented diff.
9. **License and attribution:** Hardware files under CC-BY-SA-4.0 (matches EPDiy and Inkplate convention). Code under MIT. Any image dithering tools or scripts borrowed from `pimoroni/inky` retain their MIT license and original copyright headers.

---

## Open questions to resolve

These need a human decision before proceeding past Phase 1 schematic:

- [ ] **Boost circuit IC choice** — DESPI-C73 uses an unmarked small switcher. Identify the part from the PDF schematic and pick a JLCPCB-stocked equivalent (likely a TPS61040 or similar). Confirm 3.3V → ~5–6V intermediate rail, ~50mA peak.
- [ ] **EEPROM I²C address conflict?** — HAT spec puts EEPROM on dedicated GPIO 0/1 lines, separate from the user I²C bus on GPIO 2/3. Confirm Pimoroni's `inky` library reads from the dedicated HAT EEPROM bus (`/sys/firmware/devicetree/base/hat/`) rather than user-bus I²C 0x50. **This affects whether STEMMA QT works alongside `inky` auto-detect.**
- [ ] **Buttons: side or rear?** — Pimoroni shifted from side to rear in Nov 2025 due to transit damage. Rear is mechanically better but requires deeper enclosure clearance.
- [ ] **Single PCB or two-board (carrier + adapter)?** — Two-board lets the same Pi-side carrier serve both panel sizes, with cheap swappable FPC adapters. One-board is simpler but means two distinct designs. Lean toward two-board for the second panel to halve future design work.
- [ ] **24-hour refresh enforcement** — Spectra 6 panels require a refresh at least every 24 hours per Good Display's design notice. Should this be enforced by a cron job on the Pi or by hardware (an MCU watchdog)? Cron is simpler. If we go battery + power-cycle, the wake-up scheduler handles it naturally.

---

## Quick command reference

```bash
# Clone and bootstrap
git clone https://github.com/<your-org>/spectra6-hat
cd spectra6-hat
git submodule update --init --recursive   # for any KiCad library submodules

# KiCad CLI export (Phase 1)
kicad-cli sch export pdf kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_sch \
    -o docs/schematic-7in3.pdf

kicad-cli pcb export gerbers kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_pcb \
    -o kicad/spectra6-hat-7in3/outputs/gerbers/

kicad-cli pcb export drill kicad/spectra6-hat-7in3/spectra6-hat-7in3.kicad_pcb \
    -o kicad/spectra6-hat-7in3/outputs/gerbers/ \
    --excellon-separate-th

# Zip for JLCPCB
cd kicad/spectra6-hat-7in3/outputs
zip -r jlcpcb-upload.zip gerbers/

# Flash EEPROM (run on the Pi after assembling the HAT)
cd firmware/eeprom-flash
sudo python3 flash_eeprom.py --variant 7in3 --version 1.0
```

---

## Glossary

- **HAT / HAT+** — Raspberry Pi's specification for add-on boards. HAT+ is the newer 2024 spec used by Pi 5 and modern HATs; backward compatible with older Pis.
- **FPC** — Flexible Printed Circuit, the ribbon cable terminating the e-paper panel.
- **Spectra 6 / E6** — E Ink's six-color (black, white, red, yellow, blue, green) electrophoretic display tech, launched 2023.
- **DESPI-C73** — Good Display's reference adapter board for the 7.3" Spectra 6 panel. Used here as schematic source.
- **Inky / Inky Impression** — Pimoroni's line of color e-paper Pi HATs. `pimoroni/inky` is their open-source Python driver. Our HAT aims to be drop-in compatible.
- **EEPROM (in HAT context)** — A small I²C flash chip on a HAT that the Pi reads at boot to identify the board (per the HAT spec).
- **Integrated-controller panel** — An e-paper panel with the timing controller and high-voltage drivers built into the panel's COG/TAB. The MCU only needs to send SPI/QSPI commands; no external TPS65185-class PMIC. Both Spectra 6 panels we target are this type.

---

## End of context

If this file feels out of date with reality on the ground, fix it before proceeding. The next person reading it (probably future-you with Codex) will thank you.
