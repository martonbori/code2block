Blockly.defineBlocksWithJsonArray(block_definitions);

var toolbox_json = {
    "kind": "categoryToolbox",
    "contents": [
        {
            "kind": "category",
            "name": "Basic",
            "contents": [
                {
                    "kind": "block",
                    "type": "controls_if"
                },
                {
                    "kind": "block",
                    "type": "controls_whileUntil"
                }
            ]
        },
        toolbox_data,
        {
            "kind": "category",
            "name": "Import python module",
            "toolboxitemid": "import_module_btn"
        }
        
    ]};
var workspace = Blockly.inject('blocklyDiv', {
    trashcan: true,
    toolbox:toolbox_json
})
var toolbox = workspace.getToolbox()
var category_div = toolbox.getToolboxItemById("import_module_btn").getDiv();


category_div.addEventListener("click", function(e) {
    add_module_modal = $("#import_module_modal")
    add_module_modal.modal("show")
});
