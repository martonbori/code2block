import string
from typing import List

from src.code2block.classes.models.blocks.block import Block, BlockArg


class ClassBlock(Block):

    def __init__(self,
                 name: string,
                 label: string,
                 tooltip: string = None,
                 args: List[BlockArg] = None,
                 output_type: string = None):
        super().__init__(name, label, tooltip)
        if not args:
            args = []
        self.args0 = args
        self.colour = 120
        self.output = output_type
