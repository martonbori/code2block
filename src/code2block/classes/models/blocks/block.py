import string
from typing import List


class BlockArg:

    def __init__(self, type, name, check):
        self.type = type
        self.name = name
        self.check = check


class Block:

    def __init__(self,
                 name: string,
                 label: string,
                 tooltip: string = None):
        self.type = name
        self.message0 = label
        self.colour = 0
        self.tooltip = tooltip
