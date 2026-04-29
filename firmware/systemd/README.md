# Systemd Refresh Timer

Phase 1 enforces the Spectra 6 24-hour refresh requirement in software.

These units are templates. Install them on the Raspberry Pi after adding the real refresh script at `/opt/spectra6-pihat/refresh_once.py` or adjusting `ExecStart`.

```bash
sudo cp spectra6-refresh.service spectra6-refresh.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now spectra6-refresh.timer
systemctl list-timers spectra6-refresh.timer
```

