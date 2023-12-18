import string
from typing import List


class BlockArg:

    def __init__(self, type, name, check):
        self.type = type
        self.name = name
        self.check = check

range

class Block:

    def __init__(self,
                 block_type: str,
                 name: str,
                 message: str,
                 simple: str = "",
                 tooltip: str = None):
        self.type = block_type
        self.name = name
        self.message = message
        if simple:
            self.simple = simple
        else:
            self.simple = self.message
        self.colour = 0
        self.tooltip = tooltip
