from typing import List
from sansio_lsp_client import CompletionItem, SignatureInformation
from src.code2block.classes.block import Block, BlockArg


def generate_blocks(module_name: str,
                    completion_list: List[CompletionItem],
                    signature_data: dict[str, List[SignatureInformation]]
                    ):
    """ Generate blocks from symbols """
    toolbox_category = {
        "kind": "category",
        "name": module_name,
        "contents": []
    }
    blocks = []
    code_generators = []
    for completion_item in completion_list:
        label = completion_item.label
        type_name = f"{module_name}_{label}".replace('(', '_').replace(')', '_').replace(' ', '_').replace(',', '_')
        if label not in signature_data:
            block = Block(
                type=type_name,
                message0=label,
                colour=160,
                args0=[],
                previousStatement=None,
                nextStatement=None,
                tooltip=label)
            blocks.append(block)
        else:
            signatures = signature_data[label]
            for signature in signatures:
                args = []
                if signature.parameters:
                    for param in signature.parameters:
                        args.append(BlockArg(
                            type="input_value",
                            name=param.label,
                            check=None))
                    for i in range(len(args)):
                        label += f" %{i+1}"
                signature_label = signature.label
                block = Block(
                    type=type_name,
                    message0=label,
                    args0=args,
                    colour=160,
                    previousStatement=None,
                    nextStatement=None,
                    tooltip=signature_label)
                blocks.append(block)
        toolbox_category["contents"].append({"kind": "block", "type": type_name})
        code_generators.append({
            "block_type": type_name,
            "code": label
        })
    ret = {
        "blocks": blocks,
        "toolbox_category": toolbox_category,
        "code_generators": code_generators
    }
    return ret
