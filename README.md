:blue_car: :red_car:
# Dashboard Operativo Transito

Desde el Centro de Control de Tránsito los operadores monitorean el sistema de tránsito y toman decisiones en tiempo real con el objetivo de descomprimir el tránsito.
Este dashboard muestra las anomalías de diferentes corredores prioritarios de la ciudad de acuerdo a un análisis periódico basado en información histórica

La vista principal estará siempre visible en un videowall.
El dashboard también se accede desde las computadoras de los operarios para visualizar en detalle la anomalía, comparar los datos con la vista de tráfico de Google Maps y asignarles una causa. Esta data se recolectará para ser usada en un análisis posterior.


La aplicacion se divide en dos partes.

Analisis - ( deteccion de anomalias )

Dispone de una interaccion directa con el servicio cloud Api Sensores https://apisensores.buenosaires.gob.ar, extrae los datos cada un intervalo determinado segun el rango horario y el dia, esto genera un analisis que determina la cantidad de anomalias.

Los errores que pueden generar la falla de conexion entre el servicio apisensores o la perdida conexion con la base de datos, se hacen ademas de logs  mediante el envio de email via smtp.buenosaires.gob.ar puerto (25).

Los datos de configuracion estan en analisis/config.py.sample (api + email)

WebApp - ( Dashboard )

Tiene un login, con captcha que necesita tener interaccion con google https://www.google.com/recaptcha/api/siteverify


## Instalacion bajo Linux

Tener instalado MySQL 5.1

```sh
$ apt-get install mysql-server
```

Instalamos las dependecias a mano de la siguiente manera:

```sh
$ sudo pip install bottle==0.10.1
$ sudo pip install bottle-cork==0.11.1
$ sudo pip install gevent==1.1b1
$ sudo pip install gevent-socketio==0.3.5
$ sudo pip install requests==2.7.0
$ sudo pip install requests[security]
$ sudo pip install MySQL-python==1.2.3
$ sudo pip install sqlalchemy==1.0.8
$ sudo pip install sqlalchemy-migrate==0.9.7
$ sudo pip install python-dateutil
$ sudo pip install numpy==1.9.2
$ sudo pip install pandas==0.16.2
$ sudo pip install gunicorn==19.3.0
$ sudo pip install supervisor==3.1.3
```

## Instalacion bajo Mac

```sh
brew install mysql-server
mysql.server start
```

## Instalacion bajo Windows

Bajar e instalar [Visual C++ for Python 2.7](http://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi) y [MySQL for Python](https://github.com/farcepest/MySQLdb1)

```sh
Utilizar easy_install en la instalacion dependencias 
```

## Corriendo la app 

* Actualizar datos de conexion a base de datos en (una muestra se puede encontrar en analisis/config.py.sample)


* Asegurarse que MySQL está corriendo

```sh
 mysql.server start
 ```

* Configuración de la Base de Datos

  * Creación de las tablas
    Ir a /db_repository y leer README correspondiente
  * Generación de data fake (no es necesario en produccion)
```sh
$ python analisis/getDataFake.py
```

  * Configuración del modelo. 

    Para esto hay dos alternativas, utilizar la segunda si la primera falla:

    1. Crear un nuevo modelo

        Cargar datos:

            Bajar los datos de Teracode

            $ python analisis.py --download_last_month

        Generar Modelo:

            $ python analisis.py --generate_detection_params

    2. Copiar un modelo existente creando un archivo detection_params.json en el directorio ./analisis
    Un modelo se puede encontrar en /analisis/detection_params.json.sample




## Configurar script para actualizacón de modelo en cron. 

Se ejecuta una vez al día a las 00hs.

```sh
sudo crontab -e
0 0 * * * /usr/bin/python2.7 /tu_home/tu_user/dashboard-operativo-transito/analisis/dailyUpdate.py
```

## Ejectuar Schedule e Instanciar Applicacion Web

Estos procesos son los encargados para extracción y carga de datos de Api Sensores de acuerdo a la frecuencia establecida.
La función que se llama periódicamente es executeLoop() ejecutada por schedule.py

### A mano en localhost:

* Ejecutar Schedule
```sh
$ python analisis/schedule.py
```

* Instanciar Python Server en Local
```sh
$ gunicorn -b 0.0.0.0:8080 --worker-class socketio.sgunicorn.GeventSocketIOWorker app:app 
or
$ python app.py
```

### Como Demonio:


1. Configurar Variables de configuracion en archivo supervisord.conf, 
  en scheduletransito los path y el user (whoami), en webapp solo el user.

  [program:scheduletransito]

    * command
    * stdout_logfile
    * stderr_logfile
    * user

  [program:webapp]

    * user

2. Ejecutar supervisor para instanciar los procesos en daemon. 


```sh
$ supervisord -c supervisord.conf
```

Verificar que estan daemonizados.

```sh
Output esperado a modo ejemplo
supervisorctl -i
scheduletransito RUNNING pid 6734, uptime 0:00:40
webapp RUNNING pid 6733, uptime 0:00:40
supervisor> 
```

Para monitorear, y reiniciar los procesos


```sh
$ cd dashboard-operativo-transito/
$ supervisorctl -i
status scheduletransito
status webapp
restart scheduletransito
restart webapp
supervisor> help
```

Para parar todos los procesos correr

```sh
$ supervisorctl stop all
```


* Abrir el navegador en [http://127.0.0.1:8080/](http://127.0.0.1:8080/)


## Documentación 

  - [bottle](http://bottlepy.org/docs/dev/index.html)
  - [gevent](http://gevent.org/intro.html)
  - [gevent-socketio](https://gevent-socketio.readthedocs.org/en/latest/)
  - [supervisor](http://supervisord.org/configuration.html)
  - [gunicorn](http://gunicorn.org/#quickstart)

## Licencia
[MIT](http://opensource.org/licenses/MIT)
