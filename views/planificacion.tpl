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
          <option id='mensuales'>MENSUALES</option>
          <option id='semanales'>SEMANALES</option>
        </select>
        <h1 id="title" style="color:white"></h1>
        <img id="select_img"></img>
    </div>
    <div id="entry"></div>
    <style type="text/css">
      h2 {
        font-family: "Arial";
        font-size: 21px;
      }
    </style>
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

      var remove_elem  = function(elem){
        for (var i =0;i<elem.length;i++){
          $(elem[i]).remove()
        }
      }

      var insert_graficos = function(periodo){
        remove_elem(['h2', 'img'])
        $.each(graficos[periodo], function (i, grafico){
            $('#entry').append(
              $('<h2>',{
                text : grafico.title,
                style : "color:white"
              }),
              $('<img>',{
                value: grafico.name,
                text : grafico.title,
                src : grafico.filename
              })
            )
        });
      }

      $('body').on('change', '#filtros', function (){
        $( "#filtros option:selected").attr('id', function(a, id_selc, c){
          insert_graficos(id_selc)
        })
      });

      $( document ).ready(function() {
        insert_graficos("mensuales")
      });

    </script>
</body>
</html>