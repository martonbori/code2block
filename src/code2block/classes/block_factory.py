from typing import List
from sansio_lsp_client import CompletionItem, SignatureInformation, CompletionItemKind
from src.code2block.classes import block_generators
from src.code2block.classes.models.blocks.import_block import ImportBlock

generators = {
    CompletionItemKind.TEXT: block_generators.generate_text_block,
    CompletionItemKind.METHOD: block_generators.generate_method_block,
    CompletionItemKind.FUNCTION: block_generators.generate_function_block,
    CompletionItemKind.CONSTRUCTOR: block_generators.generate_constructor_block,
    CompletionItemKind.FIELD: block_generators.generate_field_block,
    CompletionItemKind.VARIABLE: block_generators.generate_variable_block,
    CompletionItemKind.CLASS: block_generators.generate_class_block,
    CompletionItemKind.INTERFACE: block_generators.generate_interface_block,
    CompletionItemKind.MODULE: block_generators.generate_module_block,
    CompletionItemKind.PROPERTY: block_generators.generate_property_block,
    CompletionItemKind.UNIT: block_generators.generate_unit_block,
    CompletionItemKind.VALUE: block_generators.generate_value_block,
    CompletionItemKind.ENUM: block_generators.generate_enum_block,
    CompletionItemKind.KEYWORD: block_generators.generate_keyword_block,
    CompletionItemKind.SNIPPET: block_generators.generate_snippet_block,
    CompletionItemKind.COLOR: block_generators.generate_color_block,
    CompletionItemKind.FILE: block_generators.generate_file_block,
    CompletionItemKind.REFERENCE: block_generators.generate_reference_block,
    CompletionItemKind.FOLDER: block_generators.generate_folder_block,
    CompletionItemKind.ENUMMEMBER: block_generators.generate_enum_member_block,
    CompletionItemKind.CONSTANT: block_generators.generate_constant_block,
    CompletionItemKind.STRUCT: block_generators.generate_struct_block,
    CompletionItemKind.EVENT: block_generators.generate_event_block,
    CompletionItemKind.OPERATOR: block_generators.generate_operator_block,
    CompletionItemKind.TYPEPARAMETER: block_generators.generate_type_parameter_block,
}


def generate_blocks(module_name: str,
                    completion_list: List[CompletionItem],
                    signature_data: dict[str, List[SignatureInformation]]
                    ):
    """ Generate blocks from symbols """
    category_name = module_name
    if not module_name:
        category_name = "core"
    module_category = {
        "kind": "category",
        "name": category_name,
        "contents": []
    }
    blocks = []
    code_generators = []
    for completion_item in completion_list:
        label = completion_item.label
        kind = completion_item.kind
        signatures = []
        if label in signature_data:
            signatures = signature_data[label]
        print(f"{completion_item.label}: {completion_item.kind.name}")

        try:
            name, block = generators[kind](module_name, completion_item, signatures)
            print(f"{name} -> {block.__dict__}")
            blocks.append(block)
            module_category["contents"].append({"kind": "block", "type": name})
            code_generators.append({
                "block_type": name,
                "code": label
            })
        except NotImplementedError as e:
            print(e)
    import_block = ImportBlock(module_name)
    blocks.append(import_block)
    ret = {
        "blocks": blocks,
        "toolbox_category": module_category,
        "code_generators": code_generators
    }
    return ret


