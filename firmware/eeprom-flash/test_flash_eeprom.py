import argparse
import struct
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import flash_eeprom  # noqa: E402


class EepromEncodingTests(unittest.TestCase):
    def test_pimoroni_struct_is_29_bytes(self):
        self.assertEqual(flash_eeprom.EEPROM_LENGTH, 29)

    def test_7in3_default_payload(self):
        payload = flash_eeprom.encode_epd_type(
            flash_eeprom.VARIANTS["7in3"],
            pcb_variant=10,
            write_time="2026-04-28 12:34:56",
        )
        self.assertEqual(len(payload), 29)
        unpacked = struct.unpack(flash_eeprom.EEPROM_FORMAT, payload)
        self.assertEqual(unpacked[:5], (800, 480, 6, 10, 22))
        self.assertEqual(unpacked[5], b"2026-04-28 12:34:56")

    def test_7in3_ac_override_payload(self):
        payload = flash_eeprom.encode_epd_type(
            flash_eeprom.VARIANTS["7in3-ac"],
            pcb_variant=10,
            write_time="2026-04-28 12:34:56",
        )
        record = flash_eeprom.decode_epd_type(payload)
        self.assertEqual(record.display_variant, 26)

    def test_13in3_future_payloads(self):
        normal = flash_eeprom.decode_epd_type(
            flash_eeprom.encode_epd_type(
                flash_eeprom.VARIANTS["13in3"],
                pcb_variant=10,
                write_time="2026-04-28 12:34:56",
            )
        )
        ac = flash_eeprom.decode_epd_type(
            flash_eeprom.encode_epd_type(
                flash_eeprom.VARIANTS["13in3-ac"],
                pcb_variant=10,
                write_time="2026-04-28 12:34:56",
            )
        )
        self.assertEqual((normal.width, normal.height, normal.color), (1600, 1200, 6))
        self.assertEqual(normal.display_variant, 21)
        self.assertEqual(ac.display_variant, 27)

    def test_parse_pcb_version(self):
        self.assertEqual(flash_eeprom.parse_pcb_version("1.0"), 10)
        self.assertEqual(flash_eeprom.parse_pcb_version("1.2"), 12)
        self.assertEqual(flash_eeprom.parse_pcb_version("10"), 10)
        self.assertEqual(flash_eeprom.parse_pcb_version("0x0a"), 10)
        with self.assertRaises(argparse.ArgumentTypeError):
            flash_eeprom.parse_pcb_version("1.23")

    def test_address_prefix(self):
        self.assertEqual(flash_eeprom._address_prefix(0x1234, 16), b"\x12\x34")
        self.assertEqual(flash_eeprom._address_prefix(0x34, 8), b"\x34")


if __name__ == "__main__":
    unittest.main()

