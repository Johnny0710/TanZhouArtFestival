$(function(){
    function stuid(btn) {
        return btn.parent().parent().children()[1].textContent
    }
    function stuname(btn) {
        return btn.parent().parent().children()[2].textContent
    }

    function add_src(type, stuid) {
        $('#level').attr('src', '/level/' + type + '/' + stuid)
    }

    $up_btn = $('table .upclass');
    $down_btn = $('table .downclass');
    $repeat_btn = $('table .repeatclass');
    $showscore_btn = $('table .showscore');
    $score_close = $('#score_close');
    $submit_score = $('#submit_score');
    $add_score = $("table .add_score_btn");
    $up_btn.click(function () {
        add_src('up',stuid($(this)))
    });

    $down_btn.click(function () {
        add_src('down',stuid($(this)))
    });

    $repeat_btn.click(function () {
        add_src('repeat',stuid($(this)))
    });

    $showscore_btn.click(function () {
        stuid_ = stuid($(this))
        $.ajax({
            "type":"post",
            "url":"/exam/post",
            "data":{
                "stuid":stuid_
            },
            "success":function (res) {

                for (n in res[stuid_]){


                    $('#score_window tbody').append(
                        $("<tr>"),
                        $("<td></td>").text(res[stuid_][n]['class']),
                        $("<td></td>").text(res[stuid_][n]['score']),
                        $("<td></td>").text(res[stuid_][n]['time']),
                        $("</tr>")

                    );
                }

            }
        })
    });
    
    $submit_score.click(function () {
        var score = $("#input_score").val();
        var datetime = $('#input_date').val().replace("T"," ");
        var stuid = $("#stu_id").text();
        var cls_id = window.location.pathname.replace('/exam/','');
        if(score>100 || isNaN(score)){
            alert("分数不合法,请检查");
            return
        }

        $.ajax({
            "type":"post",
            "url":"/addscore/"+cls_id+'/'+stuid,
            "data":{
                "score":score,
                "datetime":datetime
            },
            "success":function (res) {
                console.log(res);
                if (res=="Error"){
                    alert("成绩添加失败,请重试")
                }else{
                    parent.location.reload()
                }
            }
        })

    });

    $score_close.click(function(){
        $('#score_window tbody').empty()
    });

    $add_score.click(function(){

        var mydate = new Date();
        var year = mydate.getFullYear();
        var month = mydate.getMonth();
        var day = mydate.getDate();
        var hour = mydate.getHours();
        var minutes = mydate.getMinutes();
        var seconds = mydate.getSeconds();
        if(month<10){
            month = 0 + String(month)
        }
        if(day<10){
            day = 0 + String(day)
        }
        if(hour<10){
            hour = 0 + String(hour)
        }
        if(minutes<10){
            minutes = 0 + String(minutes)
        }
        if(seconds<10){
            seconds = 0 + String(seconds)
        }
        $("#input_date").attr("value",year+'-'+month+'-'+day+'T'+hour+':'+minutes+':'+seconds);
        $("#stu_id").text(stuid($(this)));
        $("#stuname").text(stuname($(this)))


    })



});