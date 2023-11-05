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


class FunctionBlock(Block):

    def __init__(self,
                 name: string,
                 label: string,
                 tooltip: string = None,
                 args: List[BlockArg] = None,
                 output_type: string = None,
                 previousStatement: string = None,
                 nextStatement: string = None):
        super().__init__(name, label, tooltip)
        if not args:
            args = []
        self.args0 = args
        self.colour = 160
        self.output = output_type
        self.previousStatement = previousStatement
        self.nextStatement = nextStatement

class MethodBlock(Block):

    def __init__(self,
                 name: string,
                 label: string,
                 tooltip: string = None,
                 args: List[BlockArg] = None,
                 previousStatement: string = None,
                 nextStatement: string = None):
        super().__init__(name, label, tooltip)
        if not args:
            args = []
        self.args0 = args
        self.colour = 140
        self.previousStatement = previousStatement
        self.nextStatement = nextStatement
