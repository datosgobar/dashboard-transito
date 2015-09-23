<!DOCTYPE HTML>
<html lang="es">
<head>    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />

	<script type='text/javascript' src="http://maps.google.com/maps/api/js?sensor=false&.js&language=es"></script>
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<script type="text/javascript" src="_static/js/app.min.js"></script>
	<script type="text/javascript" src="_static/js/settings-map.js"></script>

	<link rel="stylesheet" href="_static/css/estilos.min.css" />
	<link rel="icon" href="favicon.ico"/>
</head>

<body>
    <div id="indicador"></div>
    <div id="cards">

        <div id="sinAnomalia" class="oculta">No se registran anomalías en los trayectos principales de la ciudad</div>
        <div id="noResueltos"></div>
        <div id="resueltos"></div>
    </div>
	<script type="text/javascript" src="_static/js/eventos-socket.js"></script>
</body>
</html>