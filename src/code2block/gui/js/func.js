
/******* Blockly functions *******/

function init_editor() {
    var editor = new BlockMirror({
        'container': document.getElementById('blockmirror-editor'),
        'blocklyMediaPath': '../js/lib/blockly/media/',
        
        //'height': '2000px'
    });
    editor.addChangeListener(function (event) {
        console.log('Change! Better save:', event)
    });
    editor.setCode('a = 0\nb=0\nprint(b)');

    Sk.configure({
        __future__: Sk.python3,
        read: function (filename) {
            if (Sk.builtinFiles === undefined ||
                Sk.builtinFiles["files"][filename] === undefined) {
                throw "File not found: '" + filename + "'";
            }
            return Sk.builtinFiles["files"][filename];
        }
    });

    $('#go').click(function () {
        alert('Starting!')
        var filename = 'main';
        var code = `import pedal`;
        //console.time('Run');
        Sk.importMainWithBody(filename, false, code, true).$d;
        //console.timeEnd('Run');
        alert('Done!')
    });
    
    add_category_button = {
        "kind": "category",
        "name": "Import python module",
        "toolboxitemid": "import_module_btn",
        "disabled": "True"
    }
    add_category(null, add_category_button, null, -1)
    
    $("#import_module_btn").on("click", function() {
        console.log("click")
        add_module_modal = $("#import_module_modal")
        add_module_modal.modal("show")
    });
}

function add_category(blocks, category, code_generators, idx=-2) {
    /** Add blocks to Workspace **/
    if(blocks) {
        Blockly.defineBlocksWithJsonArray(blocks);
        Object.assign(Blockly.Blocks, blocks)    
    }

    /** Update Toolbox **/
    toolbox = Blockly.getMainWorkspace().options.languageTree
    toolbox_json = Blockly.utils.toolbox.convertToolboxDefToJson(toolbox)
    if (idx < 0) {
        idx = toolbox_json["contents"].length + 1 + idx
    }
    toolbox_json["contents"].splice(idx,0, category)
    Blockly.getMainWorkspace().updateToolbox(toolbox_json);
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
