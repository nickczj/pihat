#!/usr/bin/env python3
"""Write Pimoroni `inky` display identity data to the bus-1 EEPROM."""

from __future__ import annotations

import argparse
import datetime as _datetime
import struct
import sys
import time
from dataclasses import dataclass


EEPROM_FORMAT = "<HHBBB22p"
EEPROM_LENGTH = struct.calcsize(EEPROM_FORMAT)
DEFAULT_ADDRESS = 0x50
DEFAULT_BUS = 1


@dataclass(frozen=True)
class DisplayConfig:
    """Static display identity values understood by Pimoroni `inky`."""

    name: str
    width: int
    height: int
    color: int
    display_variant: int
    description: str


@dataclass(frozen=True)
class EPDRecord:
    """Decoded EEPROM payload."""

    width: int
    height: int
    color: int
    pcb_variant: int
    display_variant: int
    write_time: str


VARIANTS: dict[str, DisplayConfig] = {
    "7in3": DisplayConfig(
        "7in3",
        width=800,
        height=480,
        color=6,
        display_variant=22,
        description="Spectra 6 7.3 inch 800x480 E673",
    ),
    "7in3-ac": DisplayConfig(
        "7in3-ac",
        width=800,
        height=480,
        color=6,
        display_variant=26,
        description="Spectra 6 7.3 inch 800x480 E673 AC",
    ),
    "13in3": DisplayConfig(
        "13in3",
        width=1600,
        height=1200,
        color=6,
        display_variant=21,
        description="Spectra 6 13.3 inch 1600x1200 EL133UF1",
    ),
    "13in3-ac": DisplayConfig(
        "13in3-ac",
        width=1600,
        height=1200,
        color=6,
        display_variant=27,
        description="Spectra 6 13.3 inch 1600x1200 EL133UF1 AC",
    ),
}


def parse_int_auto(value: str) -> int:
    """Parse decimal or 0x-prefixed integer CLI values."""

    return int(value, 0)


def parse_pcb_version(value: str) -> int:
    """Encode a human PCB version as Pimoroni's one-byte pcb_variant field.

    `1.0` becomes `10`, `1.2` becomes `12`, and raw encoded values such as
    `10` are also accepted.
    """

    text = value.strip()
    if not text:
        raise argparse.ArgumentTypeError("version must not be empty")

    try:
        if "." in text:
            major_text, minor_text = text.split(".", 1)
            if not major_text.isdigit() or not minor_text.isdigit():
                raise ValueError
            if len(minor_text) != 1:
                raise argparse.ArgumentTypeError(
                    "version must use one decimal place, for example 1.0"
                )
            encoded = int(major_text) * 10 + int(minor_text)
        else:
            encoded = int(text, 0)
            if encoded < 10:
                encoded *= 10
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid PCB version: {value!r}") from exc

    if not 0 <= encoded <= 255:
        raise argparse.ArgumentTypeError("encoded PCB version must fit in one byte")
    return encoded


def encode_epd_type(
    config: DisplayConfig,
    pcb_variant: int,
    write_time: str | None = None,
) -> bytes:
    """Encode the 29-byte Pimoroni EPDType structure."""

    timestamp = write_time
    if timestamp is None:
        timestamp = str(_datetime.datetime.now())

    return struct.pack(
        EEPROM_FORMAT,
        config.width,
        config.height,
        config.color,
        pcb_variant,
        config.display_variant,
        timestamp.encode("ascii"),
    )


def decode_epd_type(data: bytes | bytearray) -> EPDRecord:
    """Decode a Pimoroni EPDType payload."""

    if len(data) != EEPROM_LENGTH:
        raise ValueError(f"expected {EEPROM_LENGTH} bytes, got {len(data)}")

    width, height, color, pcb_variant, display_variant, write_time = struct.unpack(
        EEPROM_FORMAT, data
    )
    return EPDRecord(
        width=width,
        height=height,
        color=color,
        pcb_variant=pcb_variant,
        display_variant=display_variant,
        write_time=write_time.decode("ascii", errors="replace"),
    )


