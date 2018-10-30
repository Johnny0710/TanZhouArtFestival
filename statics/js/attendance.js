$(function(){
    var $btn = $("table .btn");
    $btn.click(function () {
        var $td = $(this).parent().parent().children();
        $.ajax({
            "type":"post",
            "url":"/attendance/post",
            "data":{
                "stuid":$td[1].textContent,
                "atten_type":$(this).val()
            },
            "success":function(res){
                $td[4].textContent = res.type;
                $td[5].textContent = res.time
            }
        });

    });

    $('#search').keyup(function () {
        $('table tbody tr').hide().filter(":contains('"+($(this).val())+"')").show()
    });
});