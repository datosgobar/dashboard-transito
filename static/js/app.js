//Recibe un string mal formateado y lo devuelve con palabras separadas por espacio y capitalizado
function formateoTexto(texto_no_formateado){
	var texto_formateado = texto_no_formateado.replace(/\_/gi, " ");
	return texto_formateado.toLowerCase().replace( /\b./g, function(a){ return a.toUpperCase(); } );
}

//escribe de manera rudimentaria los datos recibidos al dom
function renderPantalla(data){

}
