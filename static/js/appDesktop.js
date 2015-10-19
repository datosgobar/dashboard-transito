var corredores  = JSON.parse("{}");
var anomaliasDescripcion = ["--","Intermedia","Grave"]


// Trae JSON con listado de segmentos
var nombresDeCorredores = (function () {
    corredores = {}  
    $.ajax({
        'async': false,
        'global': false,
        'url': "/segmentos",
        'dataType': "json",
        'success': function (data) {
            for (var i = 10; i<58;i++){
                corredores[parseInt(i).toString()] = {
                        "anomalia": "",
                        "causa": "",
                        "corredor": data['nombresDeCorredores'][i]['corredor'],
                        "corte": "",
                        "demora": "",
                        "descripcion": "",
                        "nombreSegmento": data['nombresDeCorredores'][i]['nombreSegmento'],
                        "sentido": "",
                        "tiempo": ""
                 }
            }
        }
    });
    return corredores;
})();

// Trae JSON con geolocalizacion de los corredores
var geolocalizacion = (function () {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "/geolocalizacion",
        'dataType': "json",
        'success': function (data) {
            archivo = data;
        }
    });
    return archivo['geolocalizacion'];
})(); 

// Trae JSON con listado de causas de una anomalia
var causasAnomalias = (function() {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "/causas",
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
    var comentario = $("#descripcion_frm").val();
    if (comentario === undefined || comentario === "undefined"){
        comentario = "";
    }

    var data = 'anomaly_id='+$("#anomaly_frm").val()+'&comentario='+comentario+'&causa_id='+$("#causa_frm").val()+'&tipo_corte='+$("#corte_frm").val();

    $.ajax({
        type: "POST",
        url: "/",
        data: data,
        success: function(msg) {
            $("#mensajeStatus_frm").show();
            if (msg === "guardado"){
                $("#mensajeStatus_frm").html("Guardado");
                $("#reportar_frm").hide();
                $("#modificar_frm").show();
                $("#mensajeStatus_frm").delay(1000).hide("slow");
            }else{
                $("#mensajeStatus_frm").html(msg);
                $("#mensajeStatus_frm").delay(3000).hide("slow");
            }
        },
        contentType: 'application/x-www-form-urlencoded'
    });
}

//Vuelvo al home cuando clickeo el logo
$("#logo").click(function() {
    window.location = "/";
});

function cierroEdicion (){
    $("#cuadroOperador").animate({
        top: "100%"
    }, 200);
    $(".corredor").removeClass("corredorActivo");
}

// complrime el mapa cuando abro un corredor
$(".corredor").click(function() {
    $("#seleccioneTrayecto").css("display","inline");    
    $("#oculta").css("display", "none");
    //panTo(nombresDeCorredores[idPanelClickeado].latlng);
    var corredor = $(this);
    if ( $(this).hasClass("cargando") === false && $(this).hasClass("corredorActivo")  === false ){
        abreDetalleCorredor(corredor);        
        $("#cuadroOperador").animate({
            top: "300px"
        }, 200);
    }else{
        $(this).removeClass("corredorActivo");
        cierroEdicion();

    };
    
});

// mapa a full height
$("#salir").click(function() {
    window.location = "/logout";
});


// arma el detalle de todo el corredor en la ventana del operador
// usa todos los valores cargados en @var nombresDeCorredores
function abreDetalleCorredor(data){
    $(".corredorActivo").removeClass("corredorActivo");
    $("#"+(data[0].id)).addClass("corredorActivo");
    $("#cuadroOperador").fadeOut(0);
    var titulo = data.find(".titulo")
    $("#corredores .titulo")[0].innerHTML = titulo[0].innerHTML;
    // armo los corredores
    llenaPantallaActualizacion(titulo.parent()[0].id);
    $("#cuadroOperador").fadeIn("fast");
    panTo(geolocalizacion[data[0].id].latlng);
}

// arma las cajas de los segmentos al clickear un corredor.
function llenaPantallaActualizacion(corredor){

    var cantidad = 0; 
    var cor = ""; 
    var cappro = [0,0];
    var corPro = "";
    var corCap = "";

    // variables con legibilidades de segmentos
    var duracionAnomalia  = 0,
        tiempoTrayecto = 0,
        demora = 0,
        causa = "";

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

    var htmlEtiquetasCapital = "";
    var htmlEtiquetasProvincia = "";

    //pregunto si hay segmentos de capital
    if ( typeof(corredores[corredor].capital) != "undefined"){
        cantidad = corredores[corredor].capital.length;
        cor = corredores[corredor].capital;
        corCap = corredores[corredor].capital;
        cappro[0] = 1;

        // armo etiquetas capital
        for (var i = 0 ; i < cor.length ; i++){
            var alineado = "cen";
            if (i === 0){alineado = "izq";}
            htmlEtiquetasCapital += ('<div class="nombreCorredor ' + alineado + '">' + nombresDeCorredores[cor[i]].nombreSegmento.split(" - ")[0] + '</div>' );
        }
        htmlEtiquetasCapital += ('<div class="nombreCorredor der">' + nombresDeCorredores[cor[cor.length-1]].nombreSegmento.split(" - ")[1] + '</div>');

    }

    $("#corredores .etiquetasCapital").append(htmlEtiquetasCapital);
    
    //pregunto si hay segmentos de provincia
    if ( typeof(corredores[corredor].provincia) != "undefined"){
        cantidad = corredores[corredor].provincia.length;
        cor = corredores[corredor].provincia;
        corPro = corredores[corredor].provincia;
        cappro[1] = 1;
    

        // armo etiquetas provincia
        for (var i = 0 ; i < cor.length ; i++){
            var alineado = "cen";
            if (i === 0){alineado = "izq";}
            htmlEtiquetasProvincia += ('<div class="nombreCorredor ' + alineado + '">' + nombresDeCorredores[cor[i]].nombreSegmento.split(" - ")[1] + '</div>' );
        }
        htmlEtiquetasProvincia += ('<div class="nombreCorredor der">' + nombresDeCorredores[cor[cor.length-1]].nombreSegmento.split(" - ")[0] + '</div>');

    }

    $("#corredores .etiquetasProvincia").append(htmlEtiquetasProvincia);


    // Si no hay alguno de los dos sentidos, copio las labels y pongo el aviso
    if (cappro[1] === 0 ){
        $("#corredores .etiquetasProvincia").append(htmlEtiquetasCapital);
        $("#avisoProvincia").append('<div id="aviso">El trayecto no tiene sentido Provincia</div>');        
    }

    if (cappro[0] === 0 ){
        $("#corredores .etiquetasCapital").append(htmlEtiquetasProvincia);
        $("#avisoCapital").append('<div id="aviso">El trayecto no tiene sentido Capital</div>');
    }

    //armo segmentos
    for (var i = 0 ; i < cor.length ; i++){
        if (cappro[0] === 0 ){
            // el segmento no tiene anomalias
            $("#corredores .corredoresCapital").append('<div class="corredor segmento estado0"></div>' );
        }else{
            //demora = ( (nombresDeCorredores[corCap[i]].tiempo * (nombresDeCorredores[corCap[i]].indicador_anomalia * 100))/100+(nombresDeCorredores[corCap[i]].indicador_anomalia * 100) );
            $("#corredores .corredoresCapital").append('<div class="corredor segmento estado' + nombresDeCorredores[corCap[i]].anomalia + '"></div>' );



            //asigno tiempo de anomalia
            if (nombresDeCorredores[corCap[i]].duracion_anomalia != 0){
                duracionAnomalia = nombresDeCorredores[corCap[i]].duracion_anomalia + "'";
            }else{
                duracionAnomalia = "--";
            }
            
            //asigno tiempo de trayecto
            tiempoTrayecto = nombresDeCorredores[corCap[i]].tiempo;
    
            //asigno demora
            if (nombresDeCorredores[corCap[i]].indicador_anomalia != 0){
                var porcentaje = (tiempoTrayecto * (nombresDeCorredores[corCap[i]].indicador_anomalia *100 ).toFixed())/100;
                demora = (nombresDeCorredores[corCap[i]].indicador_anomalia *100 ).toFixed() + "% (+ " +porcentaje.toFixed()+ "')";
            }else{
                demora = "--";
            }

            //asigno causa
            if (nombresDeCorredores[corCap[i]].causa_id == 0){
                causa = "--";
            }else{
                jQuery.map(causasAnomalias.causas, function(obj) {
                  if(obj.id == nombresDeCorredores[corCap[i]].causa_id){
                    causa = obj.descripcion;
                  }
                });
            }

            //armo el panel
            $("#panelesCapital").append('<div class="panel" id="c' + corCap[i] + '">'+
                '<div class="filaPanel">Duración anomalía<div class="datoPanel">' + duracionAnomalia +'</div></div>'+
                '<div class="filaPanel">Tiempo del trayecto<div class="datoPanel">'+ tiempoTrayecto + "'" + '</div></div>'+
                '<div class="filaPanel">Demora<div class="datoPanel">'+ demora  + '</div></div>'+
                '<div class="filaPanel">Causa<div class="datoPanel">'+ causa +'</div></div></div>');
        }
        
        if (cappro[1] === 0 ){
            // el segmento no tiene anomalias
            $("#corredores .corredoresProvincia").append('<div class="corredor segmento estado0"> </div>' );
        }else{
            //demora = ( (nombresDeCorredores[corPro[i]].tiempo * (nombresDeCorredores[corPro[i]].indicador_anomalia * 100))/100+(nombresDeCorredores[corPro[i]].indicador_anomalia * 100) );
            $("#corredores .corredoresProvincia").append('<div class="corredor segmento estado' + nombresDeCorredores[corPro[i]].anomalia + ' "></div>' );


            //asigno tiempo de anomalia
            if (nombresDeCorredores[corPro[i]].duracion_anomalia != 0){
                duracionAnomalia = nombresDeCorredores[corPro[i]].duracion_anomalia + "'";
            }else{
                duracionAnomalia = "--";
            }
            
            //asigno tiempo de trayecto
            tiempoTrayecto = nombresDeCorredores[corPro[i]].tiempo;
    
            //asigno demora
            if (nombresDeCorredores[corPro[i]].indicador_anomalia != 0){
                var porcentaje = (tiempoTrayecto * (nombresDeCorredores[corPro[i]].indicador_anomalia *100 ).toFixed())/100;
                demora = (nombresDeCorredores[corPro[i]].indicador_anomalia *100 ).toFixed() + "% (+ " +porcentaje.toFixed()+ "')";
            }else{
                demora = "--";
            }

            //asigno causa
            if (nombresDeCorredores[corPro[i]].causa_id == 0){
                causa = "--";
            }else{
                jQuery.map(causasAnomalias.causas, function(obj) {
                  if(obj.id == nombresDeCorredores[corPro[i]].causa_id){
                    causa = obj.descripcion;
                  }
                });
            }
            
            //armo el panel
            $("#panelesProvincia").append('<div class="panel" id="c'+corPro[i]+'">'+
                '<div class="filaPanel">Duración anomalía<div class="datoPanel">'+ duracionAnomalia +'</div></div>'+
                '<div class="filaPanel">Tiempo del trayecto<div class="datoPanel">'+ tiempoTrayecto   + "'" +'</div></div>'+
                '<div class="filaPanel">Demora<div class="datoPanel">'+ demora + '</div></div>'+
                '<div class="filaPanel">Causa<div class="datoPanel">'+ causa +'</div></div></div>');
        }
    }

    // agrega el listener al panel del segmento que se acaba de agregar.
    $(".panel").click(function() {
        var idPanelClickeado = this.id.replace("c","");
        llenoPantallaEdicion(idPanelClickeado);
        $("#seleccioneTrayecto").css("display","none");
    });
}


//llena la pantalla de edicion del sector seleccionado
function llenoPantallaEdicion(idSegmento){

  
    var porcentaje = (nombresDeCorredores[idSegmento].tiempo * (nombresDeCorredores[idSegmento].indicador_anomalia *100 ).toFixed())/100;
    var demora = (nombresDeCorredores[idSegmento].indicador_anomalia *100 ).toFixed() + "% (+ " +porcentaje.toFixed()+ "')";

    if ( nombresDeCorredores[idSegmento].indicador_anomalia == 0) {
        demora = "--";
    }

    $("#trayecto_frm").html(nombresDeCorredores[idSegmento].nombreSegmento);
    $("#sentido_frm").html(nombresDeCorredores[idSegmento].sentido);
    $("#anomalia_frm").html(anomaliasDescripcion[nombresDeCorredores[idSegmento].anomalia]);
    $("#tiempo_frm").html(nombresDeCorredores[idSegmento].tiempo + "'");
    $("#demora_frm").html( demora );
    $("#mensajeStatus_frm").html("");
    $("#reportar_frm").show();
    $("#modificar_frm").hide();


    if ( nombresDeCorredores[idSegmento].anomalia_id != 0 ) {
        // oculto cartel de edicion..
        // console.log(nombresDeCorredores[idSegmento])
        $("#oculta").css("display", "none");
        $("#anomaly_frm").attr("value", nombresDeCorredores[idSegmento].anomalia_id);
        $("#corte_frm").val(nombresDeCorredores[idSegmento].tipo_corte);
        $("#causa_frm").val(nombresDeCorredores[idSegmento].causa_id);
        $("#descripcion_frm").val(nombresDeCorredores[idSegmento].comentario_causa);
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
    var maximoEstado = 0;
    var tieneAnonalias = false;
    var todasAnomaliasChequeadas = false;

    $("#" + data.id + " .titulo").html(data.nombre);
    $("#" + data.id).removeClass("cargando");


    // completo el sentido capital si lo hubiuese
    if (data.segmentos_capital.length != 0){
        for (var i = 0; i < data.segmentos_capital.length ; i++){
            if (data.segmentos_capital[i].anomalia_id != 0){
                tieneAnonalias = true;
                if (data.segmentos_capital[i].causa_id == 0){
                    todasAnomaliasChequeadas = true;    
                }
            }

            if (maximoEstado < data.segmentos_capital[i].anomalia){
                maximoEstado = data.segmentos_capital[i].anomalia;
            }

            nombresDeCorredores[data.segmentos_capital[i].id].sentido = "Capital";
            nombresDeCorredores[data.segmentos_capital[i].id].anomalia = data.segmentos_capital[i].anomalia;
            nombresDeCorredores[data.segmentos_capital[i].id].anomalia_id = data.segmentos_capital[i].anomalia_id;
            nombresDeCorredores[data.segmentos_capital[i].id].tipo_corte = data.segmentos_capital[i].tipo_corte;
            nombresDeCorredores[data.segmentos_capital[i].id].comentario_causa = data.segmentos_capital[i].causa;    
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

    // completo el sentido provincia si lo hubiuese
        if (data.segmentos_provincia.length != 0){
        for (var p = 0; p < data.segmentos_provincia.length ; p++){
            if (data.segmentos_provincia[p].anomalia_id != 0){
                tieneAnonalias = true;
                if (data.segmentos_provincia[p].causa_id == 0){
                    todasAnomaliasChequeadas = true;    
                }
            }


            if (maximoEstado < data.segmentos_provincia[p].anomalia){
                maximoEstado = data.segmentos_provincia[p].anomalia;
            }

            nombresDeCorredores[data.segmentos_provincia[p].id].sentido = "Provincia";
            nombresDeCorredores[data.segmentos_provincia[p].id].anomalia = data.segmentos_provincia[p].anomalia;
            nombresDeCorredores[data.segmentos_provincia[p].id].anomalia_id = data.segmentos_provincia[p].anomalia_id;
            nombresDeCorredores[data.segmentos_provincia[p].id].tipo_corte = data.segmentos_provincia[p].tipo_corte;
            nombresDeCorredores[data.segmentos_provincia[p].id].comentario_causa = data.segmentos_provincia[p].causa;                
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

    //asigno estado a listado de corredores
    $("#" + data.id).removeClass();
    $("#" + data.id).addClass("corredor shadow listado borde" + maximoEstado);

    //asigno el icono a los corredoresestado a listado de corredores
    var icon = $("#" + data.id + " .icono");
    icon.removeClass()
    icon.addClass("icono");

    if (tieneAnonalias){
        if (todasAnomaliasChequeadas){
            icon.addClass("iconoRojo");
        }else{
            icon.addClass("iconoAzul");
        }
    }else{
        icon.addClass("iconoGris");
    }

    var datos = JSON.parse('{'+texto+'}');
    corredores[data.id] = datos;

}

function updateUltimaActualizacion(data){
    $("#ultimaActualizacion").html(data);
}

function panTo(geo) {
    var latLng = new google.maps.LatLng(geo.split(",")[0],geo.split(",")[1]);
    map.panTo(latLng);
}


// abre pantalla anomalias
$("#verAnomalias").click(function() {
    window.location = "/anomalies";
});
