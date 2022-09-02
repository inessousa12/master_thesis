<?php
	ini_set('display_errors', 1);
?>

<div class="add_station_popup">
    <div class='station'>
        <h3>New Station</h3>
        <div class='popup_inline'>
            <div class='first_column'>
                <label class='form-label'>Name:</label>
                <input class='form-input-text' type='text' name='name' placeholder='Insert station name' require/>
                <label class='form-label'>Latitude:</label>
                <input class='form-input-text' type='text' name='latitude' placeholder='Insert latitude' require />
                <label class='form-label'>Longitude:</label>
                <input class='form-input-text' type='text' name='longitude' placeholder='Insert longitude' require />
            </div>
            <div class='second_column'>
                <label class='form-label'>Devices:<img src='../img/add.png' class='img_button add_img' alt='Add Device'></label>
                <span>
                    <select class="device_select"><select>
                    <select name='status'>
                        <option value='' disabled selected>Select your option</option>
                        <option value='Connected'>Connected</option>
                        <option value='Disconnected'>Disconnected</option>
                        <option value='Inactive'>Inactive</option>
                    </select>
                </span>
            </div>
        </div>
    </div>
</div>