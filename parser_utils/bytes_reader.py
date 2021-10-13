from typing import BinaryIO
import struct


def read_bytes_display(file: BinaryIO, count: int) -> str:
    return " ".join(f"{x:02x}" for x in file.read(count))


def read_int32(file: BinaryIO) -> int:
    return struct.unpack("<I", file.read(4))[0]


def read_int8(file: BinaryIO) -> int:
    return ord(struct.unpack("<c", file.read(1))[0])


def read_float(file: BinaryIO) -> float:
    return struct.unpack("<f", file.read(4))[0]


def read_str(file: BinaryIO, count: int) -> bytes:
    return file.read(count)


def read_ascii(file: BinaryIO, count:int) -> str:
    return file.read(count).decode("ascii")
