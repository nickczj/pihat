# EEPROM Flash Tools

`flash_eeprom.py` writes the Pimoroni-compatible display EEPROM on Raspberry Pi I2C bus 1 at address `0x50`.

Dry-run the Phase 1 payload:

```bash
python3 flash_eeprom.py --variant 7in3 --version 1.0 --dry-run
```

Write and read back on a Raspberry Pi:

```bash
sudo python3 flash_eeprom.py --variant 7in3 --version 1.0 --read-back
```

The script defaults to 16-bit EEPROM memory addressing for 24LC256-class parts. Use `--address-width 8` only if the hardware revision intentionally swaps to a smaller 8-bit-addressed EEPROM.

HAT+ ID EEPROM material is under `hatplus/` and should be built with Raspberry Pi `utils/eeptools`, not with this script.

