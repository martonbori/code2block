import string
from typing import List

from src.code2block.classes.models.blocks.block import Block, BlockArg


class ImportBlock(Block):

    def __init__(self,
                 module_name: str):
        super().__init__("ast_Import",
                         f"import_{module_name}",
                         f"import {module_name}",
                         f"import_{module_name}",
                         f"imports {module_name} to the workspace")
        self.module_name = module_name
        self.colour = 90
