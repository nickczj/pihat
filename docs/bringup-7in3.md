# 7.3 Inch Bring-Up

Do not insert the e-paper panel until power rails and connector orientation have been checked.

## Pre-Power Inspection

1. Check FPC connector orientation against the panel cable and the DESPI-C73 reference.
2. Confirm there are no shorts between `3V3` and `GND`.
3. Confirm HAT+ ID pins GPIO0/GPIO1 connect only to the HAT+ ID EEPROM and pull-ups.
4. Confirm the `inky` EEPROM is on GPIO2/GPIO3 at `0x50`.
5. Confirm the button nets are not shorted to panel chip-select or reset nets.

## Power Without Panel

1. Boot the Pi with the HAT installed and no panel inserted.
2. Measure 3.3 V at the FPC supply pins.
3. Probe DESPI-C73-derived boost/test rails only where the reference schematic provides test points.
4. Verify the `inky` EEPROM appears on bus 1:

```bash
sudo i2cdetect -y 1
python3 firmware/eeprom-flash/flash_eeprom.py --variant 7in3 --version 1.0 --dry-run
```

## EEPROM Programming

Write the `inky` EEPROM after the board passes power checks:

```bash
sudo python3 firmware/eeprom-flash/flash_eeprom.py --variant 7in3 --version 1.0 --read-back
```

Then verify Pimoroni auto-detection:

```bash
python3 - <<'PY'
from inky.auto import auto
display = auto()
print(display)
PY
```

## Panel Test

1. Power down fully before inserting the FPC.
2. Insert and latch the FPC without bending the cable sharply.
3. Boot and run Pimoroni identify/stripes/image examples.
4. Confirm refresh completes and the BUSY line returns to idle.
5. Confirm the display is left in sleep/no-long-HV state after refresh.

## Operational Requirement

Spectra 6 panels require at least one full refresh every 24 hours to reduce retention risk. Phase 1 enforces that in software with a timer/cron job, not with a hardware watchdog.

Template systemd units are in `firmware/systemd/`. Install them only after replacing the placeholder refresh script path with the real image-refresh command.
