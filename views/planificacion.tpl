<!DOCTYPE HTML>
<html>
<head>    
    <title>Planificacion</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <link rel="icon" href="favicon.ico"/> 
    <link rel="stylesheet" href="_static/css/estilos.min.css" />
    <link rel="stylesheet" href="_static/css/estilos-menu.min.css" />
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
</head>
<body>

    <div id="contenido">
        <div id="header">
            <div id="logo"></div>
            <div id="status"><button id="salir">salir</button></div>
        </div>

        <div class="centro">
            <h2 style="color:white">ESTADISTICAS MENSUALES</h2>
            
            <select id="filtros">
              <option id='generales'>Generar Mensual</option>
              <option id='corredores'>Corredor Particular</option>
            </select>

            <select id="periodos">
            </select>
            
            <select id="list_corredores">
            </select>

            <h1 id="title" style="color:white"></h1>
            <div id="entry"></div>

        </div>
    </div>
</body>
  <script type="text/javascript" src="_static/js/planificacion.js"></script>
</html>