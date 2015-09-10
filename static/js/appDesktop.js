var corredores  = JSON.parse("{}");


// Trae JSON con listado de segmentos
var nombresDeCorredores = (function () {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "_static/data/segmentos.json",
        'dataType': "json",
        'success': function (data) {
            archivo = data;
        }
    });
    return archivo;
})(); 

// Trae JSON con listado de causas de una anomalia
var causasAnomalias = (function() {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "_static/data/causas.json",
        'dataType': "json",
        'success': function(data) {
            archivo = data;
            armoSelectAnomalias(data);
        }
    });
    return archivo;
})();

// arma el select con las anomalias leidas en "_static/data/causas.json" y arma el select dinectamente
function armoSelectAnomalias(datos) {
    for (var i = 0; i < datos.causas.length; i++) {
        $("#causa_frm").append('<option value="' + datos.causas[i].id + '">' + datos.causas[i].descripcion + '</option>');
    }

}

// hace el post a la base de datos
function actualizoRegistro() {
    var data = 'anomaly_id='+$("#anomaly_frm").val()+'&comentario='+$("#comentario_frm").val()+'&causa_id='+$("#causa_frm").val();
    $.ajax({
        type: "POST",
        url: "/index",
        data: data,
        success: function(msg) {
            if (msg === "guardado"){
                console.log("guardado con éxito");
                
            }else{
                console.log("Error: ", msg);
            }
        },
        contentType: 'application/x-www-form-urlencoded'
    });
}

// mapa a full height
$("#logo").click(function() {
    $("#mapa").animate({
        height: "100%"
    }, 200);
});

// mapa comprimido
$(".corredor").click(function() {
    $("#seleccioneTrayecto").css("display","inline");    
    $("#oculta").css("display", "none");
    var corredor = $(this);
    if ( $(this).hasClass("cargando") === false){
        $("#mapa").animate({
            height: "300px"
        }, 200);
    }else{
        $("#mapa").animate({
            height: "100%"
        }, 200);
    };
    if ( $(this).hasClass("cargando") === false){
        abreDetalleCorredor(corredor);
    };

});

// arma el detalle de todo el corredor en la ventana del operador
// usa todos los valores cargados en @var nombresDeCorredores
function abreDetalleCorredor(data){
    $("#cuadroOperador").fadeOut(0);
    var titulo = data.find(".titulo")
    $("#corredores .titulo")[0].innerHTML = titulo[0].innerHTML;
    // armo los corredores
    llenaPantallaActualizacion(titulo.parent()[0].id);
    $("#cuadroOperador").fadeIn("fast");

}


