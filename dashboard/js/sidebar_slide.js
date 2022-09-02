$(document).ready(function(){
    var open = true;
    var snd = false;

    setInterval(function(){
		$("#node_name").load('php_includes/session_setter.php');
	}, 500) /* (0.5 seconds)*/

    $('body').on('click','#sidebar li', function(e) {
        var name = $($($(this).children()[0]).children()[0]).text();
        var group= $(this).attr('name');

        $("ul[name='"+name+"']").slideToggle('slow', function() {
            if($("ul[name='"+name+"']").is(":visible")) {
                $("li[name='"+group+"']").css("transform", "scale(1.02)");
                $("li[name='"+group+"']").css("background-color", "rgb(131 166 181)");
            } else {
                $("li[name='"+group+"']").css("transform", "scale(1)");
                $("li[name='"+group+"']").css("background-color", "#b0bec5");
            
            }
        });
    });

})