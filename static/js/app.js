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


//ARMA EL HTML DE LA TARJETA DE LA VENTANA PRINCIPAL
function armoTemplateCard(data) {

    var causaPendienteCap = false;
    var causaPendientePro = false;
    var estado = 0;
    var segmentos = Math.max(data.segmentos_capital.length, data.segmentos_provincia.length);
    var nombres;
    var card = '<div class="card oculta" id="' + data.id + '">';
    card = card + "<div class='corredor'><div class='titulo'>" + data.nombre + "</div><div class='icono enProceso'></div></div>";

    card = card + "<div class='contenedor'><div class='etiquetas'>";
    if (data.segmentos_capital.length > 0) { // hay de capital
        nombres_capi = data.segmentos_capital;
        for (var i = 0; i < segmentos; i++) {
            if (i === 0) {
                card = card + "<div class='segmento izquierda'>" + nombreDeCorredor(nombres_capi[i].id).split("-")[0] + "</div>";
            } else {
                card = card + "<div class='segmento centro'>" + nombreDeCorredor(nombres_capi[i].id).split("-")[0] + "</div>";
            }
        }
        card = card + "<div class='segmento derecha'>" + nombreDeCorredor(nombres_capi[segmentos-1].id).split("-")[1] +"</div>";
    } else {
        nombres_prov = data.segmentos_provincia;
        for (var i = 0; i < segmentos; i++) {
            if (i === 0) {
                card = card + "<div class='segmento izquierda'>" + nombreDeCorredor(nombres_prov[i].id).split("-")[1] + "</div>";
            } else {
                card = card + "<div class='segmento centro'>" + nombreDeCorredor(nombres_prov[i].id).split("-")[1] + "</div>";
            }
        }
        card = card + "<div class='segmento derecha'>" + nombreDeCorredor(nombres_prov[segmentos-1].id).split("-")[0] +"</div>";
    }
    
    card = card + "</div></div>";



    if (data.segmentos_capital.length > 0){ // hay de capital
        card = card + '<div class="contenedor"><div class="capital">';
        for (var p = 0 ; p < segmentos ; p++){
            card = card + '<div class="segmento chico estado'+data.segmentos_capital[p].anomalia+'">s:'+ data.segmentos_capital[p].id + '-c:' + data.segmentos_capital[p].causa_id +'</div>';
            if (data.segmentos_capital[p].anomalia > estado){
                estado = data.segmentos_capital[p].anomalia;
                if (data.segmentos_capital[p].causa_id === 0){ //hay problemas pero no hay causa
                    causaPendienteCap = true;
                }
            }
        }
        card = card + '</div><div class="flechaCap"></div></div>' ;
    }



    if (data.segmentos_provincia.length > 0){ // hay de provincia
        card = card + '<div class="contenedor"><div class="provincia">';
        for (var q = 0 ; q < segmentos ; q++){
            card = card + '<div class="segmento chico estado'+data.segmentos_provincia[q].anomalia+'">s:'+ data.segmentos_provincia[q].id + '-c:' + data.segmentos_provincia[q].causa_id + '</div>';
            if (data.segmentos_provincia[q].anomalia > estado){
                estado = data.segmentos_provincia[q].anomalia;
                if (data.segmentos_provincia[q].causa_id === 0){ //hay problemas pero no hay causa
                    causaPendientePro = true;
                }
            }
        }
        card = card + '</div><div class="flechaPro"></div>' ;
    }

    card = card + "</div>";

    //todos los segmentos con causa_id > 0 azul
    //algun segmento con causa_id = 0 rojo


    //cambio el icono
    if (causaPendienteCap || causaPendientePro){
        card = card.replace('enProceso','noVisto');        
    }

    if (estado === 0){
        card = "";
    }


    return card;
}


// Agrega una tarjeta al principio del div #cards
function agregaCard(data){
	if ( $("#"+data.id).length != 0 ){
		$("#"+data.id).remove();
	}
	var card = armoTemplateCard(data);

    if ( card.indexOf("noVisto") > 0 ){
        $("#noResueltos").prepend(card);
    }else{
        $("#resueltos").prepend(card);
    }
	
	$(".card").fadeIn();

    marquee();
}


function marquee(){
    if ($(".corredor").length < 5){
        $("#cards").removeClass("marquee");
    }else{
        $("#cards").addClass("marquee");
    }
}

// recibo ID devuelvo nombre del corredor
function nombreDeCorredor(id){
	return nombresDeCorredores[id].nombreSegmento;
}