function llenaPantallaActualizacion(corredor){

    var cantidad = 0; 
    var cor = ""; 
    var cappro = [0,0];
    var corPro = "";
    var corCap = "";

    // Vacío ventana
    $("#corredores .etiquetasCapital").html("");
    $("#corredores .etiquetasProvincia").html("");
    $("#corredores #corredorCapital").html("");
    $("#corredores #corredorProvincia").html("");
    $("#avisoProvincia").html("");
    $("#avisoCapital").html("");
    $("#corredores .corredoresCapital").html("");
    $("#corredores .corredoresProvincia").html("");
    $("#panelesProvincia").html("");
    $("#panelesCapital").html("");


    if ( typeof(corredores[corredor].provincia) != "undefined"){
        cantidad = corredores[corredor].provincia.length;
        cor = corredores[corredor].provincia;
        corPro = corredores[corredor].provincia;
        cappro[1] = 1;

    }

    if ( typeof(corredores[corredor].capital) != "undefined"){
        cantidad = corredores[corredor].capital.length;
        cor = corredores[corredor].capital;
        corCap = corredores[corredor].capital;
        cappro[0] = 1;
    }


    // armo etiquetas
    for (var i = 0 ; i < cor.length ; i++){
        var alineado = "cen";
        if (i === 0){alineado = "izq";}
        $("#corredores .etiquetasCapital").append('<div class="nombreCorredor ' + alineado + '">' + nombresDeCorredores[cor[i]].nombreSegmento.split(" - ")[0] + '</div>' );
        $("#corredores .etiquetasProvincia").append('<div class="nombreCorredor ' + alineado + '">' + nombresDeCorredores[cor[i]].nombreSegmento.split(" - ")[0] + '</div>' );
    }
    $("#corredores .etiquetasCapital").append('<div class="nombreCorredor der">' + nombresDeCorredores[cor[cor.length-1]].nombreSegmento.split(" - ")[1] + '</div>');
    $("#corredores .etiquetasProvincia").append('<div class="nombreCorredor der">' + nombresDeCorredores[cor[cor.length-1]].nombreSegmento.split(" - ")[1] + '</div>');

    if (cappro[1] === 0 ){
        $("#avisoProvincia").append('<div id="aviso">El trayecto no tiene dirección hacia Provincia</div>');        
    }
    if (cappro[0] === 0 ){
        $("#avisoCapital").append('<div id="aviso">El trayecto no tiene dirección hacia Capital</div>');
    }

        
    //armo segmentos
    for (var i = 0 ; i < cor.length ; i++){
        if (cappro[0] === 0 ){
            $("#corredores .corredoresCapital").append('<div class="corredor segmento estado0"></div>' );
        }else{
            $("#corredores .corredoresCapital").append('<div class="corredor segmento estado' + nombresDeCorredores[corCap[i]].anomalia + '"></div>' );
            $("#panelesCapital").append('<div class="panel" id="c'+corCap[i]+'"><div class="filaPanel">Aviso de anomalia<div class="datoPanel">Hace '+nombresDeCorredores[corCap[i]].duracion_anomalia+' min.</div></div><div class="filaPanel">Tiempo del trayecto<div class="datoPanel">'+ nombresDeCorredores[corCap[i]].tiempo +'</div></div><div class="filaPanel">Demora<div class="datoPanel">'+ ((nombresDeCorredores[corCap[i]].indicador_anomalia)*100).toFixed(1) +' </div></div><div class="filaPanel">Causa<div class="datoPanel">'+nombresDeCorredores[corCap[i]].causa+'</div></div></div>');
        }
        
        if (cappro[1] === 0 ){
            $("#corredores .corredoresProvincia").append('<div class="corredor segmento estado0"> </div>' );
        }else{
            $("#corredores .corredoresProvincia").append('<div class="corredor segmento estado' + nombresDeCorredores[corPro[i]].anomalia + ' "></div>' );
            $("#panelesProvincia").append('<div class="panel" id="c'+corPro[i]+'"><div class="filaPanel">Aviso de anomalia<div class="datoPanel"> Hace '+nombresDeCorredores[corPro[i]].duracion_anomalia+' min.</div></div><div class="filaPanel">Tiempo del trayecto<div class="datoPanel">'+ nombresDeCorredores[corPro[i]].tiempo +'</div></div><div class="filaPanel">Demora<div class="datoPanel">'+ ((nombresDeCorredores[corPro[i]].indicador_anomalia)*100).toFixed(1)+' </div></div><div class="filaPanel">Causa<div class="datoPanel">'+nombresDeCorredores[corPro[i]].causa+'</div></div></div>');
        }

        
    }

    // agrega el listener al panel que se acaba de agregar.
    $(".panel").click(function() {
        llenoPantallaEdicion(this.id.replace("c",""));
        $("#seleccioneTrayecto").css("display","none");

    });

}


//llena la pantalla de edicion del sector seleccionado
function llenoPantallaEdicion(idSegmento){

    $("#trayecto_frm").html(nombresDeCorredores[idSegmento].nombreSegmento);
    $("#sentido_frm").html(nombresDeCorredores[idSegmento].sentido);
    $("#anomalia_frm").html(nombresDeCorredores[idSegmento].duracion_anomalia);
    $("#tiempo_frm").html(nombresDeCorredores[idSegmento].tiempo + " min.");
    $("#demora_frm").html(((nombresDeCorredores[idSegmento].indicador_anomalia)*100).toFixed(1)+"%");

    if ( nombresDeCorredores[idSegmento].anomalia_id != 0 ) {

        // oculto cartel de edicion..
        $("#oculta").css("display", "none");

        
        $("#corte_frm").val('1');
        $("#causa_frm").val('4');
        $("#descripcion_frm").val("");
    }else{
        // muestro cartel de edicion
        $("#oculta").css("display", "inline");
    };


}

