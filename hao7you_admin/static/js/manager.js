function _check_account_form($form){
    var $inputs = $form.find('input');
    for (var i = 0; i < $inputs.length; i++){
        if ($inputs[i].value.trim() == ""){
            return '请不要有空内容哦';
        }
    }
    if ($form.find('#password_input_one').val() != $form.find('#password_input_two').val()){
        return '两次输入的新密码不同';
    }
}

function get_submit_data_error(obj, $form){
    switch(obj)
    {
        case 'account':
            return _check_account_form($form);
    }
}
$(document).ready(function(){
$('.current_modal form').submit(function(){
    var $form = $(this);
    var parts = location.pathname.split('/');
    var current_obj = parts[parts.length - 1];
    var error = get_submit_data_error(current_obj, $form);
    if (error){
        show_error(error);
        return false;
    }
    $form.ajaxSubmit({
        success: function(response){
            var error = response['error'];
            if (error){
                show_error(error);
                return;
            }
        },
        error: function (){
            show_error('系统出错，请重试');
        }
    });
    return false;
});
});
