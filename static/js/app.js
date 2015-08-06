//ARMA EL HTML DE LA TARJETA
function armoTemplateCard(data){

	var card = '<div class="card shadow oculta" id="' + data.id + '"><div class="titulo">' + data.nombre + '</div><div class="segmentos"><div class="contenedorSegmentos"><div class="etiquetas">';
	var capital = '<div class="capital">';
	var provincia = '<div class="provincia">';

	for (var i = 0; i < data.segmentos.length; i++){
		card = card + '<div class="segmento"><div class="etiquetaSegmento">' + 'Seg '+ (i+1) + '</div></div>'
	}


	card = card + '</div></div></div></div>';

	return card;
}

// Agrega una tarjeta al principio del div #cards
function agregaCard(data){
	if ( $("#"+data.id).length != 0 ){
		$("#"+data.id).remove();
	}
	var card = completoCard( armoTemplateCard(data) );
	$("#cards").prepend(card);
	$(".card").fadeIn();
}

function completoCard(tarjeta){
	return tarjeta;
}
