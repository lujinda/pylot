function remove_brand(brand_id){
    var $box = $('#box_' + brand_id);
    if (confirm('确定要删除 ' + $box.find('.brand_name').html() + ' 吗?')){
        $.ajax({
            url: '/brand',
            type: 'DELETE',
            data: {'brand_id': brand_id},
            success: function(response){
                var error = response['error'];
                if (error){
                    show_error(error);
                    return false;
                }
                location.reload();
            },
            error: public_error_func,
        });
    }
    return false;
}

function update_brand(brand_id){
    var $box = $('#box_' + brand_id);
    var brand_login_url = $box.find('img').attr('src');
    var brand_name = $box.find('.brand_name').html();
    var brand_alias_name = $box.find('.brand_alias_name').val();
    var brand_summary = $box.find('.brand_summary').html();
    var dialog = $('#add_brand_wrap').resetForm();
    dialog.find('input[name="brand_id"]').val(brand_id);
    dialog.find('input[name="brand_name"]').val(brand_name);
    dialog.find('input[name="brand_logo_url"]').val(brand_login_url);
    dialog.find('input[name="brand_alias_name"]').val(brand_alias_name);
    dialog.find('textarea').val(brand_summary);
    dialog.find('.modal-title').html('修改品牌');
    dialog.find('button[type="submit"]').html('修改');
    dialog.modal();
}
function add_brand(){
    var wrap = $('#add_brand_wrap').modal();
    wrap.find('form').resetForm().find('input').val('');
    wrap.find('.modal-title').html('添加品牌');
    wrap.find('button[type="submit"]').html('添加');
    wrap.modal();
}
function list_model(model_id, button){
    var $btn = $(button);
    $.ajax({
        type: 'GET',
        data: {'model_id': model_id},
        success: function(response){
            var error = response['error'];
            if (error){
                show_error(error);
                return false;
            }else{
                var param = response['param'];
                var $tbody = $btn.next().find('tbody').empty();
                write_model_param(param, $tbody);
                $btn.remove();
            }
        },
        error: public_error_func,
    });
}
function write_model_param(param, $tbody){
    for (var name in param){
        var obj = $(String.format("#add_model_wrap [name='{0}']", name));
        var param_name = obj.prev().find('span').html();
        var $tr = $(String.format('<tr><td>{0}</td><td>{1}</td></tr>',
                    param_name, param[name]));
        $tbody.append($tr);
    }
    $tbody.parent().parent().fadeIn();
}
function remove_model(model_id){
    if (!confirm('是否确定要删除?')){
        return;
    }
    $.ajax({
        type: 'DELETE',
        data: {'model_id': model_id},
        success: function(response){
            var error = response['error'];
            if (error){
                show_error(error);
                return;
            }
            $('#box_' + model_id).remove();
        },
        error: public_error_func,
    });
}

$(document).ready(function(){
    $('#add_brand_wrap form').submit(function (){
        var $form = $(this);
        var $inputs = $form.find('input');
        for (var i = 0; i < $inputs.length; i++){
            if ($inputs[i].value.trim() == "" && $inputs[i].name != 'brand_id'){
                show_error('请把必要参数填写完整');
                return false;
            }
        }
        var is_update  = $form.find('input[name="brand_id"]').val() != "" && true || false;
        $form.ajaxSubmit({
            type: is_update && 'PUT' || 'POST',
            success: function(response){
                var error = response['error'];
                if (error){
                    show_error(error);
                    return false;
                }
                location.reload();
            },
            error: public_error_func,
        });
        return false;
    });
    $('#add_model_wrap form').submit(function(){
        $(this).ajaxSubmit({
            success: function(response){
                var error = response['error'];
                if (error){
                    show_error(error);
                    return false;
                }
                location.reload();
            },
            error:public_error_func
        });
        return false;
    });
});
