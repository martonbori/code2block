import string
from typing import List

from src.code2block.classes.models.blocks.block import Block, BlockArg


class MethodBlock(Block):

    def __init__(self,
                 name: str,
                 message: str,
                 simple: str = "",
                 tooltip: str = None,
                 args: List[BlockArg] = None,
                 returns: bool = False):
        super().__init__("ast_Call", name, message, simple, tooltip)
        if not args:
            args = []
        self.args = args
        self.colour = 140
        self.returns = returns
