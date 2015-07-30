<!DOCTYPE html>
<meta charset="utf-8">
<head>
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
	<script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
</head>
<body>
	<p>a</p>
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
		socket.on('corredores', function(data) {
			console.log(data)
		});
		
		// en caso que socket disponga de un error
		socket.on('error', function(e){
			console.log("error")
		});

		// cuando el client se desconecta, socket tmb lo hace
		socket.on('disconnect', function(e){
			console.log("Disconnect.")
		});

	</script>
</html>