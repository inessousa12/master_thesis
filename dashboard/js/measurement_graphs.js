var metric;

$(document).ready(function(){
    $('body').on('click','.device-list li', function(e) {
        $checkbox = $(this).find(".checkbox_var");
        if($checkbox[0].checked) {
            $checkbox.prop('checked', false);
        } else {
            $checkbox.prop('checked', true);
        }

        $(".chart").empty();

        $('.checkbox_var:checkbox:checked').each(function() {
            metric = $(this).attr("name");
            station = $(this).attr("id");

            chart_html = "<div class='chart_html' id='" + station + "' name='" + metric + "'><iframe src='http://localhost:3000/d-solo/JS-pOnL7z/all-measurements?orgId=1&var-sensor_name=" + station +
                    "&var-metric_name=" + metric + "&refresh=5s&from=now-15m&to=now&panelId=2' width='450' height='300' frameborder='0'></iframe>" +
                    "<div class='chart_config'><div class='form-check'>" +
                    "<input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault raw' value='raw'> " +
                    "<label class='form-check-label' for='raw'> Show only raw measurements</label></div>" +
                    "<div class='form-check'><input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault corrected' value='corrected'>" +
                    "<label class='form-check-label' for='corrected'> Show only corrected measurements</label>" +
                    "</div></div>";

            $(".chart").append(chart_html);
    
        })
    }); 

    $(document).on("click", ".chart_checkbox", function() {
        div_metric = $(this).parent().parent().parent().attr("name");
        div_station = $(this).parent().parent().parent().attr("id");
        console.log($(".chart_checkbox:checked"))

        if($(".chart_checkbox:checked").length == 0)  {
            $(".chart_html#" + div_station + "[name='" + div_metric + "']").empty();
            $(".chart_html#" + div_station + "[name='" + div_metric + "']").append("<iframe src='http://localhost:3000/d-solo/JS-pOnL7z/all-measurements?orgId=1&var-sensor_name=" + station +
            "&var-metric_name=" + metric + "&refresh=5s&from=now-15m&to=now&panelId=2' width='450' height='300' frameborder='0'></iframe>" +
            "<div class='chart_config'><div class='form-check'>" +
            "<input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault raw' value='raw'> " +
            "<label class='form-check-label' for='raw'> Show only raw measurements</label></div>" +
            "<div class='form-check'><input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault corrected' value='corrected'>" +
            "<label class='form-check-label' for='corrected'> Show only corrected measurements</label>" +
            "</div>");
        } else if($(".chart_checkbox:checked").length == 1) {
            var chart_show = $(".chart_checkbox:checked").val();
            console.log(chart_show);

            if(chart_show == "corrected") {
                $(".chart_html#" + div_station + "[name='" + div_metric + "']").empty();
                $(".chart_html#" + div_station + "[name='" + div_metric + "']").append("<iframe src='http://localhost:3000/d-solo/brx5d7L7k/correct-measurements?orgId=1&var-sensor_name=" + station +
                "&var-metric_name=" + metric + "&refresh=5s&from=now-15m&to=now&panelId=2' width='450' height='300' frameborder='0'></iframe>" +
                "<div class='chart_config'><div class='form-check'>" +
                "<input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault raw' value='raw'> " +
                "<label class='form-check-label' for='raw'> Show only raw measurements</label></div>" +
                "<div class='form-check'><input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault corrected' value='corrected' checked>" +
                "<label class='form-check-label' for='corrected'> Show only corrected measurements</label>" +
                "</div>");
            } else {
                $(".chart_html#" + div_station + "[name='" + div_metric + "']").empty();
                $(".chart_html#" + div_station + "[name='" + div_metric + "']").append("<iframe src='http://localhost:3000/d-solo/ZX8FO7Lnk/raw-measurements?orgId=1&var-sensor_name=" + station +
                "&var-metric_name=" + metric + "&refresh=5s&from=now-15m&to=now&panelId=2' width='450' height='300' frameborder='0'></iframe>" +
                "<div class='chart_config'><div class='form-check'>" +
                "<input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault raw' value='raw' checked> " +
                "<label class='form-check-label' for='raw'> Show only raw measurements</label></div>" +
                "<div class='form-check'><input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault corrected' value='corrected'>" +
                "<label class='form-check-label' for='corrected'> Show only corrected measurements</label>" +
                "</div>");
            }
        } else {
            $(".chart_html#" + div_station + "[name='" + div_metric + "']").empty();
            $(".chart_html#" + div_station + "[name='" + div_metric + "']").append("<iframe src='http://localhost:3000/d-solo/JS-pOnL7z/all-measurements?orgId=1&var-sensor_name=" + station +
            "&var-metric_name=" + metric + "&refresh=5s&from=now-15m&to=now&panelId=2' width='450' height='300' frameborder='0'></iframe>" +
            "<div class='chart_config'><div class='form-check'>" +
            "<input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault raw' value='raw' checked> " +
            "<label class='form-check-label' for='raw'> Show only raw measurements</label></div>" +
            "<div class='form-check'><input type='checkbox' class='form-check-input chart_checkbox' id='flexCheckDefault corrected' value='corrected' checked>" +
            "<label class='form-check-label' for='corrected'> Show only corrected measurements</label>" +
            "</div>");
        }
    })

})