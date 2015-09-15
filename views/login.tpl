<!DOCTYPE HTML>
<html lang="es">
<head>    
    <meta content="text/html; charset=utf-8" http-equiv="content-type">    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="_public/css/estilos-login.min.css" />
    <link rel="icon" href="favicon.ico"/>
    <script src="https://www.google.com/recaptcha/api.js?hl=es" async defer></script>
</head>    
<body>
    <div class="login">
        <div class="titulo">Dashboard Tránsito</div>
        <form action="/login" method="post" name="login">
            <div class="campos">
                <label>usuario</label><br>
                <input type="text" name="username" /><br>
                <label>Contraseña</label><br>
                <input type="password" name="password" /><br>
                <p>{{ error }}</p>
                <div class="g-recaptcha" data-sitekey={{site_key}}></div>
                <div class="enviar">
                    <input type="submit" value="ENTRAR">
                </div>              
            </div>              
        </form>

    </div>
</body>
</head>