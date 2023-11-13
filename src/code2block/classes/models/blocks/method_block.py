import string
from typing import List

from src.code2block.classes.models.blocks.block import Block, BlockArg


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
