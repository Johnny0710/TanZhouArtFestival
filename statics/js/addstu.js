$(function(){
    var $input = $("table input");
    var $select = $("table select");
    var $submit = $("table button");
    $submit.click(function () {
        $.ajax({
            "type":"post",
            "url":"/addstu",
            "data": {
                "name": $input[0].value,
                "tel": $input[1].value,
                "qq": $input[2].value,
                "class": $select[0].value
            },
            "success":function (res) {
                if(res){
                    alert(res.message)
                }

            }
        });
    })

});