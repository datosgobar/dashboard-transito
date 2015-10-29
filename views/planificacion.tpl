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
        <select id="filtros"></select>
        <h1 id="title" style="color:white"></h1>
        <img id="select_img"></img>
    </div>
    <script type="text/javascript">

      var graficos = (function () {
          var archivo = null;
          $.ajax({
              'async': false,
              'global': false,
              'url': "/info_graficos",
              'dataType': "json",
              'success': function (data) {
                  archivo = data;
              }
          });
          return archivo['graficos'];
      })();
      
      $.each(graficos, function (i, grafico){
          $('#filtros').append($('<option>',{
              value: grafico.name,
              text : grafico.name,
              id : grafico.filename
          }));
      });
      
      $('body').on('change', '#filtros', function (){
        $( "#filtros option:selected").attr('id', function(a, id_selc, c){
          for (var i=0;i<graficos.length;i++){
            if (graficos[i].filename == id_selc){
              $("h1").text(graficos[i].title)
              $("#select_img").attr("src", graficos[i].filename);
            }
          }
        })
      });

      $( document ).ready(function() {
        var id_selc = $( "#filtros option:selected").attr('id')
        for (var i=0;i<graficos.length;i++){
          if (graficos[i].filename == id_selc){
            $("h1").text(graficos[i].title)
            $("#select_img").attr("src", graficos[i].filename);
          }
        }        
      });

    </script>
</body>
</html>


