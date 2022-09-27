<?php
	include "php_includes/openconn.php";
	ini_set('display_errors', 1);
	session_start();
	$_SESSION['query_par'] = 'ALL';
?>

<!DOCTYPE html>
<html>
	<head>
		<title>AQUAMON</title>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"/>
		<link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css"/>
		<link rel="stylesheet" type="text/css" href="css/aquamon.css">
		<link rel="icon" href="img/aquamon-icon.png" type="image/png" sizes="16x16">
		<link rel="stylesheet" type="text/css" href="https://js.api.here.com/v3/3.1/mapsjs-ui.css" />
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
		<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet"	/>
		<link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet"/>
		<link href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.1.0/mdb.min.css" rel="stylesheet" />
		
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.1.0/mdb.min.js"></script>
		<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
		<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
		<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
		<script src="https://code.getmdl.io/1.3.0/material.min.js"></script>
		<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
		<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-core.js"></script>
		<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-service.js"></script>
		<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-ui.js"></script>
		<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-mapevents.js"></script>
		<script type="text/javascript">
			var php_var = "<?php echo $_SERVER['SERVER_NAME']; ?>";
		</script>
		<script src="js/sidebar_slide.js"></script>
		<script src="js/sidebar.js"></script>
		<script src="js/map.js"></script>
		<script src="js/measurement_graphs.js"></script>
		<script src="js/bd_functions.js"></script>
		
		
	</head>
	



	<body>
		<header class="simple_header">
			<img id="header_img" src="img/header3.svg" alt="header">
		</header>

		<div class="modal fade" id="config_modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
			<div class="modal-dialog modal-dialog-centered modal-lg" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="exampleModalLongTitle">Configure Stations</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					<div class="modal-body">
						<div class="inline-buttons">
							<button class="mdl-button mdl-js-button mdl-button--raised button" id="add_station">Add Station</button>
							<button class="mdl-button mdl-js-button mdl-button--raised button" id="delete_station">Delete Station</button>
							<button class="mdl-button mdl-js-button mdl-button--raised button" id="edit_station">Edit Station</button>
							<button class="mdl-button mdl-js-button mdl-button--raised button" id="add_metric">Add Metric</button>
							<button class="mdl-button mdl-js-button mdl-button--raised button" id="add_device">Add Device</button>
						</div>
						
						<h2>Choose what to configure above</h2>
						<div class="popup_body"></div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary close_modal" data-dismiss="modal">Close</button>
						<button type="button" class="btn btn-primary save_modal" data-dismiss="modal">Save changes</button>
					</div>
				</div>
			</div>
		</div>

		<div class="alert alert-success" role="alert"></div>

		<div class="alert alert-danger" role="alert"></div>

		<!-- No header, and the drawer stays open on larger screens (fixed drawer). -->
		<div class="mdl-layout mdl-js-layout mdl-layout--fixed-drawer">
			<div id="drawer" class="mdl-layout__drawer">
				
				<div class="demo-list-action mdl-list">
					<div class="mdl-list__item">

						<ul id="sidebar" class="entity-list group-list mdl-list ">
							<button class="mdl-button mdl-js-button mdl-button--raised button" id="model_button" data-toggle="modal" data-target="#config_modal">Config</button>
							<div id="side_list">
							</div>
							<!-- <div class="mdh-expandable-search">
								<i class="material-icons">search</i>
								<input class="mdl-textfield__input search_bar_input" placeholder ="Search" type="text" id="sample6">
								<label class="mdl-textfield__label" for="sample-expandable"></label>
							</div> -->
						</ul>
					</div>
				</div>
			</div>

			<main class="mdl-layout__content">
				<div class="mdl-grid">
					<div class="mdl-cell mdl-cell--12-col mdl-cell--4-col-tablet">

						<div class="mdl-grid">    
							<div class="mdl-cell mdl-cell--6-col">
								<div class="map" id="map"></div>
							</div>

							<div class="mdl-cell mdl-cell--6-col">
								<div id="realtime-chart">

									<?php
										echo '<iframe src="http://'. $_SERVER['SERVER_NAME'] . ':3000/d-solo/ORwev7L7z/quality-mean?orgId=1&refresh=5s&from=now-15m&to=now&panelId=2" width="450" height="300" frameborder="0"></iframe>' .
											'<div class="mdl-grid"><div class="mdl-cell mdl-cell--6-col">' .
											'<iframe src="http://' . $_SERVER['SERVER_NAME'] . ':3000/d-solo/zeBK2SPnz/number-of-outliers?&refresh=5s&from=now-15m&to=now&orgId=1&panelId=2" width="200" height="150" frameborder="0"></iframe>' .
											'</div><div class="mdl-cell mdl-cell--6-col">' .
											'<iframe src="http://' . $_SERVER['SERVER_NAME'] . ':3000/d-solo/-oTA2IEnz/number-of-omissions?orgId=1&refresh=5s&from=now-15m&to=now&panelId=2" width="200" height="150" frameborder="0"></iframe>' .
											'</div></div>';
									?>
								
								</div>
								
							</div>
						</div>
					</div>
				</div>

				<!-- <div id="node_name">
				</div> -->
				
				<div class="mdl-grid">
					<div class="mdl-cell mdl-cell--12-col mdl-cell--4-col-tablet">

						<div class="mdl-grid"> 
							<div class="mdl-cell mdl-cell--12-col">
								<div class="chart"></div>
								</div>
							</div>   
							<!-- <div class="mdl-cell mdl-cell--4-col">
								<div id="rssi-chart"></div>
							</div>
							<div class="mdl-cell mdl-cell--4-col">
								<div id="bar-chart"></div>
							</div> -->
						</div>  
					</div>
				</div>

				
			</main>
		</div>

	</body>
</html>
