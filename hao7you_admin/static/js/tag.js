function add_tag(tag_name){
    data = {'tag_name': tag_name};
    _ajax_tag('POST', data);
}

function update_tag(tag_id, tag_name){
    function update_tag_html(){
        $('#tag_' + tag_id).find('span').first().html(tag_name);
    }
    _ajax_tag('PUT', {'tag_id': tag_id, 'tag_name': tag_name}, update_tag_html);
}

function join_edit(span){
    var $span = $(span);
    $span.hide();
    var $input= $(String.format("<input class='edit_tag_input' style='width:{0}px' name='tag_name' value='{1}'>",
            $span.width() + 20, $span.html()));
    $input.blur(function(){
        var tag_name = this.value.trim();
        if (tag_name == '' || tag_name == $span.val()){

        }else{
            var tag_id = $(span).parent().attr('id').split('tag_')[1];
            update_tag(tag_id, tag_name);
        }
        $(this).remove();
        $span.show();
    });
    $span.after($input);
}

function _ajax_tag(method, data, callback){
    $.ajax({
        url: '/tag',
        type: method,
        data:data,
        success: function(response){
            var error = response['error'];
            if (error){
                show_error(error);
                return false;
            }
            if (callback){
                callback();
            }else{
                location.reload();
            }
        },
        error: public_error_func,
    });
}
function remove_tag(tag_id){
    if (!confirm('确定删除吗?')){
        return false;
    }
    function remote_div(){
        $('#tag_' + tag_id).remove();
    }
    _ajax_tag('DELETE', {'tag_id': tag_id}, remote_div);
}

$(document).ready(function(){
    $('#add_tag_wrap form').submit(function(){
        var tag_name = $(this).find('input').val().trim();
        if (!tag_name){
            return false;
        }
        add_tag(tag_name);
        return false;
    });
});

