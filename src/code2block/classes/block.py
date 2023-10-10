import string
from typing import List


class BlockArg:

    def __init__(self, type, name, check):
        self.type = type
        self.name = name
        self.check = check


class Block:

    def __init__(self, type: string, message0: string, args0: List[BlockArg], colour: int, previousStatement: string = None, nextStatement: string = None, tooltip: string = None):
        self.type = type
        self.message0 = message0
        self.args0 = args0
        self.colour = colour
        self.previousStatement = previousStatement
        self.nextStatement = nextStatement
        self.tooltip = tooltip