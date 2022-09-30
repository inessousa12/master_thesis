$(document).ready(function(){
    $(".save_modal").on("click", function() {


        var id = $(".save_modal").attr("id");
        
        switch(id) {
            case "add_station_button":
                var station_name = $(".station").find("input[name=name]").val();
                var latitude = $(".station").find("input[name=latitude]").val();
                var longitude = $(".station").find("input[name=longitude]").val();

                if (station_name != '' && latitude != '' && longitude != '') {
                    $(".station").find(".device_select").each(function(){
                        var device_metric = $(".station").find(".device_select option:selected").val();
                        var device_status = $(".station").find("select[name=status] option:selected").val();

                        if(device_metric != '' && device_status != '') {
                            json_data = {
                                station_name: station_name, 
                                latitude: latitude,
                                longitude: longitude,
                                metric: device_metric, 
                                status: device_status
                            };


                            $.ajax({
                                type: "POST",
                                url: "../php_includes/add_station.php",
                                data: json_data,
                                success: function(data) {
                                    $('body').removeClass('modal-open');
                                    $('.modal-backdrop').remove();
                                    $(".alert-success").show().delay(5000).fadeOut();
                                    $(".alert-success").empty();
                                    $(".alert-success").append("<p>Successfully created a new station!</p>");
                                },
                                error: function(data) {
                                    $('body').removeClass('modal-open');
                                    $('.modal-backdrop').remove();
                                    $(".alert-danger").show().delay(5000).fadeOut();
                                    $(".alert-danger").empty();
                                    $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
                                }
                            });
                        } else {
                            $(".station").append("<p style='color:red'>Please fill out every section of the form.</p>");
                        }
                        
                    });
                } else {
                    $(".station").append("<p style='color:red'>Please fill out every section of the form.</p>");
                }


            case "delete_station_modal":
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();


            case "add_metric_button":
                var metric = $(".metric").find("input[name=name]").val();
                
                if(metric != '') {
                    $.ajax({
                        type: "POST",
                        url: "../php_includes/add_metric.php",
                        data: {metric_name: metric},
                        success: function(data) {
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $(".alert-success").show().delay(5000).fadeOut();
                            $(".alert-success").empty();
                            $(".alert-success").append("<p>Successfully added a new metric!</p>");
                        },
                        error: function(data) {
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $(".alert-danger").show().delay(5000).fadeOut();
                            $(".alert-danger").empty();
                            $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
                        }
                    });
                }


            case "edit_station_button":
                var station_name = $(".station").find("input[name=name]").val();
                var latitude = $(".station").find("input[name=latitude]").val();
                var longitude = $(".station").find("input[name=longitude]").val();

                if (station_name != '' && latitude != '' && longitude != '') {
                    $(".station").find(".device_select").each(function(){
                        var device_metric = $(".station").find(".device_select option:selected").val();
                        var device_status = $(".station").find("select[name=status] option:selected").val();

                        if(device_metric != '' && device_status != '') {
                            json_data = {
                                sensor_id: $(".station").find(".device_select option:selected").attr("id"),
                                original_station: $(".select_station").val(),
                                station_name: station_name, 
                                latitude: latitude,
                                longitude: longitude,
                                metric: device_metric, 
                                status: device_status
                            };

                            $.ajax({
                                type: "POST",
                                url: "../php_includes/edit_station.php",
                                data: json_data,
                                success: function(data) {
                                    $('body').removeClass('modal-open');
                                    $('.modal-backdrop').remove();
                                    $(".alert-success").show().delay(5000).fadeOut();
                                    $(".alert-success").empty();
                                    $(".alert-success").append("<p>Successfully edited a station!</p>");
                                },
                                error: function(data) {
                                    $('body').removeClass('modal-open');
                                    $('.modal-backdrop').remove();
                                    $(".alert-danger").show().delay(5000).fadeOut();
                                    $(".alert-danger").empty();
                                    $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
                                }
                            });
                        } else {
                            $(".station").append("<p style='color:red'>Please fill out every section of the form.</p>");
                        }
                        
                    });
                } else {
                    $(".station").append("<p style='color:red'>Please fill out every section of the form.</p>");
                }
            
            
            case "add_device_button":
                var station_name = $(".select_station option:selected").val();

                if (station_name != '') {
                    $(".add_device_add").find("#device_metric").each(function(){
                        var device_metric = $(".add_device_add").find("#device_metric option:selected").val();
                        var device_status = $(".add_device_add").find("select[name=status] option:selected").val();

                        if(device_metric != '' && device_status != '') {
                            json_data = {
                                station_name: station_name,
                                metric: device_metric, 
                                status: device_status
                            };

                            $.ajax({
                                type: "POST",
                                url: "../php_includes/add_device.php",
                                data: json_data,
                                success: function(data) {
                                    $('body').removeClass('modal-open');
                                    $('.modal-backdrop').remove();
                                    $(".alert-success").show().delay(5000).fadeOut();
                                    $(".alert-success").empty();
                                    $(".alert-success").append("<p>Successfully added a device to a station!</p>");
                                },
                                error: function(data) {
                                    $('body').removeClass('modal-open');
                                    $('.modal-backdrop').remove();
                                    $(".alert-danger").show().delay(5000).fadeOut();
                                    $(".alert-danger").empty();
                                    $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
                                }
                            });
                        } else {
                            $(".station").append("<p style='color:red'>Please fill out every section of the form.</p>");
                        }
                        
                    });
                } else {
                    $(".station").append("<p style='color:red'>Please fill out every section of the form.</p>");
                }
        }

        location.reload();
    });
});