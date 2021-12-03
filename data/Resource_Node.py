from data.IRPKTreeNode import IRPKTreeNode
from typing import List, BinaryIO
from parser_utils.bytes_reader import *
import json

# constant for use in file.seek() operations
SEEK_CUR = 1

class ResourceNode (IRPKTreeNode):

    def __init__(self):
        self.type: bytes = None
        self.id: int = None
        self.name: bytes = None
        self.fields = []
        self.default_fields: List[bool] = []

    def from_rpk(self, file: BinaryIO):
        # seeking backwards to find the resource type
        file.seek(-22, SEEK_CUR)
        self.type = read_bytes_display(file, 4)
        file.seek(18, SEEK_CUR)
        print("Resource type:", self.type)

        print("Magic 4-byte: " + read_bytes_display(file, 4))
        print("Resource UID(Hex):", read_ascii(file, 19))
        print("Resource\\Category:", read_ascii(file, 3))
        name_size = read_int32(file)
        resource_name = read_ascii(file, name_size)
        resource_UID_2 = read_int32(file)
        resource_UID_1 = read_int32(file)
        print(f"Resource UID(decimal): {resource_UID_1}-{resource_UID_2}")
        print(f"Resource Name:", resource_name)
        after_name = read_int8(file)
        print(f"byte after resource ID hex: {after_name}")
        num_defined_fields = read_int8(file)
        field_offsets = []

        for i in range(num_defined_fields):
            field_num = read_int8(file)
            field_offset = read_int8(file)
            field_offsets.append((field_num, field_offset))

        for num, offset in field_offsets:
            field_val = read_int32(file)
            self.fields.append((num, field_val))

        print("Fields:")
        for num, value in self.fields:
            print(f"{num}: {value}")

        resource_footer = read_bytes_display(file, 3)
        if resource_footer == "01 01 00":
            print(f"standard resource footer: {resource_footer}")
        else:
            print(f"WARNING: Received unexpected 3 bytes at end of resource: {resource_footer}")

        return

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "type": self.type,
            "id": self.id,
            "name": self.name,
            "fields": self.fields,
            "default_fields": self.default_fields
        }

