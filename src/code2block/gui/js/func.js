
/******* Blockly functions *******/

function init_blockly() {
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
            {
                "kind": "category",
                "name": "Import python module",
                "toolboxitemid": "import_module_btn",
                "disabled": "True"
            }
            
        ]
    };
    var w = Blockly.inject('blocklyDiv', {
        trashcan: true,
        toolbox:toolbox_json
    });
    $("#import_module_btn").on("click", function() {
        console.log("click")
        add_module_modal = $("#import_module_modal")
        add_module_modal.modal("show")
    });

    return w
}

function updateToolbox(workspace, toolbox_json) {
    workspace.updateToolbox(toolbox_json)
    $("#import_module_btn").on("click", function() {
        console.log("click")
        add_module_modal = $("#import_module_modal")
        add_module_modal.modal("show")
    });
}

function add_category(workspace, blocks, category, code_generators) {
    Blockly.defineBlocksWithJsonArray(blocks);
    toolbox = workspace.getToolbox().toolboxDef_
    console.log(toolbox)
    toolbox["contents"].splice(-1,0, category)
    updateToolbox(workspace, toolbox)
}


/******* JQuery functions *******/


function submit_form(form, callback = null, callback_on_fail = null) {
    
    url = $(form).attr('action');

    let post_values = {}

    $(form).find('input').each(function() {
        if(this.hasAttribute('name')) {
            if (this.type == "file" && this.hasAttribute("data-content")) {
                post_values[this.name] = this.dataset.content;
            } else if (this.type == "number") {                
                post_values[this.name] = parseInt(this.value);
                console.log(post_values)
            }
            else {
                post_values[this.name] = this.value;
            }    
        }
    });

    let posting = $.post(url, post_values);
    if (callback) {
        posting.done(function(data) {
            callback(data);
        });    
    }

    if (callback_on_fail) {
        posting.fail(function(xhr) {
            callback_on_fail(xhr);
        });    
    }

}
