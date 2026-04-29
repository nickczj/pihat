# Spectra 6 HAT 13.3 Phase 2 Placeholder

Do not start layout here until the 7.3 inch board has completed bring-up.

Captured Phase 2 decisions live in `docs/phase2-13in3-notes.md`.

Current compatibility note: Pimoroni `inky` uses dual-CS SPI for the 13.3 inch Spectra 6 driver, with GPIO26 and GPIO16 as chip-selects. Do not assume a Linux QSPI interface without explicitly changing the software target.

