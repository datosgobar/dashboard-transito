//ARMA EL HTML DE LA TARJETA
function armoTemplateCard(nombre, segmentos){


	var card = '<div class="card shadow oculta" id="' + nombre + '"><div class="titulo">' + nombre + '</div><div class="segmentos"><div class="contenedorSegmentos"><div class="etiquetas">';

	for (var i = 0; i < segmentos; i++){
		card = card + '<div class="segmento"><div class="etiquetaSegmento">' + 'Segmento ' + (i+1) + '</div></div>'
	}

	card = card + '</div> <div class="capital">';

	for (var i = 0; i < segmentos; i++){
		card = card + '<div class="segmento"><div class="estadoSegmento"></div></div>';
	}

	card = card + '</div>  <div class="provincia">';
	for (var i = 0; i < segmentos; i++){
		card = card + '<div class="segmento"><div class="estadoSegmento"></div></div>';
	}

	card = card + '</div></div></div></div>';

	return card;
}

// Agrega una tarjeta al principio del div #cards
function agregaCard(data){
	if ( $("#"+data.nombre).length != 0 ){
		$("#"+data.nombre).remove();

	}
	var card = completoCard( armoTemplateCard(data.nombre, data.segmentos.length) );
	$("#cards").prepend(card);
	$(".card").fadeIn();
}

function completoCard(tarjeta){
	return tarjeta;
}

