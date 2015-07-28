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

		var socket = io.connect('/alertas', {
			'force new connection': true
		});

		socket.on('connect', function() {
		    console.log("Connected.");
			socket.emit('receive', "Connected");
		});

		socket.on('nada', function(data) {
			console.log(data)
		});

		socket.on('error', function(e){
			console.log("error")
		});

		socket.on('disconnect', function(e){
			console.log("Disconnect.")
		});

	</script>
</html>