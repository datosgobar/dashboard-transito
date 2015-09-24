<!DOCTYPE HTML>
<html lang="es">
<head>    
    <meta content="text/html; charset=utf-8" http-equiv="content-type">    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <link rel="icon" href="favicon.ico"/>
</head>    
<style type="text/css">
    h1 {
        display: block;
        font-size: 2em;
        -webkit-margin-before: 0.67em;
        -webkit-margin-after: 0.67em;
        -webkit-margin-start: 0px;
        -webkit-margin-end: 0px;
        font-weight: bold;
    }
    body, html {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background: url('/_public/css/img/login.jpg') center center/cover no-repeat #16191C;
    }
    div {
        display: block;
    }    
    .notFound {
        font-family: AvenirNext-Regular,"Helvetica Neue",Helvetica,Arial,sans-serif;
        line-height: 55px;
        font-size: 14px;
        color: #CFD1D1;
        box-shadow: 0 0 20px 0 rgba(0,0,0,.5);
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-300px,-120px);
        width: 600px;
        height: 240px;
        border-radius: 10px;
        background-color: #16191C;
        padding-left: 20px;
        padding-right: 20px;
        text-align: center;
    }
    .notFound a:hover {
        background-color: #3C434D;
    }
    .notFound a {
        cursor: pointer;
        background-color: transparent;
        color: #CFD1D1;
        border: 2px solid #CFD1D1;
        border-radius: 50px;
        font-size: 12px;
        font-family: AvenirNext-Demi,"Helvetica Neue",Helvetica,Arial,sans-serif;
        padding: 5px 20px;
        margin-top: 20px;
    } 
</style>
<body>

    <div class="notFound">
        <h1>La página que intenta ver no esta disponible</h1>
        <div class="error"> Error {{ error }} </div>
        <a href="/" id="volver"> volver al inicio</a>
    </div>

    <script type="text/javascript" src="_public/js/jquery-2.1.3.min.js"></script>
    <link rel="stylesheet" href="_public/css/estilos-login.min.css" />
</body>
</html>