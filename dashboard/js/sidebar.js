function verify_status(status){
    if (status == "Connected"){
        return ["device-connected","Connected"];
    } else if (status == "Inactive"){
        return ["device-partial-connected", "Inactive"];
    } else if (status == "Disconnected"){
        return ["device-disconnected", "Disconnected"];
    }
    
}

document.addEventListener('DOMContentLoaded', function() {
    function get_sidebar() {
        $.ajax({
            type: "POST",
            url: "../php_includes/db_sidebar.php",
            data: {
                res: 1
            },
            success: function(data) {
                //show success message
                
                data = $.parseJSON(data);
                stations = []
                for (var i = 0; i < data.length; i++){
                    if (!stations.includes(data[i].name)) {
                        stations.push(data[i].name);
                    }
                }

                $("div #side_list").empty();

                

                for (var j = 0; j < stations.length; j++) {
                    var new_html = '<li class="mdl-list__item mdl-list__item--two-line group-item" id="station_' + j + '" name="group_'+j+'">'
                        + '<span class="mdl-list__item-primary-content">'
                        + '<span>' + stations[j] + '</span>'
                        + '<span class="mdl-list__item-sub-title" name="' + stations[j] + '"></span>'
                        + '</span>'
                        + '<span class="mdl-list__item-secondary-content"></span>'
                        + '</li><ul class="entity-list device-list mdl-list" name="' + stations[j] + '"></ul>';
                    $("#side_list").append(new_html);
                }

                for (var i = 0; i < data.length; i++) {
                    if(data[i].metric_name != null) {
                        var s = verify_status(data[i].status);
                        member_html = '<li class="mdl-list__item mdl-list__item--two-line" id="' + data[i].name + '" name="'+ data[i].metric_name +'">'
                        + '<div id="inline">'
                        + '<input class="checkbox_var" id="' + data[i].name + '" type="checkbox" name="' + data[i].metric_name + '"/>' 
                        + '<label class="form-control">'   
                        + '<span class="mdl-list__item-primary-content">'
                        + '<span class="entity-name">'+ data[i].metric_name +'</span>'
                        + '<span class="mdl-list__item-sub-title"><span class="'+s[0]+'"></span>'+s[1]+'</span>'
                        + '</label>'
                        + '</div>'
                        + '</li>';

                        $("ul[name='"+data[i].name+"']").append(member_html);
                    }
                }
                

                for (var i = 0; i < stations.length; i++) {
                    $("span[name='"+stations[i]+"']").append($("ul[name='"+stations[i]+"'] li").length + " devices");
                }
            },
            error: function(data) {
                $(".alert-danger").show().delay(5000).fadeOut();
                $(".alert-danger").empty();
                $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
            }
        });
    }
    
    // setInterval(get_sidebar, 3000);
    get_sidebar();

    $(document).on("click", ".add_img", function() {
        $.ajax({
            type: "POST",
            url: "../php_includes/get_metrics.php",
            data: {metric: 1,
                    metric_echo: 1},
            success: function(data) {
                //show success message
                data = $.parseJSON(data);
                popup_add_html = "<span style='display: -webkit-box;'><select class='device_select'>";

                popup_add_html += "<option value='' disabled selected>Select your option</option>";
                
                for(var j = 0; j < data.length; j++) {
                    popup_add_html += "<option value='" + data[j].name + "'>" + data[j].name + "</option>";
                }

                popup_add_html += "</select><select name='status'><option value='' disabled selected>Select your option</option>" +
                "<option value='Connected'>Connected</option><option value='Disconnected'>Disconnected</option><option value='Inactive'>Inactive</option></select>" +
                "<img class='img_button delete_device' src='../img/close.png' alt='Delete Device'></span>"
    
                if($(".second_column").length > 0) {
                    $(".second_column").append(popup_add_html);
                } else if($(".add_device_add").length > 0){
                    $(".add_device_add").append(popup_add_html);
                }
                            
            },
            error: function(data) {
                $(".alert-danger").show().delay(5000).fadeOut();
                $(".alert-danger").empty();
                $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
            }
        });
    });

    $(document).on("click", ".delete_device", function() {
        $(this).parent().remove();
    })

    $(document).on("click", "#delete_station_button", function() {
        var station_name = $(this).parent().parent().attr("id");
        $(this).parent().parent().remove();

        $.ajax({
            type: "POST",
            url: "../php_includes/delete_station.php",
            data: {station_name: station_name},
            success: function(data) {
                //show success message
                $(".popup_body").append("<p style='color:green; text-align:center;' id='success_msg'>Successfully deleted a station!</p>");
                $("#success_msg").show().delay(5000).fadeOut();
                            
            },
            error: function(data) {
                $(".popup_body").append("<p style='color:green; text-align:center;' id='error_msg'>Something went wrong, please try again.</p>");
                $("#error_msg").show().delay(5000).fadeOut();
            }
        });
    })

    $(document).on("click", "#delete_station", function() {
        $(".popup_body").load("../php_includes/delete_station_page.php");
        $(".save_modal").removeAttr('id');
        $(".save_modal").attr("id", "delete_station_modal");
    })

    $(document).on("click", "#edit_station", function() {
        $(".popup_body").load("../php_includes/edit_station_page.php");
        $(".save_modal").removeAttr('id');
        $(".save_modal").attr("id", "edit_station_button");
    })

    $(document).on("change", ".select_station", function() {
        $.ajax({
            type: "POST",
            url: "../php_includes/get_station.php",
            data: {station_name: $(".select_station").val(),
                    metric: 1}, //to get all metrics
            success: function(data) {
                //show success message
                data = $.parseJSON(data);

                $(".edit_station_add").empty();
                station = $(".select_station").val();

                if(data.station[0].metric_name != null) {

                    popup_edit_html = "<div class='station' id='" + station + "'><span class='station_inline'><h3>" + station + "</h3></span>";
                    popup_edit_html += "<div class='popup_inline'><div class='first_column'><label class='form-label'>Name:</label>" +
                    "<input class='form-input-text' type='text' value='" + station + "' name='name' /><label class='form-label'>Latitude:</label>" +
                    "<input class='form-input-text' type='text' value='" + data.station[0].latitude + "' name='latitude' placeholder='Insert latitude' require />" +
                    "<label class='form-label'>Longitude:</label><input class='form-input-text' type='text' value='" + data.station[0].longitude + "' name='longitude' placeholder='Insert longitude' require /></div>" +
                    "<div class='second_column' name='" + station + "'><label class='form-label'>Devices:</label></div></div></div>";
                    $(".edit_station_add").append(popup_edit_html);

                    for(var i = 0; i < data.station.length; i++) {
                        popup_edit_html = "<span id='device_info'><select class='device_select'>"
                        
                        for(var j = 0; j < data.metrics.length; j++) {
                            if(data.station[i].metric_name == data.metrics[j].name) {
                                popup_edit_html += "<option value='" + data.metrics[j].name + "' id='" + data.station[i].id + "' selected>" + data.metrics[j].name + "</option>";
                            } else {
                                popup_edit_html += "<option value='" + data.metrics[j].name + "' id='" + data.station[i].id + "'>" + data.metrics[j].name + "</option>";
                            }                        
                        }
                        popup_edit_html += "</select><select name='status'><option value='' disabled selected>Select your option</option><option value='Connected'>Connected</option><option value='Disconnected'>Disconnected</option><option value='Inactive'>Inactive</option></select>" +
                        "<img class='img_button delete_device' src='../img/close.png' alt='Delete Device'></span>";

                        $("div[name='"+station+"']").append(popup_edit_html);
                        $("select[name=status]").val(data.station[i].status);
                    }   
                } else {
                    popup_edit_html = "<div class='station' id='" + station + "'><span class='station_inline'><h3>" + station + "</h3></span>";
                    popup_edit_html += "<div class='popup_inline'><div class='first_column'><label class='form-label'>Name:</label>" +
                    "<input class='form-input-text' type='text' value='" + station + "' name='name' /><label class='form-label'>Latitude:</label>" +
                    "<input class='form-input-text' type='text' value='" + data.station[0].latitude + "' name='latitude' placeholder='Insert latitude' require />" +
                    "<label class='form-label'>Longitude:</label><input class='form-input-text' type='text' value='" + data.station[0].longitude + "' name='longitude' placeholder='Insert longitude' require /></div>" +
                    "<div class='second_column' name='" + station + "'><label class='form-label'>No devices yet</label></div></div></div>";
                    $(".edit_station_add").append(popup_edit_html);
                }
            },
            error: function(data) {
                $(".alert-danger").show().delay(5000).fadeOut();
                $(".alert-danger").empty();
                $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
            }
        });
    })

    $(document).on("change", "#device", function() {
        $.ajax({
            type: "POST",
            url: "../php_includes/get_metrics.php",
            data: {metric: 1,
                    metric_echo: 1},
            success: function(data) {
                //show success message
                data = $.parseJSON(data);
                $(".add_device_add").empty();

                popup_add_html = "<label class='form-label'>Devices:<img src='../img/add.png' class='img_button add_img' alt='Add Device'></label>" +
                    "<span style='display: -webkit-box;'><select id='device_metric'><option value='' disabled selected>Select your option</option>";
                
                for(var j = 0; j < data.length; j++) {
                    popup_add_html += "<option value='" + data[j].name + "'>" + data[j].name + "</option>";
                }

                popup_add_html += "</select><select name='status'>" +
                    "<option value='' disabled selected>Select your option</option>" +
                    "<option value='Connected'>Connected</option>" +
                    "<option value='Disconnected'>Disconnected</option>" +
                    "<option value='Inactive'>Inactive</option>" +
                    "</select></span>";
    
                $(".add_device_add").append(popup_add_html);
                $(".save_modal").removeAttr('id');
                $(".save_modal").attr("id", "add_station_button");
                            
            },
            error: function(data) {
                $(".alert-danger").show().delay(5000).fadeOut();
                $(".alert-danger").empty();
                $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
            }
        });
    })

    $("#add_station").on("click", function() {        
        $(".popup_body").load("../php_includes/add_station_page.php");

        $.ajax({
            type: "POST",
            url: "../php_includes/get_metrics.php",
            data: {metric: 1,
                    metric_echo: 1},
            success: function(data) {
                //show success message
                data = $.parseJSON(data);
                console.log(data)

                popup_add_html = "<option value='' disabled selected>Select your option</option>";
                
                for(var j = 0; j < data.length; j++) {
                    popup_add_html += "<option value='" + data[j].name + "'>" + data[j].name + "</option>";
                }
    
                $(".device_select").append(popup_add_html);
                $(".save_modal").removeAttr('id');
                $(".save_modal").attr("id", "add_station_button");
                            
            },
            error: function(data) {
                $(".alert-danger").show().delay(5000).fadeOut();
                $(".alert-danger").empty();
                $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
            }
        });
    })

    $("#add_device").on("click", function() {        
        $(".popup_body").load("../php_includes/add_device_page.php");
        $(".save_modal").removeAttr('id');
        $(".save_modal").attr("id", "add_device_button");
    })

    $(document).on("click", "#add_metric", function() {
        $(".popup_body").load("../php_includes/add_metric_page.php");
        $(".save_modal").removeAttr('id');
        $(".save_modal").attr("id", "add_metric_button");
    })
});