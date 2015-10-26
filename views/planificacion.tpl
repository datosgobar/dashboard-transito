<!DOCTYPE HTML>
<html>
<head>    
    <title>Planificacion</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <script type="text/javascript" src="_static/js/socket.io.js"></script>
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_static/css/estilos.min.css" />
    <link rel="icon" href="favicon.ico"/>
</head>
<body>
    <div>
        <h2 style="color:white">ESTADISTICAS MENSUALES</h2>
        <select id="filtros">
          % for grafico in graficos_ids:
            <option id="{{ grafico['filename'] }}">{{ grafico['name'] }}</option>
          % end 
        </select>
        <h1 style="color:white"></h1>
        <img id="select_img"></img>
    </div>
    <script type="text/javascript">
      //var graficos = {{ graficos_ids }}
      $('body').on('change', '#filtros', function (){
        $( "#filtros option:selected").attr('id', function(a, id_selc, c){
          $("#select_img").attr("src", "_static/img/" + id_selc + ".png");
        })
      });

      $( document ).ready(function() {
        var id_selc = $( "#filtros option:selected").attr('id')
        $("#select_img").attr("src", "_static/img/" + id_selc + ".png");
      });
    </script>
</body>
</html>


