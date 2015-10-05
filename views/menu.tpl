<!DOCTYPE HTML>
<html>
<head>    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_static/css/estilos-menu.min.css" />

	<link rel="icon" href="favicon.ico"/> 

    <script type="text/javascript">

        $( document ).ready(function() {

            $("#salir").click(function() {
                window.location = "/logout";
            });

            //Vuelvo al home cuando clickeo el logo
            $("#logo").click(function() {
                window.location = "/";
            });
        });

    </script>

</head>

<body>
    <div id="contenido">
        <div id="header">
            <div id="logo"></div>
            <div id="status"><button id="salir">salir</div></div>
            
    </div>

    <div class="centro">
        <div class="top">
            
        </div>

         <div class="panelMenu centrado centro">
            <a href="/anomalies"><div class="buttonMenu" id="boton-videowall">Videowall</div></a>
            <a href="/desktop"><div class="buttonMenu" id="boton-operador">Operador</div></a>
            <a href=""><div class="buttonMenu" id="boton-planificacion" >Histórico</div></a>
        </div>

        <div class="bottom">
            
        </div>
       
    </div>
</body>
</html>


