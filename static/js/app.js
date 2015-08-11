var nombresDeCorredores = (function () {
    var archivo = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': "_static/data/segmentos.json",
        'dataType': "json",
        'success': function (data) {
        	console.log("json leido");
            archivo = data;
        }
    });
    return archivo;
})(); 


//ARMA EL HTML DE LA TARJETA
function armoTemplateCard(data){

	var estado = 0;


	var segmentos = Math.max(data.segmentos_capital.length, data.segmentos_provincia.length); ;
	var capital = '<div class="capital">';
	var provincia = '<div class="provincia">';

	var card = '<div class="card shadow oculta estadoBorde" id="' +
		data.id + '"><div class="titulo">' + data.nombre +
		'</div><div class="segmentos"><div class="contenedorSegmentos"><div class="etiquetas">';


	for (var i = 0; i < segmentos ; i++){
		var nombreSegmento = "";

		if (data.segmentos_capital.length != 0){
			nombreSegmento = data.segmentos_capital[i].id
		}else{
			nombreSegmento = data.segmentos_provincia[i].id
		}

		card = card + '<div class="segmento"><div class="etiquetaSegmento">' + nombreDeCorredor(nombreSegmento) + '</div></div>'
	}

		card = card + '</div>' 

	if (data.segmentos_capital.length > 0){ // hay de capital
		card = card + capital;
		for (var p = 0 ; p < segmentos ; p++){
			card = card + '<div class="segmento"><div class="estadoSegmento estado'+data.segmentos_capital[p].anomalia+'">'+ data.segmentos_capital[p].id+'</div></div>';
			if (data.segmentos_capital[p].anomalia > estado){
				estado = data.segmentos_capital[p].anomalia;
			}
		}
		card = card + '</div>' 
	}

	if (data.segmentos_provincia.length > 0){ // hay de provincia
		card = card + provincia;
		for (var q = 0 ; q < segmentos ; q++){
			card = card + '<div class="segmento"><div class="estadoSegmento estado'+data.segmentos_provincia[q].anomalia+'">'+ data.segmentos_provincia[q].id+'</div></div>';
			if (data.segmentos_provincia[q].anomalia > estado){
				estado = data.segmentos_provincia[q].anomalia;
			}
		}
		card = card + '</div>' 
	}


	card = card + '</div></div><div class="icono"> </div></div></div>';
	card = card.replace('estadoBorde', 'estadoBorde'+estado);
    
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
	$("#cards").prepend(card);
	$(".card").fadeIn();
}


// recibo ID devuelvo nombre del corredor
function nombreDeCorredor(id){
	return nombresDeCorredores[id].nombreSegmento;
}
