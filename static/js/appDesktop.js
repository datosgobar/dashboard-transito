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

