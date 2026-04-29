# Home Assistant Integration

Home Assistant support is Phase 4. Phase 1 only needs to keep the display API simple enough that later integrations can render an image and refresh.

Likely paths:

- Pull a pre-rendered dashboard screenshot from Home Assistant.
- Use Home Assistant `media_source` or a local Python script to pick image content.
- Refresh on a systemd timer while respecting the 24-hour Spectra 6 retention guidance.

Do not add Home Assistant-specific GPIO, power, or connector decisions to Phase 1 unless the display bring-up proves they are necessary.

