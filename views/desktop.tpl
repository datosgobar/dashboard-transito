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
	<script type="text/javascript" src="_static/js/appDesktop.min.js"></script>
	<script type="text/javascript" src="_static/js/settings-map.js"></script>

	<link rel="stylesheet" href="_static/css/estilos-desktop.min.css" />
	<link rel="icon" href="favicon.ico"/>
</head>

<body>

<header>
    <div id="logo"></div>
    <div id="status">70 px</div>
</header>


    <div id="contenedor">
        <div id="listadoCorredores">
            <div id="c9int" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="c9ext" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cAlco" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cAlem" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cCabi" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cCord" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cCorr" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cIlli" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cInde" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cJuan" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cLibe" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cAvdm" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cPase" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cPuey" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cRiva" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
            <div id="cSanm" class="corredor shadow"><span class="titulo">...</span><div class="icono"></div></div>
        </div>

        <div id="detalleCorredores">
            <div id="mapa"> </div>
        </div>
    </div>


	<script type="text/javascript" src="_static/js/eventos-socket-desktop.js"></script>
	<script type="text/javascript">
		var map = new google.maps.Map(document.getElementById('mapa'), settingsItemsMap ); // Cargo mapa	
		var trafico = new google.maps.TrafficLayer();
  		trafico.setMap(map);
	</script>		
</body>
</html>