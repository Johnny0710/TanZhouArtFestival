$(function () {
    $inspect_btn = $('table .inspect');
    $inspect_btn.click(function () {
        $td = $(this).parent().parent().children();
        $('#inspect').attr('src','/inspect/'+$td[1].textContent)

    })
});