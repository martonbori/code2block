init_editor()

$("#import_module_modal_form").submit(function (event) {
    event.preventDefault();

    submit_form($(this), function(data) {
        data = JSON.parse(data)
        console.log(data)
        add_category(data["module_name"], data["blocks"])
        $("#import_module_modal").modal("hide")
    });
});