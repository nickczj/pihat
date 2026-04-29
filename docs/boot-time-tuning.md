# Boot-Time Tuning

Battery and power-cycling are Phase 3. These notes exist so Phase 1 does not block later low-power work.

Targets:

- Keep the Pi Zero 2 W able to boot, refresh, and shut down without a desktop session.
- Aim for sub-15-second boot only after the display path works.
- Prefer a systemd timer or cron job for the 24-hour Spectra 6 refresh requirement in Phase 1.

Initial software direction:

1. Use Raspberry Pi OS Lite.
2. Disable unnecessary services after measuring boot time.
3. Run a single refresh service that exits after the display sleeps.
4. Defer hard power gating to Phase 3 hardware.

