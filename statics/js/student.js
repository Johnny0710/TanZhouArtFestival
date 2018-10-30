$(function () {
    var $reset_btn = $("table .reset");
    var $add_student_btn = $("#add_student");
    var $send_student = $("#send_student");
    $reset_btn.click(function () {
        var $td = $(this).parent().parent().children();
        $.ajax({
            "type": "post",
            "url": "/stu",
            "data": {
                "stuid": $td[1].textContent,
                "rest": $(this).val()
            },
            "success": function (res) {
                if (res.rest) {
                    $td[7].innerText = res.resttime;
                    $td[8].innerText = "休学";
                } else {
                    $td[7].textContent = "";
                    $td[8].textContent = "正常";
                }
            }
        })

    });
    $add_student_btn.click(function () {
        
    });
    $send_student.click(function () {

        var clss_id = $("#class_id").val();
        $.ajax({
            "type":"post",
            "url":"/addstu",
            "data":{
                "stuid":$("#stuid").val(),
                "stuname":$("#stuname").val(),
                "tel":$("#tel").val(),
                "qq":$("#qq").val(),
                "clss_id":$("#class_id").val()
            },
            "success":function (res) {
                if(res=="Error"){
                    alert("学员信息录入失败,请重试")
                }else{
                    parent.location.reload()
                }
            }
        })

    });
    $('#search').keyup(function () {
        $('table tbody tr').hide().filter(":contains('"+($(this).val())+"')").show()
    });



});