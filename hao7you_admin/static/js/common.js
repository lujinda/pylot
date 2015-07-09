String.format = function(src){
    if (arguments.length == 0)
                return null;
        var args = Array.prototype.slice.call(arguments, 1);
            return src.replace(/\{(\d+)\}/g, function(m, i){
                    return args[i];
                        });
};
function show_error(error, error_title){
    var error_title = error_title || '出错了';
    var $dialog = $('#dialog');
    $dialog.find('.modal-title').html(error_title);
    $dialog.find('.modal-body').html(error);
    $dialog.modal();
}
function public_error_func(){
    show_error('系统出现错误，请重试')
}

