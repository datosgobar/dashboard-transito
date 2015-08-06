//ARMA EL HTML DE LA TARJETA
function armoTemplateCard(data){
	var segmentos = Math.max(data.segmentos_capital.length, data.segmentos_provincia.length); ;
	var capital = '<div class="capital">';
	var provincia = '<div class="provincia">';

	var card = '<div class="card shadow oculta" id="' +
		data.id + '"><div class="titulo">' + data.nombre +
		'</div><div class="segmentos"><div class="contenedorSegmentos"><div class="etiquetas">';


	for (var i = 0; i < segmentos ; i++){
		card = card + '<div class="segmento"><div class="etiquetaSegmento">' + 'Seg '+ (i+1) + '</div></div>'
	}
		card = card + '</div>' 

	if (data.segmentos_capital.length > 0){ // hay de capital
		card = card + capital;
		for (var i = 0 ; i < segmentos ; i++){
			card = card + '<div class="segmento"><div class="estadoSegmento"> </div></div>';
		}
		card = card + '</div>' 
	}

	if (data.segmentos_provincia.length > 0){ // hay de provincia
		card = card + provincia;
		for (var i = 0 ; i < segmentos ; i++){
			card = card + '<div class="segmento"><div class="estadoSegmento"> </div></div>';
		}
		card = card + '</div>' 
	}

	card = card + '</div></div><div class="icono"> </div></div></div>';

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



