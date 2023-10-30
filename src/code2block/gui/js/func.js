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
