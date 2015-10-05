<!DOCTYPE HTML>
<html>
<head>    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<script type="text/javascript" src="_static/js/app.min.js"></script>
	<link rel="stylesheet" href="_static/css/estilos.min.css" />
	<link rel="icon" href="favicon.ico"/>
</head>

<body>&nbsp;
    <div id="indicador"></div>
    <div id="cards">
        <img src="_static/css/img/beta.png" id="beta">
        <div id="sinAnomalia" class="oculta">
            En este momento no se registran anomalías<br>
            <img src="_static/css/img/loader.gif">
        </div>
        <div id="noResueltos">

        </div>
        <div id="resueltos">
        </div>
    </div>
	<script type="text/javascript" src="_static/js/eventos-socket.js"></script>
</body>
</html>


