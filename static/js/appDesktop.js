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

function armoSelectAnomalias(datos) {
    for (var i = 0; i < datos.causas.length; i++) {
        $("#causa_frm").append('<option value="' + datos.causas[i].id + '">' + datos.causas[i].descripcion + '</option>');
    }

}


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

// pone los titulos a la botonera
function actualizacionDesktop(data) {
    $("#" + data.id + " .titulo").html(data.nombre);
}

// mapa a full height
$("#logo").on("click", function() {
    console.log("logo");
    $("#mapa").animate({
        height: "100%"
    }, 200);
});

// mapa comprimido
$(".corredor").click(function() {
    console.log("corredor");
    $("#mapa").animate({
        height: "300px"
    }, 200);
});
