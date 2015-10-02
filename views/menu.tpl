<!DOCTYPE HTML>
<html>
<head>    
    <title>Dashboard de Tránsito</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<link rel="icon" href="favicon.ico"/>
    <style>

        @font-face {
          font-family: 'Gotham';
          font-style: normal;
          font-weight: normal;
          src:  url("_static/css/fonts/gotham.eot?#iefix") format("embedded-opentype"),
                url("_static/css/fonts/gotham.woff2") format("woff2"),
                url("_static/css/fonts/gotham.woff") format("woff"),
                url("_static/css/fonts/gotham.ttf") format("truetype"),
                url("_static/css/fonts/gotham.svg#Gotham") format("svg");
        }
        html, body {
            background: #282D33 url("_static/css/img/login.jpg") no-repeat center center;
            font-family: "Gotham", "Helvetica Neue", Helvetica, Arial, sans-serif;

        }

        .centro .panelMenu {
            padding: 0;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            margin: auto;
            width: 100%;
            height: 150px;
            z-index: 999
        }

        .centrado {
            text-align: center
        }

        .buttonMenu{
            width: 150px;
            height: 150px;
            border-radius: 75px;
            background-color: white;
            display: inline-block;
            line-height: 340px;
            font-size: 1em;
            color: white;
            text-transform: uppercase;
        }
        a, a:hover{
            margin-left: 20px;
            margin-right: 20px;
            color: black;
            text-decoration: none;
        }
    </style>    

</head>

<body>
    <div class="centro">
        <div class="panelMenu centrado">
            <a href=""><div class="buttonMenu">icono 1</div></a>
            <a href=""><div class="buttonMenu">icono 2</div></a>
            <a href=""><div class="buttonMenu">icono 3</div></a>
        </div>
    </div>
</body>
</html>


