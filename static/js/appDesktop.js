
// Trae JSON con listado de causas de una anomalia
var causasAnomalias = (function () {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "_static/data/causas.json",
        'dataType': "json",
        'success': function (data) {
            archivo = data;
            armoSelectAnomalias(data);
        }
    });
    return archivo;
})(); 
function armoSelectAnomalias(datos){
    
    for (var i = 0 ; i < datos.causas.length; i++  ){
        $("#causa").append('<option value="'+ datos.causas[i].id +'">'+ datos.causas[i].descripcion +'</option>');
    }
 
}


// pone los titulos a la botonera
function actualizacionDesktop(data){
    $("#" + data.id + " .titulo").html(data.nombre);
}

// mapa a full height
$("#logo").on("click", function() {
    console.log ("logo");
  $("#mapa").animate({height: "100%"}, 200);
});

// mapa comprimido
$(".corredor").click(function() {
    console.log ("corredor");
  $("#mapa").animate({height: "300px"}, 200);
});

