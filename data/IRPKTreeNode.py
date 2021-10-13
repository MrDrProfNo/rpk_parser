from typing import BinaryIO


class IRPKTreeNode:
    def to_rpk(self):
        raise NotImplementedError()

    def from_rpk(self, file: BinaryIO):
        raise NotImplementedError()