// pone los titulos a la botonera y completa el JSON
// esta funcion se llama cada vez que socket recibe un mensaje 
function actualizacionDesktop(data) {



    var segmentosC = [];
    var segmentosP = [];
    var texto = "";

    $("#" + data.id + " .titulo").html(data.nombre);
    $("#" + data.id).removeClass("cargando");

    if (data.segmentos_capital.length != 0){
            console.log (data.segmentos_capital);
        for (var i = 0; i < data.segmentos_capital.length ; i++){
            nombresDeCorredores[data.segmentos_capital[i].id].sentido = "capital";

            nombresDeCorredores[data.segmentos_capital[i].id].anomalia = data.segmentos_capital[i].anomalia;
            nombresDeCorredores[data.segmentos_capital[i].id].anomalia_id = data.segmentos_capital[i].anomalia_id;
            nombresDeCorredores[data.segmentos_capital[i].id].causa = data.segmentos_capital[i].causa;
            nombresDeCorredores[data.segmentos_capital[i].id].causa_id = data.segmentos_capital[i].causa_id;
            nombresDeCorredores[data.segmentos_capital[i].id].duracion_anomalia = data.segmentos_capital[i].duracion_anomalia;
            nombresDeCorredores[data.segmentos_capital[i].id].id = data.segmentos_capital[i].id;
            nombresDeCorredores[data.segmentos_capital[i].id].indicador_anomalia = data.segmentos_capital[i].indicador_anomalia;
            nombresDeCorredores[data.segmentos_capital[i].id].tiempo = data.segmentos_capital[i].tiempo;
            nombresDeCorredores[data.segmentos_capital[i].id].velocidad = data.segmentos_capital[i].velocidad;

            segmentosC.push(data.segmentos_capital[i].id);

        }
        texto = '"capital":['+segmentosC.toString()+']'
    };

    if (data.segmentos_provincia.length != 0){
        for (var p = 0; p < data.segmentos_provincia.length ; p++){
            nombresDeCorredores[data.segmentos_provincia[p].id].sentido = "provincia";

            nombresDeCorredores[data.segmentos_provincia[p].id].anomalia = data.segmentos_provincia[p].anomalia;
            nombresDeCorredores[data.segmentos_provincia[p].id].anomalia_id = data.segmentos_provincia[p].anomalia_id;
            nombresDeCorredores[data.segmentos_provincia[p].id].causa = data.segmentos_provincia[p].causa;
            nombresDeCorredores[data.segmentos_provincia[p].id].causa_id = data.segmentos_provincia[p].causa_id;
            nombresDeCorredores[data.segmentos_provincia[p].id].duracion_anomalia = data.segmentos_provincia[p].duracion_anomalia;
            nombresDeCorredores[data.segmentos_provincia[p].id].id = data.segmentos_provincia[p].id;
            nombresDeCorredores[data.segmentos_provincia[p].id].indicador_anomalia = data.segmentos_provincia[p].indicador_anomalia;
            nombresDeCorredores[data.segmentos_provincia[p].id].tiempo = data.segmentos_provincia[p].tiempo;
            nombresDeCorredores[data.segmentos_provincia[p].id].velocidad = data.segmentos_provincia[p].velocidad;

            segmentosP.push(data.segmentos_provincia[p].id);
        }
        if (texto != ""){
            texto = texto + ',"provincia":['+segmentosP.toString()+']';
        }else{
            texto = '"provincia":['+segmentosP.toString()+']';
        }
        
    };

    var datos =JSON.parse('{'+texto+'}');
    corredores[data.id] = datos;

}
