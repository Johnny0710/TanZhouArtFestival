$(function(){
    $btn_pop = $(".pop");
    $btn_send = $('#send_remark');
    var stuid = '';
    var workid = '';
    var submit = '';
    var btn_index = null;

    $btn_pop.click(function () {
        var $td = $(this).parent().parent().children();
        stuid = $td[1].textContent;
        $(this).attr("id","index")
    });

    $btn_send.click(function () {
        var $td = $(this).parent().parent().children();
        $.ajax(
            {
                "type":"post",
                "url":window.location.pathname,
                "data":{
                    "stuid":stuid,
                    "remark":$('#recipient-name').val()
                },
                "success": function (res) {
                    if (res) {
                        $('#index').text("修改评语");
                        $('#index').attr("data-whatever",res);
                        $('#index').attr("title","已添加评语:"+res);
                        $('#index').removeAttr('id')
                    } else {
                        alert('评语添加失败,请重新尝试');
                        $('#index').removeAttr('id')
                    }
                }

            }
        )
        
    });

    $('#cancel').click(function () {
        $('#index').removeAttr('id')
    });
});