import re

from src.code2block.classes.models.blocks.block import BlockArg, Block
from src.code2block.classes.models.blocks.class_block import ClassBlock
from src.code2block.classes.models.blocks.function_block import FunctionBlock
from src.code2block.classes.models.blocks.method_block import MethodBlock


def generate_method_block(module_path, completion_item, method_signatures):
    label = completion_item.label
    name = f"{label}".replace('(', '_').replace(')', '_').replace(' ', '_').replace(',', '_')
    message = f"{label}"
    if module_path:
        name = f"{module_path}_{name}"
        message = f"{module_path}.{message}"

    block = MethodBlock(
        name=name,
        label=message,
        args=[],
        tooltip=completion_item.documentation)

    # TODO: Support multiple signatures
    if method_signatures and method_signatures[0].parameters:
        signature = method_signatures[0]
        args = []
        arg_strs = []
        for idx, param in enumerate(signature.parameters):
            args.append(BlockArg(
                type="input_value",
                name=param.label,
                check=None))
            arg_strs.append(f"{param.label} = %{idx + 1}")
        if re.search("\(.*\)", block.message0):
            message = re.sub("\(.*\)", f"({' , '.join(arg_strs)})", message)
        else:
            message += f"({' , '.join(arg_strs)})"
        block.args0 = args
        block.message0 = message
    return name, block


def generate_text_block(module_name, completion_item, method_signatures):
    # TODO: generate text value block
    raise NotImplementedError("Block type not implemented: TEXT")


def generate_function_block(module_path, completion_item, signatures) -> (str, Block):
    label = completion_item.label
    name = f"{label}".replace('(', '_').replace(')', '_').replace(' ', '_').replace(',', '_')
    message = f"{label}"
    if module_path:
        name = f"{module_path}_{name}"
        message = f"{module_path}.{message}"
    block = FunctionBlock(
        name=name,
        label=message,
        args=[],
        tooltip=completion_item.documentation)

    # TODO: Support multiple signatures
    if signatures and signatures[0].parameters:
        signature = signatures[0]
        args = []
        arg_strs = []

        for idx, param in enumerate(signature.parameters):
            args.append(BlockArg(
                type="input_value",
                name=param.label,
                check=None))
            arg_strs.append(f"{param.label} = %{idx + 1}")
        if re.search("\(.*\)",block.message0):
            message = re.sub("\(.*\)", f"({' , '.join(arg_strs)})", message)
        else:
            message += f"({' , '.join(arg_strs)})"
        block.args0 = args
        block.message0 = message
    return name, block


def generate_constructor_block(module_name, completion_item, method_signatures):
    # TODO: generate constructor block
    raise NotImplementedError("Block type not implemented: CONSTRUCTOR")


def generate_field_block(module_name, completion_item, method_signatures):
    # TODO: generate field block
    raise NotImplementedError("Block type not implemented: FIELD")


def generate_variable_block(module_name, completion_item, method_signatures):
    # TODO: generate variable block
    raise NotImplementedError("Block type not implemented: VARIABLE")


def generate_class_block(module_name, completion_item, method_signatures):
    # TODO: generate class block
    raise NotImplementedError("Block type not implemented: CLASS")


def generate_interface_block(module_name, completion_item, method_signatures):
    # TODO: generate interface block
    raise NotImplementedError("Block type not implemented: INTERFACE")


def generate_module_block(module_name, completion_item, method_signatures):
    # TODO: generate module block: nested category

    raise NotImplementedError("Block type not implemented: MODULE")


def generate_property_block(module_name, completion_item, method_signatures):
    # TODO: generate property block
    raise NotImplementedError("Block type not implemented: PROPERTY")


def generate_unit_block(module_name, completion_item, method_signatures):
    # TODO: generate unit block
    raise NotImplementedError("Block type not implemented: UNIT")


def generate_value_block(module_name, completion_item, method_signatures):
    # TODO: generate value block
    raise NotImplementedError("Block type not implemented: VALUE")


def generate_enum_block(module_name, completion_item, method_signatures):
    # TODO: generate enum block
    raise NotImplementedError("Block type not implemented: ENUM")


def generate_keyword_block(module_name, completion_item, method_signatures):
    # TODO: generate keyword block
    raise NotImplementedError("Block type not implemented: KEYWORD")


def generate_snippet_block(module_name, completion_item, method_signatures):
    # TODO: generate snippet block
    raise NotImplementedError("Block type not implemented: SNIPPET")


def generate_color_block(module_name, completion_item, method_signatures):
    # TODO: generate color block
    raise NotImplementedError("Block type not implemented: COLOR")


def generate_file_block(module_name, completion_item, method_signatures):
    # TODO: generate file block
    raise NotImplementedError("Block type not implemented: FILE")


def generate_reference_block(module_name, completion_item, method_signatures):
    # TODO: generate reference block
    raise NotImplementedError("Block type not implemented: REFERENCE")


def generate_folder_block(module_name, completion_item, method_signatures):
    # TODO: generate folder block
    raise NotImplementedError("Block type not implemented: FOLDER")


def generate_enum_member_block(module_name, completion_item, method_signatures):
    # TODO: generate enum member block
    raise NotImplementedError("Block type not implemented: ENUM_MEMBER")


def generate_constant_block(module_name, completion_item, method_signatures):
    # TODO: generate constant block
    raise NotImplementedError("Block type not implemented: CONSTANT")


def generate_struct_block(module_name, completion_item, method_signatures):
    # TODO: generate struct block
    raise NotImplementedError("Block type not implemented: STRUCT")


def generate_event_block(module_name, completion_item, method_signatures):
    # TODO: generate event block
    raise NotImplementedError("Block type not implemented: EVENT")


def generate_operator_block(module_name, completion_item, method_signatures):
    # TODO: generate operator block
    raise NotImplementedError("Block type not implemented: OPERATOR")


def generate_type_parameter_block(module_name, completion_item, method_signatures):
    # TODO: generate type parameter block
    raise NotImplementedError("Block type not implemented: TYPE_PARAMETER")

