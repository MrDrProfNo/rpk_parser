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




class RPK_Node (IRPKTreeNode):

    def __init__(self, source_file: str):
        self.source_file: str = source_file
        self.config = []
        self.resources = []
        self.categories = []
        self.labels = []

        self.__file_size: int = None
        self.__file_name: str = "NOT_ASSIGNED"

        self.from_rpk()

    def from_rpk(self):
        with open(self.source_file, "rb") as file:
            if read_str(file, 3) != b"RPK":
                raise FileFormatException("File is not an RPK")

            if (constant := file.read(9)) != b'\x00\x1a\x00\x00\x04\x00\x00\x00\x00':
                print(f"WARNING: expected \"constant\" not encountered; got {constant}")

            self.__file_size = read_int32(file)
            print("File size:", self.__file_size)
            self.__file_name = read_str(file, 160).rstrip(b'\x00').decode("ascii")
            print("File name:", self.__file_name)

            print("Unknown Byte:", file.read(1).hex())
            print("Dependency bytes:", read_bytes_display(file, 4))

            # checking if the carriage return that's always been there is still there.
            if (carriage_return := file.read(1)) != b'\r':
                print(f"WARNING: expected \\r not encountered; got {carriage_return}")

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
                if byte != b'\x80':
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

            for i in range(3):
                resource = ResourceNode()
                resource.from_rpk(file)
                self.resources.append(resource)



class FileFormatException (IOError):
    def __init__(self, error: str = None):
        if error:
            self.message = error
        else:
            self.message = "No Error Message Defined"
