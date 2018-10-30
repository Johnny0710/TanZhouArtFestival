$(function () {
    $submit = $('#submit');
    $stuid = $('#stuid');
    $stuname = $('#stuname');
    $select = $('select');
    $submit.click(function () {
        $.ajax(
            {
                "type":"post",
                "url":'/level/post/submit',
                "data":{
                    "stuid":$stuid.text(),
                    "class_id":$select.val()
                },
                "success":function (res) {
                    if (res){
                        console.log(res);
                        parent.location.reload()
                    }else{
                        alert('学员班级调整失败,请重试')
                        parent.location.reload()
                    }
                }
            }
        )

    })


});