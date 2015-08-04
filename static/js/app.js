//Recibe un string mal formateado y lo devuelve con palabras separadas por espacio y capitalizado
function formateoTexto(texto_no_formateado){
	var texto_formateado = texto_no_formateado.replace(/\_/gi, " ");
	return texto_formateado.toLowerCase().replace( /\b./g, function(a){ return a.toUpperCase(); } );
	//return texto_formateado.charAt(0).toUpperCase() + texto_formateado.slice(1);;

}