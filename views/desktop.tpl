<!DOCTYPE HTML>
<html lang="es">
<head>    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
    <script type='text/javascript' src="http://maps.google.com/maps/api/js?sensor=false&.js&language=es"></script>
	<script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<script type="text/javascript" src="_static/js/settings-map.js"></script>

	<link rel="stylesheet" href="_static/css/estilos-desktop.min.css" />
	<link rel="icon" href="favicon.ico"/>
</head>

<body>

    <div id="contenido">
        <div id="header">
            <div id="logo"></div>
            <div id="status">última actualización: <span id="ultimaActualizacion">--</span><button id="salir">salir</div></div>
            
        </div>
        <div id="paneles">
            <div id="leftPanel">
                <div id="c9int" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cAlco" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cAlem" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cCabi" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cCerr" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cCord" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cCorr" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cIlli" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cInde" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cJuan" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cLibe" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cAvdm" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cPase" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cPell" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cPuey" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cRiva" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
                <div id="cSanm" class="corredor shadow listado cargando"><span class="titulo">...</span><div class="icono"></div></div>
            </div>

            <div id="rightPanel">
                <div id="mapa"> </div>
                <div id="cuadroOperador">
                    <!-- ventana corredores -->
                    <div id="corredores">
                        <div class="titulo">---</div>
                                               
                        <div class="flecha capital"></div>                        
                        <div class="etiquetasCapital"></div>
                        <div class="corredoresCapital"></div>
                        <div id="avisoCapital"></div>
                        <div id="panelesCapital"></div>

                        <div class="flecha provincia"></div>                        
                        <div class="etiquetasProvincia"></div>
                        <div class="corredoresProvincia"></div>
                        <div id="avisoProvincia"></div>
                        <div id="panelesProvincia"></div>

                    </div>
                    

                    <!-- ventana de edicion -->
                    <div id="edicion">

                        <div class="titulo">Estado<div class="tuerca"></div></div>

                        <div id="seleccioneTrayecto">Seleccione el trayecto<br>que desea visualizar</div>

                        <form action="javascript:actualizoRegistro()">

                            <input id="anomaly_frm" type="text" value="" hidden>

                            <div class="fila">
                                <div class="subtitulo">Trayecto</div>
                                <div class="dato" id="trayecto_frm">--</div>
                            </div>


                            <div class="fila">
                                <div class="izquierda">
                                    <div class="subtitulo">Sentido</div>
                                    <div class="dato" id="sentido_frm">--</div>
                                </div>
                                <div class="derecha">
                                    <div class="subtitulo">Anomalía</div>
                                    <div class="dato" id="anomalia_frm">--</div>
                                </div>
                            </div>

                            <div class="fila">
                                <div class="izquierda">
                                    <div class="subtitulo">Tiempo</div>
                                    <div class="dato" id="tiempo_frm">--</div>
                                </div>
                                <div class="derecha">

                                    <div class="subtitulo">Demora</div>
                                    <div class="dato" id="demora_frm">--</div>
                                </div>
                            </div>

                            <div id="ingresar">
                                <div id="oculta">El trayecto seleccionado<br>no registra anomalía</div>

                                <div class="fila">
                                    <label>Corte</label>
                                    <select id="corte_frm">
                                        <option selected value="0">No Aplica</option>
                                        <option value="1">Corte parcial</option>
                                        <option value="2">Corte total</option>
                                    </select>
                                </div>

                                <div class="fila">
                                    <label>Causa</label>
                                    <select id="causa_frm">
                                        <option selected value="0">Seleccionar causa...</option>
                                    </select>
                                </div>
                                    
                                <div class="fila">
                                    <label>Descripción</label>
                                    <textarea id="descripcion_frm" rows="2" maxlength="140" placeholder="Ej. Manifestación en Arenales y Sta. Fe. Congestión en Libertador."></textarea> 

                                    <br>
                                </div>
                                <div class="fila inputs">
                                    <div id="mensajeStatus_frm"></div>
                                    <input id="reportar_frm" type="submit" value="REPORTAR">
                                    <input id="modificar_frm" type="submit" value="MODIFICAR" hidden>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

	<script type="text/javascript" src="_static/js/eventos-socket-desktop.js"></script>
	<script type="text/javascript">
        var map = new google.maps.Map(document.getElementById('mapa'), settingsItemsMap ); // Cargo mapa	
		var trafico = new google.maps.TrafficLayer();
  		trafico.setMap(map);
	</script>		
    <script type="text/javascript" src="_static/js/appDesktop.min.js"></script>
</body>
</html>