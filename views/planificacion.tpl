<!DOCTYPE HTML>
<html>
<head>    
    <title>Planificacion</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <script type="text/javascript" src="_static/js/socket.io.js"></script>
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_static/css/estilos.min.css" />
    <link rel="icon" href="favicon.ico"/> 
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_static/css/estilos-desktop.min.css" />
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js" integrity="sha512-K1qjQ+NcF2TYO/eI3M6v8EiNYZfA95pQumfvcVrTHtwQVDG+aHRqLi/ETn2uB+1JqwYqVG3LIvdm9lj6imS/pQ==" crossorigin="anonymous"></script>    
</head>    
</head>
<body>

    <div id="header">
        <div id="logo"></div>
        <button id="salir">salir
    </div>
    <h2 style="color:white">ESTADISTICAS MENSUALES</h2>
    <select id="filtros">
      <option id='generales'>Generar Mensual</option>
      <option id='corredores'>Corredor Particular</option>
    </select>
    <h1 id="title" style="color:white"></h1>
    <img id="select_img"></img>
    </div>
    <div id='select_corredores'></div>
    <div id="entry"></div>
    <style type="text/css">
      h2 {
        font-family: "Arial";
        font-size: 21px;
      }
    </style>
    <script type="text/javascript">

      var get_endpoint = function (url) {
          var archivo = null;
          $.ajax({
              'async': false,
              'global': false,
              'url': url,
              'dataType': "json",
              'success': function (data) {
                  archivo = data;
              }
          });
          return archivo;
      };

      var graficos = get_endpoint('/graficos')
      var corredores = graficos['graficos']['corredores']


      var remove_elem  = function(elem){
        for (var i =0;i<elem.length;i++){
          $(elem[i]).remove()
        }
      }

      var periodos = graficos['graficos']['periodos']

      var insert_graficos = function(id){
        remove_elem(['h2', 'embed'])
        console.log(id)
        var graphs = {'graficos':[]}
        if (id == "generales"){
          graphs = get_endpoint('/generales' + "/" + periodos[0])
        }
        console.log(graphs.length)
        $.each(graphs['graficos'], function (i, grafico){
            $('#entry').append(
              $('<h2>',{
                text : grafico.title,
                style : "color:white"
              }),
              $('<embed>',{
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
          if(id_selc == 'corredores'){
            $("#select_corredores")
          }
        })
      });

      $( document ).ready(function() {
        insert_graficos("generales")
      });

    </script>
</body>
</html>