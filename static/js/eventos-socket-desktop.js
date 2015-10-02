// instancio socket y me conecto a la ruta /alertas
var socket = io.connect('/alertas', {
	'force new connection': true
});

socket.on('connect', function() {
	console.log("Connected.");
	socket.emit('receive', "Connected");
});

socket.on('error', function(e) {
	console.log("error")
});
socket.on('info', function(e) {
	console.log(e)
});
socket.on('disconnect', function(e) {
	console.log("Disconnect.")
	var socket = io.connect('/alertas', {
		'force new connection': true
	});
});
// aqui especificamos el canal para la recepcion continua de los datos
socket.on('independencia', function(data) {
	actualizacionDesktop(data);
});
socket.on('Illia', function(data) {
	actualizacionDesktop(data);
});
socket.on('9_de_julio', function(data) {
	console.log("9_de_julio --->", data)
	actualizacionDesktop(data);
});
socket.on('cerrito', function(data) {
	console.log("cerrito -->", data)
	actualizacionDesktop(data);
});
socket.on('pellegrini', function(data) {
	console.log("pellegrini -->", data)
	actualizacionDesktop(data);
});
socket.on('alem', function(data) {
	actualizacionDesktop(data);
});
socket.on('corrientes', function(data) {
	actualizacionDesktop(data);
});
socket.on('rivadavia', function(data) {
	actualizacionDesktop(data);
});
socket.on('av_de_mayo', function(data) {
	actualizacionDesktop(data);
});
socket.on('san_martin', function(data) {
	actualizacionDesktop(data);
});
socket.on('juan_b_justo', function(data) {
	console.log("juan_b_justo -->", data)
	actualizacionDesktop(data);
});
socket.on('cordoba', function(data) {
	actualizacionDesktop(data);
});
socket.on('paseo_colon', function(data) {
	actualizacionDesktop(data);
});
socket.on('cabildo', function(data) {
	actualizacionDesktop(data);
});
socket.on('pueyrredon', function(data) {
	actualizacionDesktop(data);
});
socket.on('alcorta', function(data) {
	actualizacionDesktop(data);
});
socket.on('libertador', function(data) {
	console.log("libertador -->", data)
	actualizacionDesktop(data);
});

socket.on('ultima_actualizacion', function(data) {
	updateUltimaActualizacion(data);
});