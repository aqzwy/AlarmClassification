$(document).ready(function() {
    // bind event
    $("#btn_classification").click(prediction);
});


function prediction(event){
    var alarm_content = $("#alarm_content").val();
    if(alarm_content.length < 1){
        alert("警情描述不能为空");
        return;
    }
    $("#btn_classification").attr('disabled',true);
    $('#input_result').val("正在解析中...");
    $('#input_result_type').val("正在解析中...");
    $.get("/test/",{"alarm_content": alarm_content},
        function(ret){
        $("#btn_classification").attr('disabled',false);
            $('#input_result').val(ret);
            var result = JSON.parse(ret);
            if(result.data.type != null){
                $('#input_result_type').val(result.data.type);
            }else{
                console.log("can't parse result!");
            }
    });
}