def hexdump(data: bytes) -> str:
    """Return a compact hex representation."""

    return " ".join(f"{byte:02x}" for byte in data)


def _address_prefix(offset: int, address_width: int) -> bytes:
    if address_width not in (8, 16):
        raise ValueError("address_width must be 8 or 16")
    return offset.to_bytes(address_width // 8, "big")


def write_i2c_eeprom(
    data: bytes,
    *,
    bus_number: int,
    device_address: int,
    offset: int,
    address_width: int,
    page_size: int = 16,
    write_delay: float = 0.01,
) -> None:
    """Write bytes to an I2C EEPROM using smbus2 raw messages."""

    from smbus2 import SMBus, i2c_msg

    with SMBus(bus_number) as bus:
        for chunk_offset in range(0, len(data), page_size):
            chunk = data[chunk_offset : chunk_offset + page_size]
            memory_offset = offset + chunk_offset
            payload = _address_prefix(memory_offset, address_width) + chunk
            bus.i2c_rdwr(i2c_msg.write(device_address, payload))
            time.sleep(write_delay)


def read_i2c_eeprom(
    length: int,
    *,
    bus_number: int,
    device_address: int,
    offset: int,
    address_width: int,
) -> bytes:
    """Read bytes from an I2C EEPROM using smbus2 raw messages."""

    from smbus2 import SMBus, i2c_msg

    with SMBus(bus_number) as bus:
        set_offset = i2c_msg.write(device_address, _address_prefix(offset, address_width))
        read_data = i2c_msg.read(device_address, length)
        bus.i2c_rdwr(set_offset, read_data)
        return bytes(read_data)


def describe_record(record: EPDRecord) -> str:
    """Format decoded EEPROM data for humans."""

    return "\n".join(
        [
            f"width={record.width}",
            f"height={record.height}",
            f"color={record.color}",
            f"pcb_variant={record.pcb_variant}",
            f"display_variant={record.display_variant}",
            f"write_time={record.write_time}",
        ]
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", default="7in3", choices=sorted(VARIANTS))
    parser.add_argument("--version", default="1.0", type=parse_pcb_version)
    parser.add_argument("--bus", default=DEFAULT_BUS, type=parse_int_auto)
    parser.add_argument("--address", default=DEFAULT_ADDRESS, type=parse_int_auto)
    parser.add_argument("--offset", default=0, type=parse_int_auto)
    parser.add_argument("--address-width", default=16, type=int, choices=(8, 16))
    parser.add_argument("--dry-run", action="store_true", help="print bytes but do not write")
    parser.add_argument("--read-back", action="store_true", help="read back and decode after writing")
    parser.add_argument("--yes", action="store_true", help="skip interactive write confirmation")
    parser.add_argument(
        "--time",
        default=None,
        help="override write_time string, mainly for reproducible tests",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    config = VARIANTS[args.variant]
    payload = encode_epd_type(config, args.version, write_time=args.time)
    record = decode_epd_type(payload)

    print(f"Variant: {config.name} ({config.description})")
    print(describe_record(record))
    print(f"bytes[{len(payload)}]: {hexdump(payload)}")

    if args.dry_run:
        print("Dry run only; EEPROM was not written.")
        return 0

    if not args.yes:
        if not sys.stdin.isatty():
            raise SystemExit("Refusing non-interactive write without --yes.")
        answer = input(
            f"Write {len(payload)} bytes to I2C bus {args.bus}, "
            f"address 0x{args.address:02x}, offset {args.offset}? [y/N] "
        )
        if answer.strip().lower() not in {"y", "yes"}:
            print("Aborted.")
            return 1

    write_i2c_eeprom(
        payload,
        bus_number=args.bus,
        device_address=args.address,
        offset=args.offset,
        address_width=args.address_width,
    )
    print("Write complete.")

    if args.read_back:
        read_data = read_i2c_eeprom(
            EEPROM_LENGTH,
            bus_number=args.bus,
            device_address=args.address,
            offset=args.offset,
            address_width=args.address_width,
        )
        print("Read-back:")
        print(describe_record(decode_epd_type(read_data)))
        if read_data != payload:
            raise SystemExit("Read-back does not match written payload.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

