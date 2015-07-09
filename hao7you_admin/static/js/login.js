function login_account(username, password){
    $.ajax({
        url: '/login' + location.search,
        type: 'POST',
        data: {'username': username, 'password': password},
        success: function(response){
            var error = response['error'];
            if (error){
                show_error(error, '登录失败');
                return;
            }
            var return_url = response['return_url'];
            location.href = return_url;
        },
        error: function(){
            show_error('系统出错，请重试');
        }
    });
}

$(document).ready(function(){
    $('#login_wrap').submit(function(){
        var username = $(this).find('input[name="username"]').val().trim();
        var password = $(this).find('input[name="password"]').val().trim();
        if (!(username && password)){
            show_error('请把登录信息输入完整');
            return false;
        }
        login_account(username, password);
        return false;
    });
});
