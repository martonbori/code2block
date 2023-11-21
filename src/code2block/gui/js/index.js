init_editor()

$("#import_module_btn").on("click", function() {
    console.log("click")
    add_module_modal = $("#import_module_modal")
    add_module_modal.modal("show")
});

$("#import_module_modal_form").submit(function (event) {
    event.preventDefault();
    $("#btn_add_module_submit").prop("disabled",true)
    $("#spinner_btn_add_module_submit").removeAttr("hidden")


    submit_form($(this), function(data) {
        data = JSON.parse(data)
        console.log(data)
        add_category(data["module_name"], data["blocks"])
        $("#import_module_btn").on("click", function() {
            console.log("click")
            add_module_modal = $("#import_module_modal")
            add_module_modal.modal("show")
        });
        $("#spinner_btn_add_module_submit").attr("hidden", "hidden")
        $("#btn_add_module_submit").prop("disabled",false)
        $("#import_module_modal").modal("hide")
    });

});