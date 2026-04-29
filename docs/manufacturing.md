# Manufacturing and Export

Phase 1 targets a low-cost 2-layer prototype process first. Do not order boards until KiCad ERC and DRC are clean.

## Local Prerequisites

- KiCad. The current local CLI is KiCad `10.0.1`.
- `kicad-cli`; on this Mac it is at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.
- Manufacturer rules configured for the intended order. Initial JLCPCB target is 5/5 mil minimum track/clearance.

The `Makefile` defaults `KICAD_CLI` to the local macOS app path. Override it if needed:

```bash
make kicad-version
make kicad-erc KICAD_CLI=/path/to/kicad-cli
```

## Checks

```bash
make kicad-version
make kicad-erc
make kicad-drc
```

Expected output files:

- `kicad/spectra6-hat-7in3/outputs/erc.rpt`
- `kicad/spectra6-hat-7in3/outputs/drc.rpt`

## Fabrication Export

```bash
make kicad-export
```

Expected generated artifacts:

- `docs/schematic-7in3.pdf`
- `kicad/spectra6-hat-7in3/outputs/gerbers/`
- Excellon drill files under the gerber output directory.

Before ordering, also export:

- BOM CSV with manufacturer/LCSC fields populated.
- Position CSV for SMT assembly, if used.
- Assembly drawing PDF.

## Last Prep-Shell Validation

Run date: 2026-04-29.

| Check | Result |
|---|---|
| `kicad-cli version` | `10.0.1` |
| Schematic ERC on prep sheet | 0 violations |
| PCB DRC on outline placeholder | 0 violations, 0 unconnected items |
| Schematic PDF export | Completed |
| Gerber export | Completed for the placeholder PCB |
| Drill export | Completed for the placeholder PCB |

These results only prove the starter files are syntactically usable and exportable. They do not validate the final circuit because the real schematic and layout have not been captured yet.

## Current Blockers

- The KiCad schematic shell is not yet a completed circuit.
- Exact component ordering data still needs JLCPCB/LCSC availability review.
- The exact Good Display 13.3 inch datasheet is pending; Phase 2 uses the Waveshare schematic/manual and a Seeed module datasheet only as cross-checks.
