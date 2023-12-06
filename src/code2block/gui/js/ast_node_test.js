


Blockly.Python['json_load_fp__cls__object_hook__parse_float__parse_int__parse_constant__object_pairs_hook__kwds_'] = function (block) {
    // Create a list with any number of elements of any type.
    let value = Blockly.Python.valueToCode(block, 'VALUE',
        Blockly.Python.ORDER_NONE) || Blockly.Python.blank;
    let targets = new Array(block.targetCount_);
    if (block.targetCount_ === 1 && block.simpleTarget_) {
        targets[0] = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    } else {
        for (var i = 0; i < block.targetCount_; i++) {
            targets[i] = (Blockly.Python.valueToCode(block, 'TARGET' + i,
                Blockly.Python.ORDER_NONE) || Blockly.Python.blank);
        }
    }
    return targets.join(' = ') + " = " + value + "\n";
};

BlockMirrorTextToBlocks.prototype['json_load_fp__cls__object_hook__parse_float__parse_int__parse_constant__object_pairs_hook__kwds_'] = function (node, parent) {
    let targets = node.targets;
    let value = node.value;

    let values;
    let fields = {};
    let simpleTarget = (targets.length === 1 && targets[0]._astname === 'Name');
    if (simpleTarget) {
        values = {};
        fields['VAR'] = Sk.ffi.remapToJs(targets[0].id);
    } else {
        values = this.convertElements("TARGET", targets, node);
    }
    values['VALUE'] = this.convert(value, node);

    return BlockMirrorTextToBlocks.create_block("json_load_fp__cls__object_hook__parse_float__parse_int__parse_constant__object_pairs_hook__kwds_", node.lineno, fields,
        values,
        {
            "inline": "true",
        }, {
            "@targets": targets.length,
            "@simple": simpleTarget
        });
};
