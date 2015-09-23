<!DOCTYPE HTML>
<html lang="es">
<head>    
    <meta content="text/html; charset=utf-8" http-equiv="content-type">    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_public/css/estilos-login.min.css" />
    <link rel="icon" href="favicon.ico"/>
</head>    
<body>

    <div class="notFound">
        <h1>La página que intenta ver no esta disponible</h1>
        <div class="error"> Error {{ error }} </div>
        <button id="volver"> volver al inicio</button>
    </div>


<script>

$("#volver").click(function() {
    window.location = "/";
});
</script>

</body>
</head>