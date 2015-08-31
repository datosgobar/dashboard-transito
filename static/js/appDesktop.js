// pone los titulos a la botonera
function actualizacionDesktop(data){
    $("#" + data.id + " .titulo").html(data.nombre);
    console.log (data.id, data)
}