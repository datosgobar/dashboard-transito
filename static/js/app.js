// Trae JSON con listado de segmentos
var nombresDeCorredores = (function () {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "_static/data/segmentos.json",
        'dataType': "json",
        'success': function (data) {
        	console.log("json segmentos leido");
            archivo = data;
        }
    });
    return archivo;
})(); 


//ARMA EL HTML DE LA TARJETA
function armoTemplateCard(data) {
    var causaPendiente = false;
    var estado = 0;
    var segmentos = Math.max(data.segmentos_capital.length, data.segmentos_provincia.length);
    var nombres;


    var card = '<div class="card oculta" id="' + data.id + '">';
    card = card + "<div class='corredor'><div class='titulo'>" + data.nombre + "</div><div class='icono visto'></div></div>";

    card = card + "<div class='etiquetas'>";
    if (data.segmentos_capital.length > 0) { // hay de capital
        nombres = data.segmentos_capital;
    } else {
        nombres = data.segmentos_provincia;
    }

    for (var i = 0; i < segmentos; i++) {
        if (i === 0) {
            card = card + "<div class='segmento izquierda'>" + nombreDeCorredor(nombres[i].id).split("-")[0] + "</div>";
        } else {
            card = card + "<div class='segmento centro'>" + nombreDeCorredor(nombres[i].id).split("-")[0] + "</div>";
        }

    }
    card = card + "<div class='segmento derecha'>" + nombreDeCorredor(nombres[segmentos-1].id).split("-")[1] +"</div>";
    card = card + "</div>";




    if (data.segmentos_capital.length > 0){ // hay de capital
        card = card + '<div class="capital">';
        for (var p = 0 ; p < segmentos ; p++){
            card = card + '<div class="segmento estado'+data.segmentos_capital[p].anomalia+'"> </div>';
            if (data.segmentos_capital[p].anomalia > estado){
                estado = data.segmentos_capital[p].anomalia;
                if (data.segmentos_capital[p].causa_id === 0){ //hay probelmas pero no hay causa
                    causaPendiente = true;
                }
            }
        }
        card = card + '</div><div class="flechaCap"></div>' ;
    }



    if (data.segmentos_provincia.length > 0){ // hay de provincia
        card = card + '<div class="provincia">';
        for (var q = 0 ; q < segmentos ; q++){
            card = card + '<div class="segmento estado'+data.segmentos_provincia[q].anomalia+'"></div>';
            if (data.segmentos_provincia[q].anomalia > estado){
                estado = data.segmentos_provincia[q].anomalia;
                if (data.segmentos_provincia[q].causa_id === 0){ //hay probelmas pero no hay causa
                    causaPendiente = true;
                }
            }
        }
        card = card + '</div><div class="flechaPro"></div>' ;
    }


    card = card + "</div>";

    if (causaPendiente) {
        card = card.replace('visto', 'enProceso');
    }
    //si no hay falla entonces no mando nada.
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

    if ( card.indexOf("enProceso") > 0 ){
        $("#noResueltos").prepend(card);
    }else{
        $("#resueltos").prepend(card);
    }
	
	$(".card").fadeIn();
}


// recibo ID devuelvo nombre del corredor
function nombreDeCorredor(id){
	return nombresDeCorredores[id].nombreSegmento;
}
