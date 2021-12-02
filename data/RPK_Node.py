from data.IRPKTreeNode import IRPKTreeNode
import struct
from parser_utils.bytes_reader import *
from data.Resource_Node import ResourceNode

"""
Top of the node hierarchy representing a single RPK file. Handles 
reading/writing from a bytesio

@author MrNo
"""

# constant for use in file.seek() operations
SEEK_CUR = 1


class RPK_Node(IRPKTreeNode):

    known_config_flags = {"\x13", "\x14", "\x16", "\x17", "\x1d", "\x23", "\x24"}

    def __init__(self, source_file: str, logging=False):
        self.source_file: str = source_file
        self.config = []
        self.resources = []
        self.categories = []
        self.labels = []

        self.__file_size: int = None
        self.__file_name: str = "NOT_ASSIGNED"

        self.logging: bool = logging

        self.from_rpk()

    def from_rpk(self):
        offset = 0
        with open(self.source_file, "rb") as file:
            if read_str(file, 3) != b"RPK":
                raise RPKFormatException("File is not an RPK")
            offset += 3

            if (constant := file.read(9)) != b'\x00\x1a\x00\x00\x04\x00\x00\x00\x00':
                print(f"WARNING: expected \"constant\" not encountered; got {constant}")
            offset += 9

            self.__file_size = read_int32(file)
            print("File size:", self.__file_size)
            self.__file_name = read_str(file, 160).rstrip(b'\x00').decode("ascii")
            print("File name:", self.__file_name)
            offset += 8

            print("Unknown Byte:", file.read(1).hex())
            print("Dependency bytes:", read_bytes_display(file, 4))
            offset += 5

            # checking if the carriage return that's always been there is still there.
            if (carriage_return := file.read(1)) != b'\r':
                print(f"WARNING: expected \\r; got {carriage_return} at offset {offset}")
            offset += 1

            if (unknown := file.read(1)) != 0x00:
                print(f"WARNING: expected 0x00, got {unknown}")
            offset += 1

            print("Found following fields, listed as <id>:<value>, ", end="")

            # # do a bit of screwy stuff to work out size of fields
            # file.read(1)
            # if file.read(1) == 0x00:
            #     byte_len = 4
            # else:
            #     byte_len = 1
            # print(f"with byte_len {byte_len}:")
            #
            # file.seek(-2, SEEK_CUR)

            field_len = 4

            val = ""
            id = ""
            while id[-2:] != "7f":
                id = read_bytes_display(file, field_len)
                val = read_bytes_display(file, field_len)
                print(f"{id}:{val}")

                offset += field_len * 2

            print("Unknown Bytes (searching for 04 00 00 00): ", end="")
            # this block relies on the length of the filename being preceded by 04 00 00 00
            while True:
                byte = file.read(1)
                if byte != b'\x04':
                    print(byte.hex(), end=" ")
                    continue
                else:
                    file.seek(-1, SEEK_CUR)
                    int_bytes = file.read(4)
                    val = struct.unpack("<I", int_bytes)[0]
                    if val == 4:
                        pos = file.tell()
                        try:
                            # try to read the filename
                            filename_size = read_int32(file)
                            filename = read_ascii(file, filename_size)
                            print()
                            break
                        except UnicodeDecodeError as e:
                            # failed to read as ascii, probably wrong 4
                            file.seek(pos)
                            print("(04 00 00 00) ", end="")
                            continue
                    else:
                        file.seek(-3, SEEK_CUR)
                        print(byte.hex(), end=" ")
                        continue
            print()
            print("File Name #2:", filename)
            print("Following Filename:", read_bytes_display(file, 3))  # should catch 01 01 00

            print("Unknown Bytes: ")
            while True:
                byte = file.read(1)
                if byte == b'':
                    print("reached end of file while searching for resource")
                    raise RPKFormatException("Unable to locate beginning of resources")
                elif byte != b'\x80':
                    print(byte.hex(), end=" ")
                    continue
                else:
                    file.seek(-1, SEEK_CUR)
                    resource_header_bytes = file.read(14)
                    if resource_header_bytes != b'\x80\x01\x00\x00\x00\x00\x20\x40\x00\x00\x00\x00\x00\x00':
                        file.seek(-14, SEEK_CUR)
                        print("WARNING: Expected resource header not encountered, got:",
                              read_bytes_display(file, 14))
                        file.seek(-13, SEEK_CUR)
                    else:
                        print("\nResource Header:", resource_header_bytes)
                        break

            resource = ResourceNode()
            resource.from_rpk(file)
            self.resources.append(resource)

    def to_json(self):
        return


class RPKFormatException (IOError):
    def __init__(self, error: str = None):
        if error:
            self.message = error
        else:
            self.message = "No Error Message Defined"
