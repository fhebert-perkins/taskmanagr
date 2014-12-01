jQuery(document).ready(function($) {
    $(".clickableRow").click(function() {
        window.document.location = $(this).attr("href");
    });
    $(".deletebutton").click(function(){
        if (window.confirm("Are you absolutely sure?")){
            $.get("/delproject/"+$(this).attr("pid")+"?continue=YES", function (data){
                if (data == "true") {
                    window.document.location = "/list"
                }
            });
        } else {
            window.document.location = "/list"
        }

    });
    $(".completed").click(function(){
        if ($(this).is(":checked")){
            console.log("making complete")
            $.get("/complete/"+$(this).attr("tid"), function(data){
                console.log(data);
            });
        } else {
            console.log("making uncomplete")
            $.get("/uncomplete/"+$(this).attr("tid"), function(data){
                console.log(data);
            });
        }
    });
});
