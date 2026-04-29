# HAT+ ID EEPROM

This directory is for the Raspberry Pi HAT+ ID EEPROM, which is separate from the Pimoroni-compatible `inky` EEPROM.

Use the official Raspberry Pi `utils/eeptools` flow:

```bash
git clone https://github.com/raspberrypi/utils.git
cd utils/eeptools
make
./eepmake /path/to/spectra6-hat-7in3.eep.txt /tmp/spectra6-hat-7in3.eep
sudo ./eepflash.sh -w -f=/tmp/spectra6-hat-7in3.eep -t=24c256
./eepdump /tmp/spectra6-hat-7in3.eep
```

The template file here is a placeholder until product IDs, UUID policy, and device-tree overlay contents are finalized.

