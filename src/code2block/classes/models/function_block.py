import string
from typing import List

from src.code2block.classes.models.block import Block, BlockArg


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