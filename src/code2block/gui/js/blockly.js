Blockly.defineBlocksWithJsonArray([{
    "type": "back",
    "message0": 'length of %1',
    "args0": [
        {
            "type": "input_value",
            "name": "distance",
            "check": "float"
        }
    ],
    "output": null,
    "colour": 160,
    "tooltip": "Returns number of letters in the provided text.",
    "helpUrl": "http://www.w3schools.com/jsref/jsref_length_string.asp"
}]);
var toolbox = {
    "kind": "flyoutToolbox",
    "contents": [
        {
            "kind": "block",
            "type": "controls_if"
        },
        {
            "kind": "block",
            "type": "controls_whileUntil"
        },
        {
            "kind": "block",
            "type": "back"
        }
    ]
};
Blockly.inject('blocklyDiv', {
    trashcan: true,
    toolbox:toolbox
})
