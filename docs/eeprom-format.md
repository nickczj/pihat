# EEPROM Format

This project uses two different EEPROM contents.

## Pimoroni `inky` EEPROM

Pimoroni `inky` reads display identity from I2C bus 1 at address `0x50`, not from the Raspberry Pi HAT ID EEPROM bus. The current structure is 29 bytes:

```python
struct.pack("<HHBBB22p", width, height, color, pcb_variant, display_variant, write_time)
```

| Field | Size | Phase 1 value |
|---|---:|---|
| `width` | 2 bytes little-endian | `800` |
| `height` | 2 bytes little-endian | `480` |
| `color` | 1 byte | `6` (`spectra6`) |
| `pcb_variant` | 1 byte | PCB version times ten, for example `10` for `1.0` |
| `display_variant` | 1 byte | `22` for Spectra 6 7.3 inch E673; `26` is the AC override |
| `write_time` | 22-byte Pascal string | Timestamp, truncated by the upstream format |

Future 13.3 inch defaults are `1600`, `1200`, color `6`, display variant `21`, with `27` as the AC override.

Use:

```bash
python3 firmware/eeprom-flash/flash_eeprom.py --variant 7in3 --version 1.0 --dry-run
sudo python3 firmware/eeprom-flash/flash_eeprom.py --variant 7in3 --version 1.0 --read-back
```

The script writes the first 29 bytes of the EEPROM. Its default addressing mode is 16-bit memory addressing, suitable for 24LC256-class EEPROMs.

## HAT+ ID EEPROM

The HAT+ ID EEPROM is separate and lives only on GPIO0/GPIO1. Build it with the official Raspberry Pi `utils/eeptools` flow. The template in `firmware/eeprom-flash/hatplus/` is intentionally minimal until a real vendor/product ID and overlay are chosen.

Validation on a Raspberry Pi:

```bash
sudo ./eepmake spectra6-hat-7in3.eep.txt spectra6-hat-7in3.eep
sudo ./eepflash.sh -w -f=spectra6-hat-7in3.eep -t=24c256
sudo ./eepdump spectra6-hat-7in3.eep
```

Do not bridge or reuse the HAT+ ID pins for Qw/ST, the display EEPROM, buttons, or panel control signals.

