<!DOCTYPE HTML>
<html lang="es">
<head>    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
	<script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<script type="text/javascript" src="_static/js/app.js"></script>
	<link rel="icon" href="favicon.ico"/>

</head>
<body>
</body>
	<script>

		// instancio socket y me conecto a la ruta /alertas
		var socket = io.connect('/alertas', {
			'force new connection': true
		});
		// cuando se establece la conecion, le envio un dato al server que envie estado 0
		socket.on('connect', function() {
		    console.log("Connected.");
			socket.emit('receive', "Connected");
		});
		// aqui especificamos el canal para la recepcion continua de los datos
		socket.on('independencia', function(data) {
			actualizacion(data);
		});
		socket.on('Illia', function(data) { // no llega el nombre en data.nombre
			actualizacion(data);
		});
		socket.on('9_de_julio', function(data) {
			actualizacion(data);
		});

		socket.on('9_de_julio_externo', function(data) {
			actualizacion(data);
		});

		socket.on('alem', function(data) {
			actualizacion(data);
		});
		socket.on('corrientes', function(data) {
			actualizacion(data);
		});
		socket.on('rivadavia', function(data) {
			actualizacion(data);
		});
		socket.on('av_de_mayo', function(data) {
			actualizacion(data);
		});
		socket.on('san_martin', function(data) {
			actualizacion(data);
		});
		socket.on('juan_b_justo', function(data) {
			actualizacion(data);
		});
		socket.on('cordoba', function(data) {
			actualizacion(data);
		});
		socket.on('paseo_colon', function(data) {
			actualizacion(data);
		});
		socket.on('cabildo', function(data) {
			actualizacion(data);
		});
		socket.on('pueyrredon', function(data) {
			actualizacion(data);
		});
		socket.on('alcorta', function(data) {
			actualizacion(data);
		});
		socket.on('libertador', function(data) {
			actualizacion(data);
		});			
		// en caso que socket disponga de un error
		socket.on('error', function(e){
			console.log("error")
		});
		// cuando el client se desconecta, socket tmb lo hace
		socket.on('info', function(e){
			console.log(e)
		});
		// cuando el client se desconecta, socket tmb lo hace
		socket.on('disconnect', function(e){
			console.log("Disconnect.")
		});

		var actualizacion = function(data){
			console.log(data)
		}



	</script>
</html>