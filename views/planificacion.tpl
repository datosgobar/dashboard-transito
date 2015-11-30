<!DOCTYPE HTML>
<html>
<head>    
    <title>Planificacion</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />

    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_static/css/estilos.min.css" />
    <link rel="icon" href="favicon.ico"/> 
    <link rel="stylesheet" href="_static/css/estilos-menu.min.css" />
</head>    
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

            <select id="periodos"></select>
            
            <select id="list_corredores"></select>
            <h1 id="title" style="color:white"></h1>

            <div id="entry"></div>

        </div>
    </div>

    <script type="text/javascript">

      String.prototype.titleCase = function(){
        return this.replace(/\w\S*/g, function(txt){
          return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
      };

      String.prototype.twoReplace = function(r1, r2){
        return this.replace(r1, r2).replace(r1, r2)
      }

      String.prototype.replaceTitle = function(){
        return this.twoReplace("_", " ").titleCase()
      }

      var get_endpoint = function (url){
        var archivo = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': url,
            'dataType': "json",
            'success': function (data){
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
      
      $.each(periodos, function (i, periodo){
        periodo = periodo.replace("_", " ")
        $('#periodos').append($('<option>',{
          value: periodo,
          text : periodo,
          id : periodo
        }));
      });

      $.each(corredores, function (i, corredor){
        corredor = corredor.replaceTitle()
        $('#list_corredores').append($('<option>',{
          value: corredor,
          text : corredor,
          id : corredor
        }));
      });

      var insert_graficos = function(id){

        remove_elem(['h2', 'embed'])
        console.log(id)
        
        var graphs = {'graficos':[]}
        select_periodo = $("#periodos option:selected").attr('id').replace(" ", "_")

        if (id == "generales"){
          $("#list_corredores").hide()
          graphs = get_endpoint('/generales' + "/" + select_periodo)
        } else {
          select_corredor = $("#list_corredores option:selected").attr('id').twoReplace(" ", "_").toLowerCase()
          $("#list_corredores").show()
          graphs = get_endpoint('/corredores' + "/" + select_periodo + "/" + select_corredor)
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

      $('body').on('change', '#list_corredores', function (){
        $( "#list_corredores option:selected").attr('id', function(a, id_selc, c){
          insert_graficos("corredores")
        })
      });

      $( document ).ready(function() {
        insert_graficos("generales")
      });

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
</body>
</html>