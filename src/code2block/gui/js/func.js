
/******* Blockly functions *******/
var editor;

function init_editor() {
    editor = new BlockMirror({
        'container': document.getElementById('blockmirror-editor'),
        'blocklyMediaPath': '../js/lib/blockly/media/',
        'toolbox':'normal'
        //'height': '2000px'
    });
    editor.addChangeListener(function (event) {
        console.log('Change! Better save:', event)
    });

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


    
    

    Blockly.Extensions.registerMutator(
        "test_mutator",
        {
            "saveExtraState": function() {
                return {
                  'testAttrib': "test atrib value",
                };
              },
              
            "loadExtraState": function(state) {
                this.testAttrib = state['testAttrib'];
                // This is a helper function which adds or removes inputs from the block.
                this.updateShape_();
            },
            "mutationToDom": function() {
                var container = Blockly.utils.xml.createElement('mutation');
                container.setAttribute('testAttrib', "test atrib value");
                return container;
            },
            "domToMutation": function() {
                this.testAttrib = xmlElement.getAttribute('testAttrib');
                this.updateShape_();
            }
        }
    )



}

function add_category(module_name, blocks, idx=-2) {
    /** Add blocks to Workspace **/
    console.log(blocks)

    if (blocks) {
        BlockMirrorTextToBlocks.prototype.MODULE_FUNCTION_SIGNATURES[module_name] = {}
        category_contents = []
        blocks.forEach(block => {
            var block_code = ""
            if (block.type == "ast_Import") {
                let argumentsMutation = {
                    "@names": 1,
                    "regular": [true]
                };
                let fields = {
                    "NAME0": block.module_name,
                    "MODULE": block.module_name
                }
                let block_xml = BlockMirrorTextToBlocks.create_block("ast_Import", null, fields,{}, {inline: true}, argumentsMutation);
                console.log(block_xml)
                block_code = block.message
            }
            else {
                block_name = block["name"]
                block_code = block["message"] + "("
                args = []
                if (block["args"].length > 0) {
                    block["args"].forEach(arg => {
                        args.push(arg.type)
                        block_code += "___,"
                    })
                    block_code = block_code.replace(/.$/,")")
                }
                else {
                    block_code += ")"
                }
                BlockMirrorTextToBlocks.prototype.MODULE_FUNCTION_SIGNATURES[module_name][block_name] = {
                    "returns": block["returns"],
                    "simple": args,
                    "message": block["message"],
                    "colour": block["colour"]
                };
            }
            category_contents.push(block_code)
        });    
    }
    BlockMirrorTextToBlocks.prototype.MODULE_FUNCTION_IMPORTS[module_name] = "import " + module_name
    BlockMirrorBlockEditor.prototype.TOOLBOXES["normal"].push({name: module_name, colour:"FUNCTIONS", blocks: category_contents})
    document.getElementById('blockmirror-editor').innerHTML = ""
    editor = new BlockMirror({
        'container': document.getElementById('blockmirror-editor'),
        'blocklyMediaPath': '../js/lib/blockly/media/',
        'toolbox':'normal'
    });
}


function getFunctionBlock(name, values, module) {
    if (values === undefined) {
        values = {};
    }
    // TODO: hack, we shouldn't be accessing the prototype like this
    let signature;
    let method = false;
    if (module !== undefined) {
        signature = BlockMirrorTextToBlocks.prototype.MODULE_FUNCTION_SIGNATURES[module][name];
    } else if (name.startsWith('.')) {
        signature = BlockMirrorTextToBlocks.prototype.METHOD_SIGNATURES[name.substr(1)];
        method = true;
    } else {
        signature = BlockMirrorTextToBlocks.prototype.FUNCTION_SIGNATURES[name];
    }
    let args = (signature.simple !== undefined ? signature.simple :
               signature.full !== undefined ? signature.full : []);
    let argumentsMutation = {
        "@arguments": args.length,
        "@returns": (signature.returns || false),
        "@parameters": true,
        "@method": method,
        "@name": module ? module+"."+name : name,
        "@message": signature.message ? signature.message : name,
        "@premessage": signature.premessage ? signature.premessage : "",
        "@colour": signature.colour ? signature.colour : 0,
        "@module": module || ""
    };
    for (let i = 0; i < args.length; i += 1) {
        argumentsMutation["UNKNOWN_ARG:" + i] = null;
    }
    let newBlock = BlockMirrorTextToBlocks.create_block("ast_Call", null, {},
        values, {inline: true}, argumentsMutation);
    // Return as either statement or expression
    return BlockMirrorTextToBlocks.xmlToString(newBlock);
};

function create_block_json(type, lineNumber, fields, values, settings, mutations, statements) {
    var newBlock = {
        "type": type,
        "line_number": lineNumber
    }
    
    for (var setting in settings) {
        var settingValue = settings[setting];
        newBlock[setting] = settingValue;
    }
    // Mutations
    /*
    if (mutations !== undefined && Object.keys(mutations).length > 0) {
        mutator_functions = {
            decompose: function(workspace) {
                // This is a special sub-block that only gets created in the mutator UI.
                // It acts as our "top block"
                var topBlock = workspace.newBlock('lists_create_with_container');
                topBlock.initSvg();
              
                // Then we add one sub-block for each item in the list.
                var connection = topBlock.getInput('STACK').connection;
                for (var i = 0; i < this.itemCount_; i++) {
                  var itemBlock = workspace.newBlock('lists_create_with_item');
                  itemBlock.initSvg();
                  connection.connect(itemBlock.previousConnection);
                  connection = itemBlock.nextConnection;
                }
              
                // And finally we have to return the top-block.
                return topBlock;
              },
        }
        args = {}
        for (let mutation in mutations) {
            var mutationValue = mutations[mutation];
            if (mutation.charAt(0) === '@') {
                newMutation[mutation.substr(1)] = mutationValue;
            } else if (mutationValue != null && mutationValue.constructor === Array) {
                for (var i = 0; i < mutationValue.length; i++) {
                    let mutationNode = {};
                    mutationNode["name"] = mutationValue[i];
                    newMutation.appendChild(mutationNode);
                }
            } else {
                let mutationNode = document.createElement("arg");
                if (mutation.charAt(0) === '!') {
                    mutationNode.setAttribute("name", "");
                } else {
                    mutationNode.setAttribute("name", mutation);
                }
                if (mutationValue !== null) {
                    mutationNode.appendChild(mutationValue);
                }
                newMutation.appendChild(mutationNode);
            }
        }
        Blockly.Extensions.registerMutator(
            type + '_mutator',
            {
                saveExtraState: function() {
                    return {
                      'itemCount': this.itemCount_,
                    };
                  },
                  
                  loadExtraState: function(state) {
                    this.itemCount_ = state['itemCount'];
                    // This is a helper function which adds or removes inputs from the block.
                    this.updateShape_();
                  },
            },
            undefined,
            []
        );

        newBlock.appendChild(newMutation);
    }*/
    // Fields
    for (var field in fields) {
        var fieldValue = fields[field];
        var newField = document.createElement("field");
        newField.setAttribute("name", field);
        newField.appendChild(document.createTextNode(fieldValue));
        newBlock.appendChild(newField);
    }
    // Values
    for (var value in values) {
        var valueValue = values[value];
        var newValue = document.createElement("value");
        if (valueValue !== null) {
            newValue.setAttribute("name", value);
            newValue.appendChild(valueValue);
            newBlock.appendChild(newValue);
        }
    }
    // Statements
    if (statements !== undefined && Object.keys(statements).length > 0) {
        for (var statement in statements) {
            var statementValue = statements[statement];
            if (statementValue == null) {
                continue;
            } else {
                for (var i = 0; i < statementValue.length; i += 1) {
                    // In most cases, you really shouldn't ever have more than
                    //  one statement in this list. I'm not sure Blockly likes
                    //  that.
                    var newStatement = document.createElement("statement");
                    newStatement.setAttribute("name", statement);
                    newStatement.appendChild(statementValue[i]);
                    newBlock.appendChild(newStatement);
                }
            }
        }
    }
    return newBlock;
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
